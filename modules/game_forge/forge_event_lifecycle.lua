local ForgeEventLifecycleCore = rawget(_G, 'ForgeEventLifecycleCore') or dofile('forge_event_lifecycle_core')

local originalScheduleEvent = scheduleEvent
local originalRemoveEvent = removeEvent
local originalShow = ForgeController.show
local originalHide = ForgeController.hide
local originalOnGameStart = ForgeController.onGameStart
local originalOnGameEnd = ForgeController.onGameEnd
local originalTerminate = ForgeController.terminate

local registry = ForgeEventLifecycleCore.newRegistry()

local function ensureGeneration()
    return ForgeEventLifecycleCore.beginGeneration(registry)
end

local function cancelPendingEvents()
    local cancelled = ForgeEventLifecycleCore.cancelAll(registry, originalRemoveEvent)
    ForgeController.resultTimeout = nil
    return cancelled
end

function scheduleEvent(callback, delay)
    if type(callback) ~= 'function' then
        return originalScheduleEvent(callback, delay)
    end

    local generation = ensureGeneration()
    local handle = nil
    local wrappedCallback = function(...)
        ForgeEventLifecycleCore.take(registry, handle)
        if not ForgeEventLifecycleCore.isCurrent(registry, generation) then
            return
        end
        return callback(...)
    end

    handle = originalScheduleEvent(wrappedCallback, delay)
    if handle ~= nil then
        ForgeEventLifecycleCore.track(registry, handle, generation, wrappedCallback)
    end
    return handle
end

function removeEvent(handle)
    ForgeEventLifecycleCore.retire(registry, handle)
    return originalRemoveEvent(handle)
end

function ForgeController:show(...)
    ensureGeneration()
    return originalShow(self, ...)
end

function ForgeController:hide(...)
    cancelPendingEvents()
    return originalHide(self, ...)
end

function ForgeController:onGameStart(...)
    cancelPendingEvents()
    ensureGeneration()
    return originalOnGameStart(self, ...)
end

function ForgeController:onGameEnd(...)
    cancelPendingEvents()
    if originalOnGameEnd then
        return originalOnGameEnd(self, ...)
    end
end

function ForgeController:terminate(...)
    cancelPendingEvents()
    return originalTerminate(self, ...)
end
