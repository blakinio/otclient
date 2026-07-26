local CooldownLifecycleCore = rawget(_G, 'ActionBarCooldownLifecycleCore') or dofile('cooldown_lifecycle_core')

local originalSetupActionBar = setupActionBar
local originalCheckRemainSpellCooldown = checkRemainSpellCooldown
local originalOnSpellCooldown = onSpellCooldown
local originalOnSpellGroupCooldown = onSpellGroupCooldown
local originalToggleCooldownOption = toggleCooldownOption
local originalControllerOnInit = ActionBarController.onInit
local originalControllerOnTerminate = ActionBarController.onTerminate
local originalControllerOnGameStart = ActionBarController.onGameStart
local originalControllerOnGameEnd = ActionBarController.onGameEnd

local sessionState = CooldownLifecycleCore.newSessionState()
local eventsConnected = false
local localPlayerEvents = nil
local gameEvents = nil
local rebuildSpellCache = nil
local rebuildGroupCache = nil

local function visualCooldownsEnabled()
    return CooldownLifecycleCore.shouldRender(
        modules.client_options.getOption('graphicalCooldown'),
        modules.client_options.getOption('cooldownSecond'))
end

local function buttonIsUsable(button)
    return button ~= nil and (not button.isDestroyed or not button:isDestroyed())
end

local function clearButtonCooldown(button)
    if not buttonIsUsable(button) then
        return
    end

    local cache = getButtonCache(button)
    if cache and cache.removeCooldownEvent then
        removeEvent(cache.removeCooldownEvent)
        cache.removeCooldownEvent = nil
    end
    removeCooldown(button)
end

local function getButtonSpellData(button)
    if not buttonIsUsable(button) then
        return nil
    end

    local cache = getButtonCache(button)
    if not cache then
        return nil
    end

    if cache.multiActions and not table.empty(cache.multiActions) and updateMultiButtonState then
        updateMultiButtonState(button)
        cache = getButtonCache(button)
    end

    if cache.spellData then
        return cache.spellData
    end

    if cache.itemId and cache.itemId > 0 and Spells.getRuneSpellByItem then
        return Spells.getRuneSpellByItem(cache.itemId)
    end

    return nil
end

local function getGroupIds(spellData)
    if not spellData or not Spells.getGroupIds then
        return nil
    end

    local success, groupIds = pcall(Spells.getGroupIds, spellData)
    if success and type(groupIds) == 'table' then
        return groupIds
    end
    return nil
end

local function getRemainingForButton(button, explicitSpellId)
    local spellData = getButtonSpellData(button)
    local spellId = explicitSpellId or (spellData and spellData.id)
    local spellCache = rebuildSpellCache or spellCooldownCache
    local groupCache = rebuildGroupCache or spellGroupCooldownCache
    return CooldownLifecycleCore.getMaxRemaining(
        spellCache,
        groupCache,
        spellId,
        getGroupIds(spellData),
        g_clock.millis())
end

local function applyButtonCooldown(button, remaining)
    if not buttonIsUsable(button) or not visualCooldownsEnabled() or remaining <= 0 then
        return false
    end

    clearButtonCooldown(button)
    updateCooldown(button, remaining)

    local cache = getButtonCache(button)
    cache.removeCooldownEvent = scheduleEvent(function()
        if buttonIsUsable(button) then
            removeCooldown(button)
        end
    end, remaining)
    return true
end

local function restoreButtonCooldown(button, explicitSpellId)
    local remaining = getRemainingForButton(button, explicitSpellId)
    if remaining <= 0 then
        return false
    end
    return applyButtonCooldown(button, remaining)
end

local function forEachActionButton(actionBar, callback)
    if not actionBar or not actionBar.tabBar or not callback then
        return
    end
    for _, button in pairs(actionBar.tabBar:getChildren()) do
        if button and button.getChildById and button:getChildById('item') then
            callback(button)
        end
    end
end

local function restoreAllButtonCooldowns()
    for _, actionBar in pairs(actionBars or {}) do
        forEachActionButton(actionBar, restoreButtonCooldown)
    end
end

local function clearAllButtonCooldowns()
    for _, actionBar in pairs(actionBars or {}) do
        forEachActionButton(actionBar, clearButtonCooldown)
    end
end

local function refreshActionBarStatus()
    if not g_game.isOnline() then
        return
    end
    for _, actionBar in pairs(activeActionBars or {}) do
        forEachActionButton(actionBar, updateButtonState)
    end
end

function onSpellCooldown(spellId, delay)
    CooldownLifecycleCore.ensureSession(sessionState, spellCooldownCache, spellGroupCooldownCache)
    CooldownLifecycleCore.recordCooldown(spellCooldownCache, spellId, delay, g_clock.millis())

    if not visualCooldownsEnabled() then
        return true
    end
    return originalOnSpellCooldown(spellId, delay)
end

function onSpellGroupCooldown(groupId, delay)
    CooldownLifecycleCore.ensureSession(sessionState, spellCooldownCache, spellGroupCooldownCache)
    CooldownLifecycleCore.recordCooldown(spellGroupCooldownCache, groupId, delay, g_clock.millis())

    if not visualCooldownsEnabled() then
        return true
    end
    return originalOnSpellGroupCooldown(groupId, delay)
end

function checkRemainSpellCooldown(button, spellId)
    if not visualCooldownsEnabled() then
        return true
    end

    if restoreButtonCooldown(button, spellId) then
        return true
    end

    return originalCheckRemainSpellCooldown(button, spellId)
end

function setupActionBar(index)
    local actionBar = actionBars[index]
    forEachActionButton(actionBar, clearButtonCooldown)

    local result = originalSetupActionBar(index)

    actionBar = actionBars[index]
    forEachActionButton(actionBar, restoreButtonCooldown)
    return result
end

function toggleCooldownOption()
    local result = originalToggleCooldownOption()
    if visualCooldownsEnabled() then
        restoreAllButtonCooldowns()
    else
        clearAllButtonCooldowns()
    end
    return result
end

local function buildEventMaps()
    localPlayerEvents = {
        onManaChange = refreshActionBarStatus,
        onSoulChange = refreshActionBarStatus,
        onLevelChange = onUpdateLevel,
        onSpellsChange = onSpellsChange
    }
    gameEvents = {
        onItemInfo = onHotkeyItems,
        onPassiveData = onPassiveData,
        onSpellCooldown = onSpellCooldown,
        onMultiUseCooldown = onMultiUseCooldown,
        onSpellGroupCooldown = onSpellGroupCooldown,
        updateInventoryItems = updateInventoryItems
    }
end

local function ensureEventsConnected()
    if eventsConnected then
        return
    end
    buildEventMaps()
    connect(LocalPlayer, localPlayerEvents)
    connect(g_game, gameEvents)
    eventsConnected = true
end

local function disconnectEvents()
    if not eventsConnected then
        return
    end
    disconnect(LocalPlayer, localPlayerEvents)
    disconnect(g_game, gameEvents)
    localPlayerEvents = nil
    gameEvents = nil
    eventsConnected = false
end

function updateActionBarEventSubscriptions()
    ensureEventsConnected()
end

function ActionBarController:onInit()
    local result = originalControllerOnInit(self)
    ensureEventsConnected()
    return result
end

function ActionBarController:onGameStart()
    CooldownLifecycleCore.beginSession(sessionState, spellCooldownCache, spellGroupCooldownCache)

    local preservedSpellCache = CooldownLifecycleCore.copyCache(spellCooldownCache)
    local preservedGroupCache = CooldownLifecycleCore.copyCache(spellGroupCooldownCache)
    rebuildSpellCache = preservedSpellCache
    rebuildGroupCache = preservedGroupCache

    local success, result = xpcall(function()
        return originalControllerOnGameStart(self)
    end, debug.traceback)

    CooldownLifecycleCore.mergeCache(preservedSpellCache, spellCooldownCache)
    CooldownLifecycleCore.mergeCache(preservedGroupCache, spellGroupCooldownCache)
    spellCooldownCache = preservedSpellCache
    spellGroupCooldownCache = preservedGroupCache
    rebuildSpellCache = nil
    rebuildGroupCache = nil

    if not success then
        error(result, 0)
    end

    restoreAllButtonCooldowns()
    return result
end

function ActionBarController:onGameEnd()
    CooldownLifecycleCore.endSession(sessionState, spellCooldownCache, spellGroupCooldownCache)
    return originalControllerOnGameEnd(self)
end

function ActionBarController:onTerminate()
    disconnectEvents()
    CooldownLifecycleCore.endSession(sessionState, spellCooldownCache, spellGroupCooldownCache)
    return originalControllerOnTerminate(self)
end
