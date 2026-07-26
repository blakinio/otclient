local sourceDir = assert(os.getenv('OTCLIENT_SOURCE_DIR'), 'OTCLIENT_SOURCE_DIR is required')
local path = sourceDir .. '/modules/game_wheel/classes/conviction_indices.lua'
local Indices = dofile(path)

test('Wheel conviction indices match the parser order', function()
    assertEqual(1, Indices.SPECIAL_1)
    assertEqual(4, Indices.SPECIAL_4)
    assertEqual(5, Indices.SKILL)
    assertEqual(6, Indices.LIFE_LEECH)
    assertEqual(7, Indices.MANA_LEECH)
    assertEqual(8, Indices.SPELL_1)
    assertEqual(12, Indices.SPELL_5)
    assertEqual(13, Indices.VESSEL_1)
    assertEqual(16, Indices.VESSEL_4)
end)

test('Wheel conviction summary view skips reserved special slots three and four', function()
    local source = {}
    for index = 1, 16 do
        source[index] = 'slot-' .. index
    end

    local summary = Indices.buildSummaryView(source)
    assertEqual('slot-1', summary[1])
    assertEqual('slot-2', summary[2])
    assertEqual('slot-5', summary[3])
    assertEqual('slot-6', summary[4])
    assertEqual('slot-7', summary[5])
    assertEqual('slot-8', summary[6])
    assertEqual('slot-12', summary[10])
    assertEqual(10, #summary)
end)

test('Wheel summary adapter scopes the remap to configureSummary', function()
    local savedWheel = rawget(_G, 'WheelOfDestiny')
    local savedGetter = rawget(_G, 'getConvictionPerks')
    local captured = nil
    local source = {}
    for index = 1, 16 do source[index] = { slot = index } end

    WheelOfDestiny = {
        configureSummary = function()
            captured = getConvictionPerks()
        end
    }
    getConvictionPerks = function() return source end

    local success, result = xpcall(function()
        dofile(path)
        WheelOfDestiny.configureSummary()
        assertEqual(5, captured[3].slot)
        assertEqual(6, captured[4].slot)
        assertEqual(7, captured[5].slot)
        assertEqual(12, captured[10].slot)
        assertEqual(source, getConvictionPerks())
    end, debug.traceback)

    WheelOfDestiny = savedWheel
    getConvictionPerks = savedGetter
    if not success then error(result, 0) end
end)
