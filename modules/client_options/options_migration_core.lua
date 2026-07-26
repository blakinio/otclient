local OptionsMigrationCore = {}

OptionsMigrationCore.CANONICAL_INVENTORY_EXPIRY_KEY = 'showExpiryInInventory'
OptionsMigrationCore.LEGACY_INVENTORY_EXPIRY_KEY = 'showExpiryInInvetory'

function OptionsMigrationCore.resolveInventoryExpiryValue(canonicalValue, legacyValue, defaultValue)
    if canonicalValue ~= nil then
        return canonicalValue == true
    end
    if legacyValue ~= nil then
        return legacyValue == true
    end
    return defaultValue == true
end

function OptionsMigrationCore.isInventoryExpiryKey(key)
    return key == OptionsMigrationCore.CANONICAL_INVENTORY_EXPIRY_KEY or
        key == OptionsMigrationCore.LEGACY_INVENTORY_EXPIRY_KEY
end

return OptionsMigrationCore
