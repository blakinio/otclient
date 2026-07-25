local sourceDir = assert(os.getenv('OTCLIENT_SOURCE_DIR'), 'OTCLIENT_SOURCE_DIR is required')
local Core = dofile(sourceDir .. '/modules/game_actionbar/cooldown_lifecycle_core.lua')

local function withHarness(callback)
    local names = {
        'ActionBarController',
        'ActionBarCooldownLifecycleCore',
        'LocalPlayer',
        'Spells',
        'actionBars',
        'activeActionBars',
        'checkRemainSpellCooldown',
        'connect',
        'disconnect',
        'g_clock',
        'g_game',
        'getButtonCache',
        'modules',
        'onHotkeyItems',
        'onMultiUseCooldown',
        'onPassiveData',
        'onSpellCooldown',
        'onSpellGroupCooldown',
        'onSpellsChange',
        'onUpdateLevel',
        'removeCooldown',
        'removeEvent',
        'scheduleEvent',
        'setupActionBar',
        'spellCooldownCache',
        'spellGroupCooldownCache',
        'toggleCooldownOption',
        'updateActionBarEventSubscriptions',
        'updateButtonState',
        'updateCooldown',
        'updateInventoryItems',
        'updateMultiButtonState'
    }
    local saved = {}
    for _, name in ipairs(names) do
        saved[name] = rawget(_G, name)
    end
    local savedTableEmpty = table.empty

    local state = {
        connected = 0,
        disconnected = 0,
        originalGroupCalls = 0,
        originalSpellCalls = 0,
        originalStartCalls = 0,
        sequence = {},
        updates = {},
        visuals = false
    }

    local button = {
        cache = {
            spellData = { id = 100, groups = { 1, 2 } },
            removeCooldownEvent = 'old-event'
        },
        cooldown = {}
    }
    function button:isDestroyed() return false end
    function button:getChildById(id)
        if id == 'item' then return {} end
        return nil
    end

    local tabBar = {}
    function tabBar:getChildren() return { button } end
    local actionBar = { tabBar = tabBar }

    table.empty = function(values)
        return type(values) ~= 'table' or next(values) == nil
    end

    ActionBarCooldownLifecycleCore = Core
    LocalPlayer = {}
    Spells = {
        getGroupIds = function(spellData) return spellData.groups end,
        getRuneSpellByItem = function() return nil end
    }
    actionBars = { actionBar }
    activeActionBars = { actionBar }
    spellCooldownCache = {}
    spellGroupCooldownCache = {}

    modules = {
        client_options = {
            getOption = function()
                return state.visuals
            end
        }
    }
    g_clock = { millis = function() return 1000 end }
    g_game = { isOnline = function() return true end }

    getButtonCache = function(target) return target.cache end
    updateMultiButtonState = function() end
    updateButtonState = function() end
    onUpdateLevel = function() end
    onSpellsChange = function() end
    onHotkeyItems = function() end
    onPassiveData = function() end
    onMultiUseCooldown = function() end
    updateInventoryItems = function() end

    removeEvent = function(eventId)
        state.sequence[#state.sequence + 1] = 'removeEvent:' .. tostring(eventId)
    end
    removeCooldown = function(target)
        state.sequence[#state.sequence + 1] = 'removeCooldown'
        target.cache.removeCooldownEvent = nil
    end
    updateCooldown = function(_, remaining)
        state.sequence[#state.sequence + 1] = 'updateCooldown'
        state.updates[#state.updates + 1] = remaining
    end
    scheduleEvent = function()
        return 'new-event'
    end

    setupActionBar = function()
        state.sequence[#state.sequence + 1] = 'setup'
    end
    checkRemainSpellCooldown = function()
        state.sequence[#state.sequence + 1] = 'fallback'
    end
    onSpellCooldown = function()
        state.originalSpellCalls = state.originalSpellCalls + 1
    end
    onSpellGroupCooldown = function()
        state.originalGroupCalls = state.originalGroupCalls + 1
    end
    toggleCooldownOption = function() end
    updateActionBarEventSubscriptions = function() end

    ActionBarController = {}
    function ActionBarController:onInit() end
    function ActionBarController:onTerminate() end
    function ActionBarController:onGameStart()
        state.originalStartCalls = state.originalStartCalls + 1
        spellGroupCooldownCache = {}
        setupActionBar(1)
    end
    function ActionBarController:onGameEnd() end

    connect = function()
        state.connected = state.connected + 1
    end
    disconnect = function()
        state.disconnected = state.disconnected + 1
    end

    local loadSuccess, loadError = pcall(dofile, sourceDir .. '/modules/game_actionbar/cooldown_lifecycle.lua')
    if not loadSuccess then
        table.empty = savedTableEmpty
        for _, name in ipairs(names) do rawset(_G, name, saved[name]) end
        error(loadError, 0)
    end

    local success, result = xpcall(function()
        callback(state, button)
    end, debug.traceback)

    table.empty = savedTableEmpty
    for _, name in ipairs(names) do rawset(_G, name, saved[name]) end

    if not success then error(result, 0) end
end

test('action-bar adapter caches packets when cooldown visuals are disabled', function()
    withHarness(function(state)
        onSpellCooldown(100, 1500)
        onSpellGroupCooldown(2, 2500)

        assertEqual(0, state.originalSpellCalls)
        assertEqual(0, state.originalGroupCalls)
        assertEqual(1500, spellCooldownCache[100].exhaustion)
        assertEqual(2500, spellGroupCooldownCache[2].exhaustion)
    end)
end)

test('action-bar adapter restores the longest applicable cooldown', function()
    withHarness(function(state, button)
        state.visuals = true
        spellCooldownCache[100] = { startTime = 0, exhaustion = 1500 }
        spellGroupCooldownCache[1] = { startTime = 0, exhaustion = 1200 }
        spellGroupCooldownCache[2] = { startTime = 0, exhaustion = 3000 }

        assertTrue(checkRemainSpellCooldown(button, 100))
        assertEqual(2000, state.updates[#state.updates])
    end)
end)

test('action-bar adapter clears stale widget state before rebuilding and restoring', function()
    withHarness(function(state)
        state.visuals = true
        spellCooldownCache[100] = { startTime = 1000, exhaustion = 2000 }

        setupActionBar(1)

        assertEqual('removeEvent:old-event', state.sequence[1])
        assertEqual('removeCooldown', state.sequence[2])
        assertEqual('setup', state.sequence[3])
        assertEqual('removeCooldown', state.sequence[4])
        assertEqual('updateCooldown', state.sequence[5])
    end)
end)

test('action-bar adapter preserves pre-UI packets through controller start', function()
    withHarness(function(state)
        state.visuals = true
        onSpellGroupCooldown(2, 3000)
        ActionBarController:onGameStart()

        assertEqual(1, state.originalStartCalls)
        assertEqual(3000, spellGroupCooldownCache[2].exhaustion)
        assertEqual(3000, state.updates[#state.updates])
    end)
end)

test('action-bar adapter owns module-lifetime subscriptions and cleanup', function()
    withHarness(function(state)
        ActionBarController:onInit()
        assertEqual(2, state.connected)

        updateActionBarEventSubscriptions()
        assertEqual(2, state.connected)

        ActionBarController:onTerminate()
        assertEqual(2, state.disconnected)
    end)
end)
