local ConvictionIndices = {
    SPECIAL_1 = 1,
    SPECIAL_2 = 2,
    SPECIAL_3 = 3,
    SPECIAL_4 = 4,
    SKILL = 5,
    LIFE_LEECH = 6,
    MANA_LEECH = 7,
    SPELL_1 = 8,
    SPELL_2 = 9,
    SPELL_3 = 10,
    SPELL_4 = 11,
    SPELL_5 = 12,
    VESSEL_1 = 13,
    VESSEL_2 = 14,
    VESSEL_3 = 15,
    VESSEL_4 = 16
}

function ConvictionIndices.buildSummaryView(convictions)
    local source = type(convictions) == 'table' and convictions or {}
    return {
        [1] = source[ConvictionIndices.SPECIAL_1],
        [2] = source[ConvictionIndices.SPECIAL_2],
        [3] = source[ConvictionIndices.SKILL],
        [4] = source[ConvictionIndices.LIFE_LEECH],
        [5] = source[ConvictionIndices.MANA_LEECH],
        [6] = source[ConvictionIndices.SPELL_1],
        [7] = source[ConvictionIndices.SPELL_2],
        [8] = source[ConvictionIndices.SPELL_3],
        [9] = source[ConvictionIndices.SPELL_4],
        [10] = source[ConvictionIndices.SPELL_5]
    }
end

if WheelOfDestiny and WheelOfDestiny.configureSummary and getConvictionPerks then
    local originalConfigureSummary = WheelOfDestiny.configureSummary

    function WheelOfDestiny.configureSummary(...)
        local originalGetConvictionPerks = getConvictionPerks
        getConvictionPerks = function()
            return ConvictionIndices.buildSummaryView(originalGetConvictionPerks())
        end

        local arguments = { ... }
        local success, result = xpcall(function()
            return originalConfigureSummary(unpack(arguments))
        end, debug.traceback)

        getConvictionPerks = originalGetConvictionPerks
        if not success then
            error(result, 0)
        end
        return result
    end
end

return ConvictionIndices
