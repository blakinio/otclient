local OptionsMigrationCore = rawget(_G, 'OptionsMigrationCore') or dofile('options_migration_core')

local canonicalKey = OptionsMigrationCore.CANONICAL_INVENTORY_EXPIRY_KEY
local legacyKey = OptionsMigrationCore.LEGACY_INVENTORY_EXPIRY_KEY
local originalSetOption = setOption
local originalGetOption = getOption
local originalScheduleEvent = scheduleEvent
local originalRemoveEvent = removeEvent
local originalControllerOnInit = controller.onInit
local originalControllerOnTerminate = controller.onTerminate
local inventoryReloadEvent = nil

local function updateCanonicalWidget(value)
    for _, panel in pairs(panels or {}) do
        if panel and panel.recursiveGetChildById then
            local widget = panel:recursiveGetChildById(canonicalKey)
            if widget then
                widget:setChecked(value)
                return
            end
        end
    end
end

local function persistInventoryExpiry(value)
    g_settings.set(canonicalKey, value)
    g_settings.set(legacyKey, value)
end

local function cancelInventoryReload()
    if inventoryReloadEvent ~= nil then
        originalRemoveEvent(inventoryReloadEvent)
        inventoryReloadEvent = nil
    end
end

local function setInventoryExpiry(value, force)
    value = value == true

    if not force and originalGetOption(legacyKey) == value then
        persistInventoryExpiry(value)
        updateCanonicalWidget(value)
        return
    end

    local alreadyRemoved = {}
    if inventoryReloadEvent ~= nil then
        local oldEvent = inventoryReloadEvent
        cancelInventoryReload()
        alreadyRemoved[oldEvent] = true
    end

    local previousScheduleEvent = scheduleEvent
    local previousRemoveEvent = removeEvent
    local capturedEvent = nil

    scheduleEvent = function(callback, delay)
        local handle = nil
        local wrappedCallback = function(...)
            if inventoryReloadEvent == handle then
                inventoryReloadEvent = nil
            end
            return callback(...)
        end
        handle = originalScheduleEvent(wrappedCallback, delay)
        capturedEvent = handle
        return handle
    end

    removeEvent = function(handle)
        if handle ~= nil and not alreadyRemoved[handle] then
            return originalRemoveEvent(handle)
        end
    end

    local success, result = xpcall(function()
        return originalSetOption(legacyKey, value, force)
    end, debug.traceback)

    scheduleEvent = previousScheduleEvent
    removeEvent = previousRemoveEvent
    inventoryReloadEvent = capturedEvent
    persistInventoryExpiry(value)
    updateCanonicalWidget(value)

    if not success then
        error(result, 0)
    end
    return result
end

function setOption(key, value, force)
    if OptionsMigrationCore.isInventoryExpiryKey(key) then
        return setInventoryExpiry(value, force)
    end
    return originalSetOption(key, value, force)
end

function getOption(key)
    if key == canonicalKey then
        return originalGetOption(legacyKey)
    end
    return originalGetOption(key)
end

function controller:onInit(...)
    local legacyValue = g_settings.getBoolean(legacyKey, true)
    local canonicalValue = g_settings.getBoolean(canonicalKey, legacyValue)
    local migratedValue = OptionsMigrationCore.resolveInventoryExpiryValue(canonicalValue, legacyValue, true)
    persistInventoryExpiry(migratedValue)

    local result = originalControllerOnInit(self, ...)
    updateCanonicalWidget(migratedValue)
    return result
end

function controller:onTerminate(...)
    cancelInventoryReload()
    return originalControllerOnTerminate(self, ...)
end
