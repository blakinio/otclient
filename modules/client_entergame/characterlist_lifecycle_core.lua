local CharacterListLifecycleCore = {}

local MODULE_UI_ROOT = '/client_entergame/'
local DEFAULT_LAYOUT = 'characterlist'

local function isNonEmptyString(value)
    return type(value) == 'string' and value ~= ''
end

function CharacterListLifecycleCore.normalizeLayoutPath(resources, layoutName)
    if resources == nil or type(resources.guessFilePath) ~= 'function' then
        return nil, 'invalid_resources'
    end

    local requestedLayout = isNonEmptyString(layoutName) and layoutName or DEFAULT_LAYOUT
    local success, layoutPath = pcall(resources.guessFilePath, requestedLayout, 'otui')
    if not success or not isNonEmptyString(layoutPath) then
        return nil, 'invalid_layout'
    end

    layoutPath = layoutPath:gsub('\\', '/')
    if layoutPath:sub(1, 1) == '/' then
        return layoutPath
    end

    while layoutPath:sub(1, 2) == './' do
        layoutPath = layoutPath:sub(3)
    end

    if layoutPath == '..' or layoutPath:sub(1, 3) == '../' or layoutPath:find('/../', 1, true) then
        return nil, 'invalid_layout'
    end

    return MODULE_UI_ROOT .. layoutPath
end

function CharacterListLifecycleCore.shouldRecreate(isCreated, characters, account)
    return not isCreated and type(characters) == 'table' and account ~= nil
end

return CharacterListLifecycleCore
