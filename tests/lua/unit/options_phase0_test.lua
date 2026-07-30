local sourceDir = assert(os.getenv('OTCLIENT_SOURCE_DIR'), 'OTCLIENT_SOURCE_DIR is required')
local Core = dofile(sourceDir .. '/modules/client_options/options_migration_core.lua')

local function readFile(path)
    local file = assert(io.open(path, 'rb'))
    local content = file:read('*a')
    file:close()
    return content
end

local function countPlain(content, needle)
    local count = 0
    local position = 1
    while true do
        local found = content:find(needle, position, true)
        if not found then return count end
        count = count + 1
        position = found + #needle
    end
end

test('options migration prefers canonical, falls back to legacy and then default', function()
    assertFalse(Core.resolveInventoryExpiryValue(false, true, true))
    assertTrue(Core.resolveInventoryExpiryValue(nil, true, false))
    assertFalse(Core.resolveInventoryExpiryValue(nil, nil, false))
    assertTrue(Core.resolveInventoryExpiryValue(nil, nil, true))
end)

test('options migration recognizes canonical and legacy inventory keys only', function()
    assertTrue(Core.isInventoryExpiryKey('showExpiryInInventory'))
    assertTrue(Core.isInventoryExpiryKey('showExpiryInInvetory'))
    assertFalse(Core.isInventoryExpiryKey('showExpiryInContainers'))
end)

test('action-bar reset OTUI maps the third right bar to nine with unique ids', function()
    local content = readFile(sourceDir .. '/modules/client_options/styles/interface/actionbars.otui')
    assertTrue(content:find('@onClick: modules.game_actionbar.resetAction(9)', 1, true) ~= nil)
    assertTrue(content:find('id: resetAllActionBars', 1, true) ~= nil)
    assertEqual(1, countPlain(content, 'id: clearRightBar3'))
end)

test('options adapter does not replace global event functions', function()
    local content = readFile(sourceDir .. '/modules/client_options/options_phase0.lua')
    assertTrue(content:find('\nscheduleEvent =', 1, true) == nil)
    assertTrue(content:find('\nremoveEvent =', 1, true) == nil)
end)

local function withAdapterHarness(callback)
    local names = {
        'OptionsMigrationCore',
        'controller',
        'g_settings',
        'getOption',
        'modules',
        'panels',
        'removeEvent',
        'scheduleEvent',
        'setOption',
        'tr'
    }
    local saved = {}
    for _, name in ipairs(names) do saved[name] = rawget(_G, name) end

    local state = {
        checked = nil,
        cooldownText = nil,
        cooldownTooltip = nil,
        nextEvent = 0,
        queued = {},
        removed = {},
        settings = {
            showExpiryInInvetory = false
        },
        hiddenUnused = false,
        teleportText = nil,
        stairsText = nil,
        terminated = false,
        inventoryReloads = 0,
        unrelatedRuns = 0,
        originalInventorySetCalls = 0,
        passthroughSetCalls = 0
    }

    local idMap = {}
    local function widget(id)
        local value = { id = id, visible = true, enabled = true }
        function value:setId(newId)
            idMap[self.id] = nil
            self.id = newId
            idMap[newId] = self
        end
        function value:setChecked(checked) state.checked = checked end
        function value:setText(text)
            if self.id == 'showSpellGroupCooldowns' then state.cooldownText = text end
            if self.id == 'walkTeleportDelay' then state.teleportText = text end
            if self.id == 'walkStairsDelay' then state.stairsText = text end
        end
        function value:setTooltip(text) state.cooldownTooltip = text end
        function value:setVisible(visible)
            self.visible = visible
            if self.id == 'showExpiryOnUnusedItems' and not visible then state.hiddenUnused = true end
        end
        function value:setEnabled(enabled) self.enabled = enabled end
        idMap[id] = value
        return value
    end

    local legacyWidget = widget('showExpiryInInvetory')
    widget('showSpellGroupCooldowns')
    widget('showExpiryOnUnusedItems')
    widget('walkTeleportDelay')
    widget('walkStairsDelay')

    local interfacePanel = {}
    function interfacePanel:recursiveGetChildById(id) return idMap[id] end
    function interfacePanel:getChildren() return {} end
    local generalPanel = interfacePanel
    local hudPanel = { getChildren = function() return {} end }

    OptionsMigrationCore = Core
    modules = {
        game_inventory = {
            reloadInventory = function() state.inventoryReloads = state.inventoryReloads + 1 end
        }
    }
    panels = {
        interface = interfacePanel,
        generalPanel = generalPanel,
        interfaceHUD = hudPanel
    }
    tr = function(format, ...)
        if select('#', ...) > 0 then return string.format(format, ...) end
        return format
    end

    g_settings = {}
    function g_settings.getBoolean(key, default)
        local value = state.settings[key]
        if value == nil then return default end
        return value
    end
    function g_settings.set(key, value) state.settings[key] = value end

    local scheduleEventImplementation = function(eventCallback)
        state.nextEvent = state.nextEvent + 1
        state.queued[state.nextEvent] = eventCallback
        return state.nextEvent
    end
    local removeEventImplementation = function(handle) state.removed[handle] = true end
    scheduleEvent = scheduleEventImplementation
    removeEvent = removeEventImplementation

    getOption = function(key)
        if key == 'showExpiryInInvetory' then return true end
        if key == 'walkTeleportDelay' or key == 'walkStairsDelay' then return 50 end
        return nil
    end
    setOption = function(key)
        if Core.isInventoryExpiryKey(key) then
            state.originalInventorySetCalls = state.originalInventorySetCalls + 1
        else
            state.passthroughSetCalls = state.passthroughSetCalls + 1
        end
    end

    controller = {}
    function controller:onInit() return true end
    function controller:onTerminate()
        state.terminated = true
        return true
    end

    local loaded, loadError = pcall(dofile, sourceDir .. '/modules/client_options/options_phase0.lua')
    if not loaded then
        for _, name in ipairs(names) do rawset(_G, name, saved[name]) end
        error(loadError, 0)
    end

    local success, result = xpcall(function()
        callback(state, legacyWidget, idMap, scheduleEventImplementation, removeEventImplementation)
    end, debug.traceback)

    for _, name in ipairs(names) do rawset(_G, name, saved[name]) end
    if not success then error(result, 0) end
end

test('options adapter migrates legacy inventory expiry and normalizes loaded widgets', function()
    withAdapterHarness(function(state, legacyWidget, idMap, originalSchedule, originalRemove)
        assertTrue(controller:onInit())
        assertFalse(state.settings.showExpiryInInventory)
        assertFalse(state.settings.showExpiryInInvetory)
        assertFalse(getOption('showExpiryInInventory'))
        assertFalse(getOption('showExpiryInInvetory'))
        assertEqual('showExpiryInInventory', legacyWidget.id)
        assertEqual(legacyWidget, idMap.showExpiryInInventory)
        assertEqual('Show Cooldown Bar', state.cooldownText)
        assertTrue(state.cooldownTooltip ~= nil)
        assertTrue(state.hiddenUnused)
        assertEqual('Walk delay after teleport: 50ms', state.teleportText)
        assertEqual('Walk delay after floor change: 50ms', state.stairsText)
        assertEqual(originalSchedule, scheduleEvent)
        assertEqual(originalRemove, removeEvent)
    end)
end)

test('options adapter owns rapid inventory reloads without touching unrelated events', function()
    withAdapterHarness(function(state, _, _, originalSchedule, originalRemove)
        controller:onInit()

        local unrelatedEvent = scheduleEvent(function()
            state.unrelatedRuns = state.unrelatedRuns + 1
        end, 25)

        setOption('showExpiryInInventory', true, true)
        local firstInventoryEvent = state.nextEvent
        setOption('showExpiryInInvetory', false, true)
        local secondInventoryEvent = state.nextEvent

        assertEqual(0, state.originalInventorySetCalls)
        assertFalse(state.removed[unrelatedEvent] == true)
        assertTrue(state.removed[firstInventoryEvent])
        assertFalse(state.removed[secondInventoryEvent] == true)
        assertFalse(getOption('showExpiryInInventory'))
        assertFalse(getOption('showExpiryInInvetory'))
        assertFalse(state.settings.showExpiryInInventory)
        assertFalse(state.settings.showExpiryInInvetory)
        assertEqual(originalSchedule, scheduleEvent)
        assertEqual(originalRemove, removeEvent)

        state.queued[firstInventoryEvent]()
        assertEqual(0, state.inventoryReloads)

        state.queued[secondInventoryEvent]()
        assertEqual(1, state.inventoryReloads)

        state.queued[unrelatedEvent]()
        assertEqual(1, state.unrelatedRuns)
        removeEvent(unrelatedEvent)
        assertTrue(state.removed[unrelatedEvent])

        setOption('showExpiryInInventory', true, true)
        local terminationEvent = state.nextEvent
        controller:onTerminate()
        assertTrue(state.removed[terminationEvent])
        assertTrue(state.terminated)
    end)
end)

test('options adapter delegates unrelated options unchanged', function()
    withAdapterHarness(function(state)
        controller:onInit()
        setOption('showPing', true, true)
        assertEqual(1, state.passthroughSetCalls)
    end)
end)
