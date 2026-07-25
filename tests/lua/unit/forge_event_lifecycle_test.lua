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
    assertEqual(2, #registry.retiredCallbacks)
end)

test('Forge event registry retains manually removed callback references', function()
    local registry = Core.newRegistry()
    local generation = Core.beginGeneration(registry)
    local callback = function() end

    Core.track(registry, 'manual', generation, callback)
    local entry = Core.retire(registry, 'manual')

    assertEqual(callback, entry.callback)
    assertEqual(1, #registry.retiredCallbacks)
    assertEqual(callback, registry.retiredCallbacks[1])
end)
