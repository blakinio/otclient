local sourceDir = assert(os.getenv('OTCLIENT_SOURCE_DIR'), 'OTCLIENT_SOURCE_DIR is required')
local Core = dofile(sourceDir .. '/modules/client_entergame/characterlist_lifecycle_core.lua')

local function withHarness(callback)
    local names = {
        'CharacterList',
        'CharacterListLifecycleCore',
        'EnterGame',
        'G',
        'g_game',
        'g_logger',
        'g_resources'
    }
    local saved = {}
    for _, name in ipairs(names) do
        saved[name] = rawget(_G, name)
    end

    local state = {
        createPaths = {},
        enterGameShows = 0,
        errors = {},
        originalShowAgainCalls = 0,
        windowExists = false,
        missingLayouts = {}
    }

    CharacterList = {}
    function CharacterList.create(_, _, layoutPath)
        state.windowExists = true
        state.createPaths[#state.createPaths + 1] = layoutPath
    end
    function CharacterList.destroy()
        CharacterList.hide(true)
        state.windowExists = false
    end
    function CharacterList.hide()
        if not state.windowExists then
            error('attempted to hide a missing character list')
        end
    end
    function CharacterList.showAgain()
        if not state.windowExists then
            error('attempted to show a missing character list')
        end
        state.originalShowAgainCalls = state.originalShowAgainCalls + 1
    end

    CharacterListLifecycleCore = Core
    EnterGame = {
        show = function()
            state.enterGameShows = state.enterGameShows + 1
        end
    }
    G = {
        characters = { { name = 'Tester' } },
        characterAccount = {}
    }
    g_game = {
        isOnline = function()
            return false
        end
    }
    g_logger = {
        error = function(message)
            state.errors[#state.errors + 1] = message
        end
    }
    g_resources = {
        guessFilePath = function(path, extension)
            if path:sub(-(extension:len() + 1)) == '.' .. extension then
                return path
            end
            return path .. '.' .. extension
        end,
        fileExists = function(path)
            return not state.missingLayouts[path]
        end
    }

    local loadSuccess, loadError = pcall(dofile, sourceDir .. '/modules/client_entergame/characterlist_lifecycle.lua')
    if not loadSuccess then
        for _, name in ipairs(names) do
            rawset(_G, name, saved[name])
        end
        error(loadError, 0)
    end

    local success, result = xpcall(function()
        callback(state)
    end, debug.traceback)

    for _, name in ipairs(names) do
        rawset(_G, name, saved[name])
    end

    if not success then
        error(result, 0)
    end
end

test('character list adapter recreates the legacy layout after destroy', function()
    withHarness(function(state)
        assertTrue(CharacterList.create(G.characters, G.characterAccount))
        assertEqual('/client_entergame/characterlist.otui', state.createPaths[1])
        assertTrue(CharacterList.destroy())
        assertTrue(CharacterList.showAgain())
        assertEqual(2, #state.createPaths)
        assertEqual('/client_entergame/characterlist.otui', state.createPaths[2])
        assertEqual(1, state.originalShowAgainCalls)
    end)
end)

test('character list adapter retains the Oteryn layout for recreation', function()
    withHarness(function(state)
        assertTrue(CharacterList.create(G.characters, G.characterAccount, 'oteryn_characterlist'))
        assertTrue(CharacterList.destroy())
        assertTrue(CharacterList.showAgain())
        assertEqual('/client_entergame/oteryn_characterlist.otui', state.createPaths[1])
        assertEqual('/client_entergame/oteryn_characterlist.otui', state.createPaths[2])
    end)
end)

test('character list adapter restores EnterGame when the layout is missing', function()
    withHarness(function(state)
        state.missingLayouts['/client_entergame/characterlist.otui'] = true
        assertFalse(CharacterList.create(G.characters, G.characterAccount))
        assertTrue(state.enterGameShows > 0)
        assertTrue(#state.errors > 0)
        assertEqual(0, #state.createPaths)
    end)
end)
