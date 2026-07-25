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

test('client asset selector recognizes only GitHub releases API URLs', function()
    assertTrue(Selector.isGitHubReleasesUrl('https://api.github.com/repos/dudantas/tibia-client/releases?per_page=100'))
    assertFalse(Selector.isGitHubReleasesUrl('https://api.github.com/repos/dudantas/tibia-client/git/trees/v15.24'))
    assertFalse(Selector.isGitHubReleasesUrl('https://example.invalid/releases'))
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
    local state = { calls = 0 }

    ClientAssetsReleaseSelector = Selector
    HTTP = {}
    local originalGetJSON = function(url, responseCallback)
        state.calls = state.calls + 1
        responseCallback(fixtures, nil)
        return 'operation-' .. state.calls
    end
    HTTP.getJSON = originalGetJSON

    local loaded, loadError = pcall(dofile, sourceDir .. '/modules/client_assets/client_assets_release_adapter.lua')
    if not loaded then
        ClientAssetsReleaseAdapter = savedAdapter
        ClientAssetsReleaseSelector = savedSelector
        HTTP = savedHTTP
        error(loadError, 0)
    end

    local success, result = xpcall(function()
        callback(state, originalGetJSON)
    end, debug.traceback)

    ClientAssetsReleaseAdapter.terminate()
    ClientAssetsReleaseAdapter = savedAdapter
    ClientAssetsReleaseSelector = savedSelector
    HTTP = savedHTTP
    if not success then error(result, 0) end
end

test('client asset adapter prepares only GitHub release responses and restores HTTP on unload', function()
    withAdapterHarness(function(_, originalGetJSON)
        ClientAssetsReleaseAdapter.init()
        local wrapper = HTTP.getJSON
        assertFalse(wrapper == originalGetJSON)

        local prepared = nil
        HTTP.getJSON('https://api.github.com/repos/dudantas/tibia-client/releases', function(data)
            prepared = data
        end)
        assertEqual('https://example.invalid/client.zip', legacyFindReleaseArchive(prepared[1]))
        assertNil(legacyFindReleaseArchive(prepared[2]))

        local passthrough = nil
        HTTP.getJSON('https://example.invalid/catalog.json', function(data)
            passthrough = data
        end)
        assertEqual(fixtures, passthrough)

        ClientAssetsReleaseAdapter.terminate()
        assertEqual(originalGetJSON, HTTP.getJSON)
    end)
end)
