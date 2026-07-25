local CharacterListLifecycleCore = dofile('characterlist_lifecycle_core')

local originalCreate = CharacterList.create
local originalDestroy = CharacterList.destroy
local originalHide = CharacterList.hide
local originalShowAgain = CharacterList.showAgain

local currentLayoutPath = nil
local characterListCreated = false

local function restoreEnterGame()
    if EnterGame and EnterGame.show and not g_game.isOnline() then
        EnterGame.show()
    end
end

local function reportFailure(message)
    g_logger.error(string.format('Character list lifecycle error: %s', tostring(message)))
    restoreEnterGame()
end

local function cleanupPartialWindow()
    pcall(originalDestroy)
    characterListCreated = false
end

function CharacterList.create(characters, account, otui)
    local layoutPath, pathError = CharacterListLifecycleCore.normalizeLayoutPath(g_resources, otui)
    if not layoutPath then
        reportFailure(pathError)
        return false
    end

    currentLayoutPath = layoutPath
    characterListCreated = false

    local lookupSuccess, layoutExists = pcall(g_resources.fileExists, layoutPath)
    if not lookupSuccess then
        reportFailure(layoutExists)
        cleanupPartialWindow()
        return false
    end
    if not layoutExists then
        reportFailure(string.format("layout '%s' was not found", layoutPath))
        cleanupPartialWindow()
        return false
    end

    local success, createError = pcall(originalCreate, characters, account, layoutPath)
    if not success then
        reportFailure(createError)
        cleanupPartialWindow()
        return false
    end

    characterListCreated = true
    return true
end

function CharacterList.destroy()
    local success, destroyError = pcall(originalDestroy)
    characterListCreated = false

    if not success then
        reportFailure(destroyError)
        return false
    end

    return true
end

function CharacterList.hide(showLogin)
    if not characterListCreated then
        if showLogin then
            restoreEnterGame()
        end
        return false
    end

    local success, hideError = pcall(originalHide, showLogin)
    if not success then
        reportFailure(hideError)
        return false
    end

    return true
end

function CharacterList.showAgain()
    if CharacterListLifecycleCore.shouldRecreate(characterListCreated, G.characters, G.characterAccount) then
        if not CharacterList.create(G.characters, G.characterAccount, currentLayoutPath) then
            return false
        end
    end

    if not characterListCreated then
        return false
    end

    local success, showError = pcall(originalShowAgain)
    if not success then
        reportFailure(showError)
        cleanupPartialWindow()
        return false
    end

    return true
end
