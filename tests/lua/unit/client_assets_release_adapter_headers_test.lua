local sourceDir = assert(os.getenv('OTCLIENT_SOURCE_DIR'), 'OTCLIENT_SOURCE_DIR is required')
local Selector = dofile(sourceDir .. '/modules/client_assets/client_assets_release_selector.lua')

local function cloneAsset(digest)
    return {
        name = 'v15.25-client.zip',
        browser_download_url = 'https://example.invalid/client.zip',
        digest = digest
    }
end

local function releaseWithDigest(digest)
    return {
        {
            tag_name = 'v15.25.0a00a0',
            name = '15.25',
            assets = { cloneAsset(digest) }
        }
    }
end

local function withHarness(releases, callback)
    local savedAdapter = rawget(_G, 'ClientAssetsReleaseAdapter')
    local savedSelector = rawget(_G, 'ClientAssetsReleaseSelector')
    local savedHTTP = rawget(_G, 'HTTP')
    local savedServices = rawget(_G, 'Services')
    local savedResources = rawget(_G, 'g_resources')
    local savedCrypt = rawget(_G, 'g_crypt')
    local savedLogger = rawget(_G, 'g_logger')
    local state = {
        activeHeaders = {},
        headerAdds = 0,
        headerRemoves = 0,
        downloads = 0,
        logs = {}
    }

    ClientAssetsReleaseSelector = Selector
    Services = { clientAssets = { repository = 'dudantas/tibia-client' } }
    HTTP = {
        addCustomHeader = function(headers)
            state.headerAdds = state.headerAdds + 1
            for name, value in pairs(headers) do
                state.activeHeaders[name] = value
            end
        end,
        removeCustomHeader = function(name)
            state.headerRemoves = state.headerRemoves + 1
            state.activeHeaders[name] = nil
        end
    }
    HTTP.getJSON = function(_, responseCallback)
        state.requestHeaders = {}
        for name, value in pairs(state.activeHeaders) do
            state.requestHeaders[name] = value
        end
        state.pendingResponse = responseCallback
        return 'get-operation'
    end
    HTTP.download = function(_, path, responseCallback)
        state.downloads = state.downloads + 1
        responseCallback(path, 'transport-checksum', nil)
        return 'download-operation'
    end
    g_resources = {
        readFileContents = function() return 'archive-bytes' end
    }
    g_crypt = {
        sha256 = function() return string.rep('a', 64) end
    }
    g_logger = {
        info = function(message) state.logs[#state.logs + 1] = message end,
        warning = function(message) state.logs[#state.logs + 1] = message end
    }

    local loaded, loadError = pcall(dofile, sourceDir .. '/modules/client_assets/client_assets_release_adapter.lua')
    if not loaded then
        ClientAssetsReleaseAdapter = savedAdapter
        ClientAssetsReleaseSelector = savedSelector
        HTTP = savedHTTP
        Services = savedServices
        g_resources = savedResources
        g_crypt = savedCrypt
        g_logger = savedLogger
        error(loadError, 0)
    end

    local ok, result = xpcall(function()
        ClientAssetsReleaseAdapter.init()
        callback(state)
    end, debug.traceback)

    ClientAssetsReleaseAdapter.terminate()
    ClientAssetsReleaseAdapter = savedAdapter
    ClientAssetsReleaseSelector = savedSelector
    HTTP = savedHTTP
    Services = savedServices
    g_resources = savedResources
    g_crypt = savedCrypt
    g_logger = savedLogger
    if not ok then error(result, 0) end
end

test('client asset adapter keeps GitHub API headers until the configured response completes', function()
    withHarness(releaseWithDigest('sha256:' .. string.rep('a', 64)), function(state)
        local response = nil
        HTTP.getJSON('https://api.github.com/repos/dudantas/tibia-client/releases?per_page=100', function(data)
            response = data
        end)

        assertEqual('application/vnd.github+json', state.requestHeaders.Accept)
        assertEqual('2026-03-10', state.requestHeaders['X-GitHub-Api-Version'])
        assertEqual('application/vnd.github+json', state.activeHeaders.Accept)
        assertEqual('2026-03-10', state.activeHeaders['X-GitHub-Api-Version'])
        assertEqual(1, state.headerAdds)
        assertEqual(0, state.headerRemoves)

        state.pendingResponse(releaseWithDigest('sha256:' .. string.rep('a', 64)), nil)
        assertTrue(type(response) == 'table')
        assertEqual(2, state.headerRemoves)
        assertNil(state.activeHeaders.Accept)
        assertNil(state.activeHeaders['X-GitHub-Api-Version'])

        state.requestHeaders = nil
        HTTP.getJSON('https://example.invalid/catalog.json', function() end)
        assertNil(state.requestHeaders.Accept)
        assertNil(state.requestHeaders['X-GitHub-Api-Version'])
        assertEqual(1, state.headerAdds)
    end)
end)

test('client asset adapter fails closed before downloading an archive without a digest', function()
    withHarness(releaseWithDigest(nil), function(state)
        HTTP.getJSON('https://api.github.com/repos/dudantas/tibia-client/releases?per_page=100', function() end)
        state.pendingResponse(releaseWithDigest(nil), nil)

        local downloadError = nil
        HTTP.download(
            'https://example.invalid/client.zip',
            'asset-downloads/1525/client.zip',
            function(_, _, err) downloadError = err end)

        assertEqual(0, state.downloads)
        assertTrue(type(downloadError) == 'string')
        assertTrue(downloadError:find('missing an authoritative SHA-256 digest', 1, true) ~= nil)
    end)
end)
