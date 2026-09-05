local sourceDir = assert(os.getenv('OTCLIENT_SOURCE_DIR'), 'OTCLIENT_SOURCE_DIR is required')
local Selector = dofile(sourceDir .. '/modules/client_assets/client_assets_release_selector.lua')
local archiveUrl = 'https://github.com/dudantas/tibia-client/releases/download/v15.25.0a00a0/v15.25-client.zip'

local function cloneAsset(digest)
    return {
        name = 'v15.25-client.zip',
        browser_download_url = archiveUrl,
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

local function withHarness(callback)
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
    HTTP.getJSON = function(url, responseCallback)
        state.requestUrl = url
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
    withHarness(function(state)
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
    end)
end)

test('client asset adapter refreshes a missing digest binding before a configured release download', function()
    withHarness(function(state)
        local downloadError = 'not-called'
        HTTP.download(archiveUrl, 'asset-downloads/1525/client.zip', function(_, _, err)
            downloadError = err
        end)

        assertEqual(0, state.downloads)
        assertTrue(state.requestUrl:find('https://api.github.com/repos/dudantas/tibia-client/releases', 1, true) == 1)
        assertTrue(state.requestUrl:find('per_page=100', 1, true) ~= nil)
        assertEqual('2026-03-10', state.activeHeaders['X-GitHub-Api-Version'])

        state.pendingResponse(releaseWithDigest('sha256:' .. string.rep('a', 64)), nil)
        assertEqual(1, state.downloads)
        assertNil(downloadError)
        assertNil(state.activeHeaders['X-GitHub-Api-Version'])

        local verified = false
        for _, message in ipairs(state.logs) do
            if message:find('Verified downloaded asset archive SHA-256', 1, true) then
                verified = true
            end
        end
        assertTrue(verified)
    end)
end)

test('client asset adapter fails closed when a refreshed configured release lacks a digest', function()
    withHarness(function(state)
        local downloadError = nil
        HTTP.download(archiveUrl, 'asset-downloads/1525/client.zip', function(_, _, err)
            downloadError = err
        end)
        state.pendingResponse(releaseWithDigest(nil), nil)

        assertEqual(0, state.downloads)
        assertTrue(type(downloadError) == 'string')
        assertTrue(downloadError:find('missing an authoritative SHA-256 digest', 1, true) ~= nil)
    end)
end)

test('client asset adapter leaves unrelated downloads unchanged', function()
    withHarness(function(state)
        local downloadError = 'not-called'
        HTTP.download('https://example.invalid/client.zip', 'other/client.zip', function(_, _, err)
            downloadError = err
        end)

        assertEqual(1, state.downloads)
        assertNil(downloadError)
        assertNil(state.requestUrl)
        assertEqual(0, state.headerAdds)
    end)
end)

test('client asset adapter installs HTTP wrappers when ensureClientVersion runs after HTTP startup', function()
    local savedAdapter = rawget(_G, 'ClientAssetsReleaseAdapter')
    local savedSelector = rawget(_G, 'ClientAssetsReleaseSelector')
    local savedModules = rawget(_G, 'modules')
    local savedClientAssets = rawget(_G, 'ClientAssets')
    local savedHTTP = rawget(_G, 'HTTP')
    local savedServices = rawget(_G, 'Services')
    local savedLogger = rawget(_G, 'g_logger')

    local state = {
        ensureCalls = 0,
        callbackOk = nil
    }
    local originalEnsureClientVersion = function(version, callback)
        state.ensureCalls = state.ensureCalls + 1
        state.version = version
        callback(true, nil)
        return 'ensure-operation'
    end
    local originalGetJSON = function() return 'get-operation' end
    local originalDownload = function() return 'download-operation' end

    ClientAssetsReleaseAdapter = nil
    ClientAssetsReleaseSelector = Selector
    modules = {
        client_assets = {
            ensureClientVersion = originalEnsureClientVersion
        }
    }
    ClientAssets = nil
    HTTP = nil
    Services = { clientAssets = { repository = 'dudantas/tibia-client' } }
    g_logger = {
        info = function() end,
        warning = function() end
    }

    local ok, result = xpcall(function()
        dofile(sourceDir .. '/modules/client_assets/client_assets_release_adapter.lua')
        ClientAssetsReleaseAdapter.init()
        assertTrue(modules.client_assets.ensureClientVersion ~= originalEnsureClientVersion)

        HTTP = {
            getJSON = originalGetJSON,
            download = originalDownload,
            addCustomHeader = function() end,
            removeCustomHeader = function() end
        }

        local operation = modules.client_assets.ensureClientVersion(1525, function(callbackOk)
            state.callbackOk = callbackOk
        end)

        assertEqual('ensure-operation', operation)
        assertEqual(1, state.ensureCalls)
        assertEqual(1525, state.version)
        assertTrue(state.callbackOk)
        assertTrue(HTTP.getJSON ~= originalGetJSON)
        assertTrue(HTTP.download ~= originalDownload)

        ClientAssetsReleaseAdapter.terminate()
        assertEqual(originalEnsureClientVersion, modules.client_assets.ensureClientVersion)
        assertEqual(originalGetJSON, HTTP.getJSON)
        assertEqual(originalDownload, HTTP.download)
    end, debug.traceback)

    if ClientAssetsReleaseAdapter and type(ClientAssetsReleaseAdapter.terminate) == 'function' then
        pcall(ClientAssetsReleaseAdapter.terminate)
    end
    ClientAssetsReleaseAdapter = savedAdapter
    ClientAssetsReleaseSelector = savedSelector
    modules = savedModules
    ClientAssets = savedClientAssets
    HTTP = savedHTTP
    Services = savedServices
    g_logger = savedLogger

    if not ok then error(result, 0) end
end)
