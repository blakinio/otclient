local sourceDir = assert(os.getenv('OTCLIENT_SOURCE_DIR'), 'OTCLIENT_SOURCE_DIR is required')
local Core = dofile(sourceDir .. '/modules/client_entergame/characterlist_lifecycle_core.lua')

local resources = {}
function resources.guessFilePath(path, extension)
    if path:sub(-(extension:len() + 1)) == '.' .. extension then
        return path
    end
    return path .. '.' .. extension
end

local rootResolvingResources = {}
function rootResolvingResources.guessFilePath(path, extension)
    if path:sub(-(extension:len() + 1)) == '.' .. extension then
        return '/' .. path:gsub('^/+', '')
    end
    return '/' .. path:gsub('^/+', '') .. '.' .. extension
end

test('character list lifecycle resolves the default layout inside its module', function()
    local path, err = Core.normalizeLayoutPath(resources)
    assertNil(err)
    assertEqual('/client_entergame/characterlist.otui', path)
end)

test('character list lifecycle anchors relative names when resolver returns a root path', function()
    local path, err = Core.normalizeLayoutPath(rootResolvingResources, 'characterlist')
    assertNil(err)
    assertEqual('/client_entergame/characterlist.otui', path)

    local oterynPath, oterynError = Core.normalizeLayoutPath(rootResolvingResources, 'oteryn_characterlist.otui')
    assertNil(oterynError)
    assertEqual('/client_entergame/oteryn_characterlist.otui', oterynPath)
end)

test('character list lifecycle resolves custom legacy and Oteryn layout names', function()
    local legacyPath, legacyError = Core.normalizeLayoutPath(resources, 'characterlist.otui')
    assertNil(legacyError)
    assertEqual('/client_entergame/characterlist.otui', legacyPath)

    local oterynPath, oterynError = Core.normalizeLayoutPath(resources, 'oteryn_characterlist')
    assertNil(oterynError)
    assertEqual('/client_entergame/oteryn_characterlist.otui', oterynPath)
end)

test('character list lifecycle preserves explicit absolute layouts', function()
    local path, err = Core.normalizeLayoutPath(resources, '/client_entergame/oteryn_characterlist.otui')
    assertNil(err)
    assertEqual('/client_entergame/oteryn_characterlist.otui', path)
end)

test('character list lifecycle rejects relative traversal', function()
    local path, err = Core.normalizeLayoutPath(resources, '../characterlist')
    assertNil(path)
    assertEqual('invalid_layout', err)
end)

test('character list lifecycle recreates only missing windows with retained login data', function()
    assertTrue(Core.shouldRecreate(false, {}, {}))
    assertFalse(Core.shouldRecreate(true, {}, {}))
    assertFalse(Core.shouldRecreate(false, nil, {}))
    assertFalse(Core.shouldRecreate(false, {}, nil))
end)