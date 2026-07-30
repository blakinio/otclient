local OptionsMigrationCore = rawget(_G, 'OptionsMigrationCore') or dofile('options_migration_core')

local canonicalKey = OptionsMigrationCore.CANONICAL_INVENTORY_EXPIRY_KEY
local legacyKey = OptionsMigrationCore.LEGACY_INVENTORY_EXPIRY_KEY
local originalSetOption = setOption
local originalGetOption = getOption
local originalScheduleEvent = scheduleEvent
local originalRemoveEvent = removeEvent
local originalControllerOnInit = controller.onInit
local originalControllerOnTerminate = controller.onTerminate
local inventoryExpiryValue = nil
local inventoryReloadEvent = nil
local inventoryReloadGeneration = 0

local function updateCanonicalWidget(value)
    for _, panel in pairs(panels or {}) do
        if panel and panel.recursiveGetChildById then
            local widget = panel:recursiveGetChildById(canonicalKey)
            if widget then
                widget:setChecked(value, true)
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
    inventoryReloadGeneration = inventoryReloadGeneration + 1
    if inventoryReloadEvent ~= nil then
        originalRemoveEvent(inventoryReloadEvent)
        inventoryReloadEvent = nil
    end
end

local function scheduleInventoryReload()
    cancelInventoryReload()

    local generation = inventoryReloadGeneration
    local handle = nil
    handle = originalScheduleEvent(function()
        if generation ~= inventoryReloadGeneration or inventoryReloadEvent ~= handle then
            return
        end

        inventoryReloadEvent = nil
        if modules and modules.game_inventory and modules.game_inventory.reloadInventory then
            modules.game_inventory.reloadInventory()
        end
    end, 100)
    inventoryReloadEvent = handle
end

local function setInventoryExpiry(value, force)
    value = value == true

    if not force and inventoryExpiryValue == value then
        persistInventoryExpiry(value)
        updateCanonicalWidget(value)
        return
    end

    inventoryExpiryValue = value
    persistInventoryExpiry(value)
    updateCanonicalWidget(value)
    scheduleInventoryReload()
end

local function hideUnsupportedWidget(widget)
    if not widget then
        return
    end
    widget:setVisible(false)
    widget:setEnabled(false)
end

local function hideUnsupportedPanel(panel)
    if not panel then
        return
    end
    panel:setVisible(false)
    panel:setHeight(0)
    panel:setMarginTop(0)
end

local function hideStatusBarPlaceholders(root)
    if not root or not root.getChildren then
        return
    end

    for _, child in pairs(root:getChildren()) do
        if child.getText then
            local text = child:getText()
            if text == tr('Show Customisable Status Bars') or text == tr('Show Status Bars') then
                hideUnsupportedPanel(child:getParent())
            end
        end
        hideStatusBarPlaceholders(child)
    end
end

local function configurePhase0Widgets()
    local interfacePanel = panels and panels.interface
    if interfacePanel then
        local legacyWidget = interfacePanel:recursiveGetChildById(legacyKey)
        if legacyWidget then
            legacyWidget:setId(canonicalKey)
        end

        local cooldownWidget = interfacePanel:recursiveGetChildById('showSpellGroupCooldowns')
        if cooldownWidget then
            cooldownWidget:setText(tr('Show Cooldown Bar'))
            cooldownWidget:setTooltip(tr('Show or hide the complete spell cooldown window'))
        end

        hideUnsupportedWidget(interfacePanel:recursiveGetChildById('showExpiryOnUnusedItems'))
    end

    local generalPanel = panels and panels.generalPanel
    if generalPanel then
        local teleportDelay = generalPanel:recursiveGetChildById('walkTeleportDelay')
        if teleportDelay then
            teleportDelay:setText(tr('Walk delay after teleport: %dms', getOption('walkTeleportDelay')))
        end

        local stairsDelay = generalPanel:recursiveGetChildById('walkStairsDelay')
        if stairsDelay then
            stairsDelay:setText(tr('Walk delay after floor change: %dms', getOption('walkStairsDelay')))
        end
    end

    hideStatusBarPlaceholders(panels and panels.interfaceHUD)
end

function setOption(key, value, force)
    if OptionsMigrationCore.isInventoryExpiryKey(key) then
        return setInventoryExpiry(value, force)
    end
    return originalSetOption(key, value, force)
end

function getOption(key)
    if OptionsMigrationCore.isInventoryExpiryKey(key) then
        if inventoryExpiryValue ~= nil then
            return inventoryExpiryValue
        end
        return originalGetOption(legacyKey)
    end
    return originalGetOption(key)
end

function controller:onInit(...)
    local legacyValue = g_settings.getBoolean(legacyKey, true)
    local canonicalValue = g_settings.getBoolean(canonicalKey, legacyValue)
    inventoryExpiryValue = OptionsMigrationCore.resolveInventoryExpiryValue(canonicalValue, legacyValue, true)
    persistInventoryExpiry(inventoryExpiryValue)

    local result = originalControllerOnInit(self, ...)
    configurePhase0Widgets()
    updateCanonicalWidget(inventoryExpiryValue)
    return result
end

function controller:onTerminate(...)
    cancelInventoryReload()
    return originalControllerOnTerminate(self, ...)
end
