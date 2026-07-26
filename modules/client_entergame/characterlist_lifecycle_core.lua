local CharacterListLifecycleCore = {}

local MODULE_UI_ROOT = '/client_entergame/'
local DEFAULT_LAYOUT = 'characterlist'
local LAYOUT_EXTENSION = '.otui'

local function isNonEmptyString(value)
    return type(value) == 'string' and value ~= ''
end

local function normalizeSeparators(path)
    return tostring(path or ''):gsub('\\', '/')
end

local function stripCurrentDirectory(path)
    while path:sub(1, 2) == './' do
        path = path:sub(3)
    end
    return path
end

local function containsTraversal(path)
    for segment in path:gmatch('[^/]+') do
        if segment == '..' then
            return true
        end
    end
    return false
end

local function ensureLayoutExtension(path)
    if path:sub(-#LAYOUT_EXTENSION):lower() == LAYOUT_EXTENSION then
        return path
    end
    return path .. LAYOUT_EXTENSION
end

function CharacterListLifecycleCore.normalizeLayoutPath(resources, layoutName)
    if resources == nil or type(resources.guessFilePath) ~= 'function' then
        return nil, 'invalid_resources'
    end

    local requestedLayout = isNonEmptyString(layoutName) and layoutName or DEFAULT_LAYOUT
    requestedLayout = stripCurrentDirectory(normalizeSeparators(requestedLayout))
    if not isNonEmptyString(requestedLayout) or containsTraversal(requestedLayout) then
        return nil, 'invalid_layout'
    end

    local explicitlyAbsolute = requestedLayout:sub(1, 1) == '/'
    local success, guessedPath = pcall(resources.guessFilePath, requestedLayout, 'otui')
    if not success or not isNonEmptyString(guessedPath) then
        return nil, 'invalid_layout'
    end

    guessedPath = normalizeSeparators(guessedPath)
    if containsTraversal(guessedPath) then
        return nil, 'invalid_layout'
    end

    if explicitlyAbsolute then
        if guessedPath:sub(1, 1) ~= '/' then
            return nil, 'invalid_layout'
        end
        return guessedPath
    end

    -- A deferred UI callback may have no active module source context, causing
    -- later ResourceManager::resolvePath to resolve a relative layout at `/`.
    -- Build the absolute module-local path before handing it to displayUI.
    return MODULE_UI_ROOT .. ensureLayoutExtension(requestedLayout)
end

function CharacterListLifecycleCore.shouldRecreate(isCreated, characters, account)
    return not isCreated and type(characters) == 'table' and account ~= nil
end

return CharacterListLifecycleCore
