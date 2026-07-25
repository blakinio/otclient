local sourceDir = assert(os.getenv('OTCLIENT_SOURCE_DIR'), 'OTCLIENT_SOURCE_DIR is required')
local Core = dofile(sourceDir .. '/modules/game_forge/forge_event_lifecycle_core.lua')

local function withHarness(callback)
    local names = {
        'ForgeController',
        'ForgeEventLifecycleCore',
        'removeEvent',
        'scheduleEvent'
    }
    local saved = {}
    for _, name in ipairs(names) do saved[name] = rawget(_G, name) end

    local state = {
        callbacks = {},
        executed = 0,
        nextHandle = 0,
        removed = {},
        terminated = false
    }

    scheduleEvent = function(eventCallback)
        state.nextHandle = state.nextHandle + 1
        state.callbacks[state.nextHandle] = eventCallback
        return state.nextHandle
    end
    removeEvent = function(handle)
        state.removed[handle] = true
    end

    ForgeEventLifecycleCore = Core
    ForgeController = {
        callbacks = {},
        resultTimeout = nil
    }
    function ForgeController:show() end
    function ForgeController:hide() end
    function ForgeController:onGameStart()
        self.callbacks.pending = function()
            state.executed = state.executed + 1
        end
        self.resultTimeout = scheduleEvent(self.callbacks.pending, 5000)
    end
    function ForgeController:onGameEnd() end
    function ForgeController:terminate()
        self:hide()
        self.callbacks = {}
        state.terminated = true
    end

    local loadSuccess, loadError = pcall(dofile, sourceDir .. '/modules/game_forge/forge_event_lifecycle.lua')
    if not loadSuccess then
        for _, name in ipairs(names) do rawset(_G, name, saved[name]) end
        error(loadError, 0)
    end

    local success, result = xpcall(function()
        callback(state)
    end, debug.traceback)

    for _, name in ipairs(names) do rawset(_G, name, saved[name]) end
    if not success then error(result, 0) end
end

test('Forge adapter cancels pending callbacks before hide and ignores queue races', function()
    withHarness(function(state)
        ForgeController:onGameStart()
        local handle = ForgeController.resultTimeout
        local queuedCallback = state.callbacks[handle]

        ForgeController:hide()
        assertTrue(state.removed[handle])
        assertNil(ForgeController.resultTimeout)

        queuedCallback()
        assertEqual(0, state.executed)
    end)
end)

test('Forge adapter releases naturally completed handles from cancellation', function()
    withHarness(function(state)
        ForgeController:onGameStart()
        local handle = ForgeController.resultTimeout
        state.callbacks[handle]()
        assertEqual(1, state.executed)

        ForgeController:terminate()
        assertTrue(state.terminated)
        assertFalse(state.removed[handle] == true)
    end)
end)

test('Forge adapter keeps new generations independent from stale callbacks', function()
    withHarness(function(state)
        ForgeController:onGameStart()
        local oldHandle = ForgeController.resultTimeout
        local oldCallback = state.callbacks[oldHandle]

        ForgeController:hide()
        ForgeController:show()
        local newHandle = scheduleEvent(function()
            state.executed = state.executed + 10
        end, 100)
        local newCallback = state.callbacks[newHandle]

        oldCallback()
        newCallback()
        assertEqual(10, state.executed)
    end)
end)

test('Forge adapter tracks manual event removal', function()
    withHarness(function(state)
        ForgeController:show()
        local handle = scheduleEvent(function()
            state.executed = state.executed + 1
        end, 100)

        removeEvent(handle)
        assertTrue(state.removed[handle])
        ForgeController:terminate()
        assertEqual(0, state.executed)
    end)
end)
