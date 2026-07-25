local sourceDir = assert(os.getenv('OTCLIENT_SOURCE_DIR'), 'OTCLIENT_SOURCE_DIR is required')
local Core = dofile(sourceDir .. '/modules/game_actionbar/cooldown_lifecycle_core.lua')

test('cooldown lifecycle begins and ends isolated sessions', function()
    local state = Core.newSessionState()
    local spells = { [10] = { startTime = 1, exhaustion = 100 } }
    local groups = { [2] = { startTime = 1, exhaustion = 200 } }

    assertTrue(Core.beginSession(state, spells, groups))
    assertTrue(state.active)
    assertEqual(1, state.generation)
    assertNil(spells[10])
    assertNil(groups[2])

    Core.recordCooldown(spells, 10, 500, 1000)
    assertFalse(Core.beginSession(state, spells, groups))
    assertNotNil(spells[10])

    Core.endSession(state, spells, groups)
    assertFalse(state.active)
    assertNil(spells[10])
end)

test('cooldown lifecycle records protocol state independently from rendering', function()
    local cache = {}
    assertFalse(Core.shouldRender(false, false))
    assertTrue(Core.recordCooldown(cache, 42, 1500, 10000))
    assertEqual(1500, cache[42].exhaustion)
    assertEqual(10000, cache[42].startTime)

    assertFalse(Core.recordCooldown(cache, 42, 0, 11000))
    assertNil(cache[42])
end)

test('cooldown lifecycle uses the longest individual or group remaining time', function()
    local spells = {
        [100] = { startTime = 1000, exhaustion = 2500 }
    }
    local groups = {
        [1] = { startTime = 1200, exhaustion = 1000 },
        [2] = { startTime = 1000, exhaustion = 4000 }
    }

    assertEqual(3000, Core.getMaxRemaining(spells, groups, 100, { 1, 2 }, 2000))
    assertEqual(1500, Core.getMaxRemaining(spells, groups, 100, { 1 }, 2000))
    assertEqual(0, Core.getMaxRemaining(spells, groups, 100, { 1, 2 }, 6000))
end)

test('cooldown lifecycle preserves packets received before deferred UI setup', function()
    local state = Core.newSessionState()
    local spells = {}
    local groups = {}

    assertTrue(Core.ensureSession(state, spells, groups))
    Core.recordCooldown(groups, 7, 3000, 1000)

    assertFalse(Core.beginSession(state, spells, groups))
    assertEqual(2500, Core.getMaxRemaining(spells, groups, nil, { 7 }, 1500))
end)

test('cooldown lifecycle cache copies are independent from later reset', function()
    local cache = {
        [4] = { startTime = 10, exhaustion = 20 }
    }
    local copy = Core.copyCache(cache)
    Core.endSession(Core.newSessionState(), cache, {})

    assertNil(cache[4])
    assertEqual(20, copy[4].exhaustion)
    assertEqual(10, copy[4].startTime)
end)
