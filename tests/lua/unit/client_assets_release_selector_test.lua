local sourceDir = assert(os.getenv('OTCLIENT_SOURCE_DIR'), 'OTCLIENT_SOURCE_DIR is required')
local Selector = dofile(sourceDir .. '/modules/client_assets/client_assets_release_selector.lua')
local fixtures = dofile(sourceDir .. '/tests/lua/fixtures/client_assets_releases.lua')

local function legacyFindReleaseArchive(release)
    if type(release.assets) ~= 'table' then return nil end
    local fallback = nil
    for _, asset in ipairs(release.assets) do
        local name = tostring(asset.name or ''):lower()
        local url = asset.browser_download_url
        if url and Selector.isArchivePath(name) then
            fallback = fallback or url
            if not name:find('mac', 1, true) and not name:find('.app.zip', 1, true) then
                return url
            end
        end
    end
    return fallback
end

test('client asset selector prefers the matching client archive', function()
    local selected, score = Selector.selectArchive(fixtures[1])
    assertEqual('v15.24-client.zip', selected.name)
    assertTrue(score > 0)

    local prepared = Selector.prepareRelease(fixtures[1])
    assertEqual('https://example.invalid/client.zip', legacyFindReleaseArchive(prepared))
    assertEqual('v15.24-client.zip', prepared.assets[1].name)
    assertEqual('SHA256SUMS.txt', prepared.assets[2].name)
end)

test('client asset selector normalizes only SHA-256 release digests', function()
    local selected = Selector.selectArchive(fixtures[1])
    assertEqual(string.rep('a', 64), Selector.assetSha256(selected))
    assertEqual(string.rep('b', 64), Selector.normalizeSha256Digest('  SHA256:' .. string.rep('B', 64) .. '  '))
    assertEqual(string.rep('c', 64), Selector.normalizeSha256Digest(string.rep('c', 64)))
    assertNil(Selector.normalizeSha256Digest('sha512:' .. string.rep('d', 64)))
    assertNil(Selector.normalizeSha256Digest('sha256:not-hex'))
    assertNil(Selector.normalizeSha256Digest(string.rep('e', 63)))
    assertNil(Selector.assetSha256({ digest = '' }))
end)

test('client asset selector excludes macOS and unrelated legacy archives', function()
    assertTrue(Selector.isMacArchivePath('Tibia.app.zip'))
    assertTrue(Selector.isMacArchivePath('client-macos.zip'))
    assertTrue(Selector.isMacArchivePath('client-mac.zip'))
    assertFalse(Selector.isMacArchivePath('client-15.24.zip'))

    local prepared = Selector.prepareRelease(fixtures[2])
    assertNil(legacyFindReleaseArchive(prepared))
    assertEqual(1, #prepared.assets)
    assertEqual('release-notes.txt', prepared.assets[1].name)
end)

test('client asset selector derives the release version from name when tag is generic', function()
    assertEqual('15.26', Selector.releaseVersionLabel(fixtures[3]))
    local selected = Selector.selectArchive(fixtures[3])
    assertEqual('client-15.26.rar', selected.name)
end)

test('client asset release preparation is cache-stable and idempotent', function()
    local prepared = Selector.prepareReleases(fixtures)
    local preparedAgain = Selector.prepareReleases(prepared)

    assertEqual(prepared[1], preparedAgain[1])
    assertEqual(prepared[2], preparedAgain[2])
    assertEqual('https://example.invalid/client.zip', legacyFindReleaseArchive(preparedAgain[1]))
    assertNil(legacyFindReleaseArchive(preparedAgain[2]))
end)

test('client asset selector recognizes and scopes configured GitHub release URLs', function()
    local defaultConfig = { repository = 'dudantas/tibia-client' }
    local customConfig = {
        repository = 'ignored/repository',
        releasesUrl = 'https://api.github.com/repos/oteryn/assets/releases?per_page=50'
    }

    assertTrue(Selector.isGitHubReleasesUrl('https://api.github.com/repos/dudantas/tibia-client/releases?per_page=100'))
    assertFalse(Selector.isGitHubReleasesUrl('https://api.github.com/repos/dudantas/tibia-client/git/trees/v15.24'))
    assertFalse(Selector.isGitHubReleasesUrl('https://example.invalid/releases'))

    assertTrue(Selector.isConfiguredReleasesUrl(
        'https://api.github.com/repos/dudantas/tibia-client/releases?per_page=100', defaultConfig))
    assertFalse(Selector.isConfiguredReleasesUrl(
        'https://api.github.com/repos/other/repository/releases', defaultConfig))
    assertTrue(Selector.isConfiguredReleasesUrl(
        'https://api.github.com/repos/oteryn/assets/releases?per_page=100', customConfig))
    assertFalse(Selector.isConfiguredReleasesUrl(
        'https://api.github.com/repos/ignored/repository/releases', customConfig))
    assertFalse(Selector.isConfiguredReleasesUrl(
        'https://api.github.com/repos/dudantas/tibia-client/releases', false))
end)

test('client asset final paths match the production installer contract', function()
    local paths = Selector.expectedInstallPaths(1524)
    assertEqual('data/things/1524/', paths.thingsRoot)
    assertEqual('data/sounds/1524/', paths.soundsRoot)
    assertEqual('bin/', paths.extrasRoot)
    assertEqual('data/things/1524/.client-assets-complete', paths.completionMarker)
    assertEqual('data/things/1524/catalog-content.json', paths.catalog)
    assertEqual('data/things/1524/assets.json.sha256', paths.manifestHash)
end)

test('client asset runtime path contract requires catalog, hash, appearances and static data', function()
    local files = {
        ['data/things/1524/catalog-content.json'] = true,
        ['data/things/1524/assets.json.sha256'] = true,
        ['data/things/1524/appearances.dat'] = true,
        ['data/things/1524/staticdata.dat'] = true,
        ['data/things/1524/proficiencies.dat'] = true
    }
    local catalog = {
        { type = 'appearances', file = 'appearances.dat' },
        { type = 'staticdata', file = 'staticdata.dat' },
        { type = 'proficiencies', file = 'proficiencies.dat' }
    }
    local exists = function(path) return files[path] == true end

    assertTrue(Selector.hasRequiredRuntimePaths(1524, catalog, exists))
    files['data/things/1524/staticdata.dat'] = nil
    assertFalse(Selector.hasRequiredRuntimePaths(1524, catalog, exists))
end)

local function withAdapterHarness(callback)
    local savedAdapter = rawget(_G, 'ClientAssetsReleaseAdapter')
    local savedSelector = rawget(_G, 'ClientAssetsReleaseSelector')
    local savedHTTP = rawget(_G, 'HTTP')
    local savedServices = rawget(_G, 'Services')
    local savedResources = rawget(_G, 'g_resources')
    local savedCrypt = rawget(_G, 'g_crypt')
    local savedLogger = rawget(_G, 'g_logger')
    local archiveContents = 'synthetic verified archive bytes'
    local state = {
        calls = 0,
        downloads = 0,
        reads = 0,
        logs = {},
        archiveContents = archiveContents
    }

    ClientAssetsReleaseSelector = Selector
    Services = {
        clientAssets = {
            repository = 'dudantas/tibia-client'
        }
    }
    HTTP = {}
    local originalGetJSON = function(url, responseCallback)
        state.calls = state.calls + 1
        responseCallback(fixtures, nil)
        return 'operation-' .. state.calls
    end
    local originalDownload = function(url, path, responseCallback, progressCallback)
        state.downloads = state.downloads + 1
        state.lastDownloadUrl = url
        state.lastDownloadPath = path
        state.lastProgressCallback = progressCallback
        if responseCallback then
            responseCallback(path, 'transport-checksum', nil)
        end
        return 'download-' .. state.downloads
    end
    HTTP.getJSON = originalGetJSON
    HTTP.download = originalDownload
    g_resources = {
        readFileContents = function(path)
            state.reads = state.reads + 1
            state.lastReadPath = path
            return archiveContents
        end
    }
    g_crypt = {
        sha256 = function(contents)
            assertEqual(archiveContents, contents)
            return string.rep('a', 64)
        end
    }
    g_logger = {
        info = function(message)
            state.logs[#state.logs + 1] = message
        end
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

    local success, result = xpcall(function()
        callback(state, originalGetJSON, originalDownload)
    end, debug.traceback)

    ClientAssetsReleaseAdapter.terminate()
    ClientAssetsReleaseAdapter = savedAdapter
    ClientAssetsReleaseSelector = savedSelector
    HTTP = savedHTTP
    Services = savedServices
    g_resources = savedResources
    g_crypt = savedCrypt
    g_logger = savedLogger
    if not success then error(result, 0) end
end

local function hasLog(state, fragment)
    for _, message in ipairs(state.logs) do
        if tostring(message):find(fragment, 1, true) then
            return true
        end
    end
    return false
end

test('client asset adapter prepares only configured release responses and restores HTTP on unload', function()
    withAdapterHarness(function(_, originalGetJSON, originalDownload)
        ClientAssetsReleaseAdapter.init()
        local getJsonWrapper = HTTP.getJSON
        local downloadWrapper = HTTP.download
        assertFalse(getJsonWrapper == originalGetJSON)
        assertFalse(downloadWrapper == originalDownload)

        local prepared = nil
        HTTP.getJSON('https://api.github.com/repos/dudantas/tibia-client/releases?per_page=100', function(data)
            prepared = data
        end)
        assertEqual('https://example.invalid/client.zip', legacyFindReleaseArchive(prepared[1]))
        assertNil(legacyFindReleaseArchive(prepared[2]))

        local otherRepository = nil
        HTTP.getJSON('https://api.github.com/repos/other/repository/releases', function(data)
            otherRepository = data
        end)
        assertEqual(fixtures, otherRepository)

        local passthrough = nil
        HTTP.getJSON('https://example.invalid/catalog.json', function(data)
            passthrough = data
        end)
        assertEqual(fixtures, passthrough)

        ClientAssetsReleaseAdapter.terminate()
        assertEqual(originalGetJSON, HTTP.getJSON)
        assertEqual(originalDownload, HTTP.download)
    end)
end)

test('client asset adapter verifies only configured selected release archives', function()
    withAdapterHarness(function(state)
        ClientAssetsReleaseAdapter.init()
        HTTP.getJSON('https://api.github.com/repos/dudantas/tibia-client/releases?per_page=100', function() end)

        local verifiedPath = nil
        local verifiedChecksum = nil
        local verifiedError = 'unset'
        HTTP.download(
            'https://example.invalid/client.zip',
            'asset-downloads/1524/client.zip',
            function(path, checksum, err)
                verifiedPath = path
                verifiedChecksum = checksum
                verifiedError = err
            end)

        assertEqual('asset-downloads/1524/client.zip', verifiedPath)
        assertEqual('transport-checksum', verifiedChecksum)
        assertNil(verifiedError)
        assertEqual(1, state.reads)
        assertEqual('/downloads/asset-downloads/1524/client.zip', state.lastReadPath)
        assertTrue(hasLog(state, 'Verified downloaded asset archive SHA-256'))

        local readsBefore = state.reads
        local unrelatedError = 'unset'
        HTTP.download(
            'https://example.invalid/unrelated.zip',
            'asset-downloads/1524/unrelated.zip',
            function(_, _, err) unrelatedError = err end)
        assertNil(unrelatedError)
        assertEqual(readsBefore, state.reads)
    end)
end)

test('client asset adapter rejects a selected release archive digest mismatch', function()
    withAdapterHarness(function(state)
        ClientAssetsReleaseAdapter.init()
        HTTP.getJSON('https://api.github.com/repos/dudantas/tibia-client/releases?per_page=100', function() end)
        g_crypt.sha256 = function(contents)
            assertEqual(state.archiveContents, contents)
            return string.rep('b', 64)
        end

        local mismatchError = nil
        HTTP.download(
            'https://example.invalid/client.zip',
            'asset-downloads/1524/client.zip',
            function(_, _, err) mismatchError = err end)

        assertTrue(type(mismatchError) == 'string')
        assertTrue(mismatchError:find('Invalid SHA-256', 1, true) ~= nil)
        assertFalse(hasLog(state, 'Verified downloaded asset archive SHA-256'))
    end)
end)
