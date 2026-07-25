local CooldownLifecycleCore = {}

local function clearTable(values)
    if type(values) ~= 'table' then
        return
    end
    for key in pairs(values) do
        values[key] = nil
    end
end

function CooldownLifecycleCore.newSessionState()
    return {
        active = false,
        generation = 0
    }
end

function CooldownLifecycleCore.beginSession(state, spellCache, groupCache)
    if type(state) ~= 'table' then
        return false
    end
    if state.active then
        return false
    end

    clearTable(spellCache)
    clearTable(groupCache)
    state.active = true
    state.generation = (tonumber(state.generation) or 0) + 1
    return true
end

function CooldownLifecycleCore.ensureSession(state, spellCache, groupCache)
    if type(state) ~= 'table' then
        return false
    end
    if state.active then
        return true
    end
    CooldownLifecycleCore.beginSession(state, spellCache, groupCache)
    return state.active
end

function CooldownLifecycleCore.endSession(state, spellCache, groupCache)
    clearTable(spellCache)
    clearTable(groupCache)
    if type(state) == 'table' then
        state.active = false
    end
end

function CooldownLifecycleCore.recordCooldown(cache, key, delay, startTime)
    if type(cache) ~= 'table' or key == nil then
        return false
    end

    local normalizedDelay = tonumber(delay)
    local normalizedStart = tonumber(startTime)
    if not normalizedDelay or normalizedDelay <= 0 or not normalizedStart then
        cache[key] = nil
        return false
    end

    cache[key] = {
        exhaustion = normalizedDelay,
        startTime = normalizedStart
    }
    return true
end

function CooldownLifecycleCore.getRemaining(cooldown, now)
    if type(cooldown) ~= 'table' then
        return 0
    end

    local startTime = tonumber(cooldown.startTime)
    local exhaustion = tonumber(cooldown.exhaustion)
    local currentTime = tonumber(now)
    if not startTime or not exhaustion or not currentTime then
        return 0
    end

    local remaining = startTime + exhaustion - currentTime
    return remaining > 0 and remaining or 0
end

function CooldownLifecycleCore.getMaxRemaining(spellCache, groupCache, spellId, groupIds, now)
    local maximum = 0

    if type(spellCache) == 'table' and spellId ~= nil then
        maximum = CooldownLifecycleCore.getRemaining(spellCache[spellId], now)
    end

    if type(groupCache) == 'table' and type(groupIds) == 'table' then
        for _, groupId in pairs(groupIds) do
            local remaining = CooldownLifecycleCore.getRemaining(groupCache[groupId], now)
            if remaining > maximum then
                maximum = remaining
            end
        end
    end

    return maximum
end

function CooldownLifecycleCore.copyCache(cache)
    local copy = {}
    if type(cache) ~= 'table' then
        return copy
    end

    for key, cooldown in pairs(cache) do
        if type(cooldown) == 'table' then
            copy[key] = {
                exhaustion = cooldown.exhaustion,
                startTime = cooldown.startTime
            }
        end
    end
    return copy
end

function CooldownLifecycleCore.shouldRender(showProgress, showTime)
    return showProgress == true or showTime == true
end

return CooldownLifecycleCore
