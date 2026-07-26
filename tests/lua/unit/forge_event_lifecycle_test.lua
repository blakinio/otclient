local sourceDir = assert(os.getenv('OTCLIENT_SOURCE_DIR'), 'OTCLIENT_SOURCE_DIR is required')
local Core = dofile(sourceDir .. '/modules/game_forge/forge_event_lifecycle_core.lua')

test('Forge event registry tracks and completes callbacks', function()
    local registry = Core.newRegistry()
    local generation = Core.beginGeneration(registry)
    local callback = function() end

    assertTrue(Core.track(registry, 'event-1', generation, callback))
    assertEqual(1, Core.pendingCount(registry))
    local entry = Core.take(registry, 'event-1')
    assertEqual(callback, entry.callback)
    assertEqual(generation, entry.generation)
    assertEqual(0, Core.pendingCount(registry))
end)

test('Forge event registry invalidates stale generations', function()
    local registry = Core.newRegistry()
    local first = Core.beginGeneration(registry)
    assertTrue(Core.isCurrent(registry, first))

    Core.invalidate(registry)
    assertFalse(Core.isCurrent(registry, first))

    local second = Core.beginGeneration(registry)
    assertTrue(second > first)
    assertTrue(Core.isCurrent(registry, second))
end)

test('Forge event registry cancels every pending handle before teardown', function()
    local registry = Core.newRegistry()
    local generation = Core.beginGeneration(registry)
    local removed = {}
    local first = function() end
    local second = function() end

    Core.track(registry, 10, generation, first)
    Core.track(registry, 20, generation, second)
    local cancelled = Core.cancelAll(registry, function(handle)
        removed[handle] = true
    end)

    assertEqual(2, cancelled)
    assertTrue(removed[10])
    assertTrue(removed[20])
    assertEqual(0, Core.pendingCount(registry))
    assertFalse(registry.active)
    assertNil(registry.retiredCallbacks)
end)

test('Forge event registry releases manually removed callback references', function()
    local registry = Core.newRegistry()
    local generation = Core.beginGeneration(registry)
    local callback = function() end

    Core.track(registry, 'manual', generation, callback)
    assertTrue(Core.retire(registry, 'manual'))
    assertFalse(Core.retire(registry, 'manual'))
    assertEqual(0, Core.pendingCount(registry))
    assertNil(registry.retiredCallbacks)
end)

test('Forge event registry does not accumulate callbacks across lifecycle cycles', function()
    local registry = Core.newRegistry()
    local removed = 0

    for cycle = 1, 100 do
        local generation = Core.beginGeneration(registry)
        Core.track(registry, cycle, generation, function() end)
        assertEqual(1, Core.cancelAll(registry, function()
            removed = removed + 1
        end))
        assertEqual(0, Core.pendingCount(registry))
        assertNil(registry.retiredCallbacks)
    end

    assertEqual(100, removed)
end)
