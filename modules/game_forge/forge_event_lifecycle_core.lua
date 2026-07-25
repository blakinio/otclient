local ForgeEventLifecycleCore = {}

function ForgeEventLifecycleCore.newRegistry()
    return {
        active = false,
        generation = 0,
        handles = {},
        retiredCallbacks = {}
    }
end

function ForgeEventLifecycleCore.beginGeneration(registry)
    if type(registry) ~= 'table' then
        return nil
    end
    if registry.active then
        return registry.generation
    end

    registry.generation = (tonumber(registry.generation) or 0) + 1
    registry.active = true
    return registry.generation
end

function ForgeEventLifecycleCore.invalidate(registry)
    if type(registry) ~= 'table' then
        return
    end
    registry.generation = (tonumber(registry.generation) or 0) + 1
    registry.active = false
end

function ForgeEventLifecycleCore.track(registry, handle, generation, callback)
    if type(registry) ~= 'table' or handle == nil or type(callback) ~= 'function' then
        return false
    end

    registry.handles[handle] = {
        generation = generation,
        callback = callback
    }
    return true
end

function ForgeEventLifecycleCore.take(registry, handle)
    if type(registry) ~= 'table' or handle == nil then
        return nil
    end
    local entry = registry.handles[handle]
    registry.handles[handle] = nil
    return entry
end

function ForgeEventLifecycleCore.retire(registry, handle)
    local entry = ForgeEventLifecycleCore.take(registry, handle)
    if entry and entry.callback then
        registry.retiredCallbacks[#registry.retiredCallbacks + 1] = entry.callback
    end
    return entry
end

function ForgeEventLifecycleCore.isCurrent(registry, generation)
    return type(registry) == 'table' and registry.active and registry.generation == generation
end

function ForgeEventLifecycleCore.cancelAll(registry, removeCallback)
    if type(registry) ~= 'table' then
        return 0
    end

    local cancelled = 0
    for handle, entry in pairs(registry.handles) do
        if type(removeCallback) == 'function' then
            pcall(removeCallback, handle)
        end
        if entry.callback then
            registry.retiredCallbacks[#registry.retiredCallbacks + 1] = entry.callback
        end
        registry.handles[handle] = nil
        cancelled = cancelled + 1
    end

    ForgeEventLifecycleCore.invalidate(registry)
    return cancelled
end

function ForgeEventLifecycleCore.pendingCount(registry)
    if type(registry) ~= 'table' then
        return 0
    end
    local count = 0
    for _ in pairs(registry.handles) do count = count + 1 end
    return count
end

return ForgeEventLifecycleCore
