local ClientAssetsReleaseSelector = {}

local ARCHIVE_EXTENSIONS = { '.zip', '.rar' }

local function endsWith(value, suffix)
    return type(value) == 'string' and suffix ~= '' and value:sub(-#suffix) == suffix
end

function ClientAssetsReleaseSelector.isArchivePath(path)
    path = tostring(path or ''):lower()
    for _, extension in ipairs(ARCHIVE_EXTENSIONS) do
        if endsWith(path, extension) then
            return true
        end
    end
    return false
end

function ClientAssetsReleaseSelector.isMacArchivePath(path)
    path = tostring(path or ''):lower()
    return endsWith(path, '.app.zip') or
        path:find('macos', 1, true) ~= nil or
        path:find('%f[%a]mac%f[^%a]') ~= nil
end

function ClientAssetsReleaseSelector.releaseVersionLabel(release)
    if type(release) ~= 'table' then
        return ''
    end

    local tag = tostring(release.tag_name or ''):lower()
    local name = tostring(release.name or ''):lower()
    return tag:match('%d+%.%d+') or name:match('%d+%.%d+') or ''
end

function ClientAssetsReleaseSelector.scoreAsset(release, asset)
    if type(release) ~= 'table' or type(asset) ~= 'table' then
        return 0
    end

    local name = tostring(asset.name or ''):lower()
    if not asset.browser_download_url or
        not ClientAssetsReleaseSelector.isArchivePath(name) or
        ClientAssetsReleaseSelector.isMacArchivePath(name) then
        return 0
    end

    local tag = tostring(release.tag_name or ''):lower()
    local label = ClientAssetsReleaseSelector.releaseVersionLabel(release)
    local score = 0

    if tag ~= '' and name:find(tag, 1, true) then
        score = score + 4
    end
    if label ~= '' and name:find(label, 1, true) then
        score = score + 2
    end

    if score == 0 then
        return 0
    end
    if name:find('client', 1, true) then
        score = score + 1
    end
    if name:find('original', 1, true) or name:find('linux', 1, true) then
        score = score - 1
    end

    return math.max(score, 0)
end

function ClientAssetsReleaseSelector.selectArchive(release)
    if type(release) ~= 'table' or type(release.assets) ~= 'table' then
        return nil
    end

    local bestAsset = nil
    local bestScore = 0
    for _, asset in ipairs(release.assets) do
        local score = ClientAssetsReleaseSelector.scoreAsset(release, asset)
        if score > bestScore then
            bestAsset = asset
            bestScore = score
        end
    end
    return bestAsset, bestScore
end

function ClientAssetsReleaseSelector.prepareRelease(release)
    if type(release) ~= 'table' then
        return release
    end
    if release._otclientArchiveSelectionPrepared then
        return release
    end

    local prepared = {}
    for key, value in pairs(release) do prepared[key] = value end
    prepared._otclientArchiveSelectionPrepared = true
    prepared.assets = {}

    local selected = ClientAssetsReleaseSelector.selectArchive(release)
    if selected then
        prepared.assets[#prepared.assets + 1] = selected
    end

    if type(release.assets) == 'table' then
        for _, asset in ipairs(release.assets) do
            if asset ~= selected and not ClientAssetsReleaseSelector.isArchivePath(asset.name) then
                prepared.assets[#prepared.assets + 1] = asset
            end
        end
    end

    return prepared
end

function ClientAssetsReleaseSelector.prepareReleases(releases)
    if type(releases) ~= 'table' then
        return releases
    end

    local prepared = {}
    for index, release in ipairs(releases) do
        prepared[index] = ClientAssetsReleaseSelector.prepareRelease(release)
    end
    return prepared
end

function ClientAssetsReleaseSelector.isGitHubReleasesUrl(url)
    url = tostring(url or ''):lower()
    return url:find('api.github.com/repos/', 1, true) ~= nil and
        url:find('/releases', 1, true) ~= nil
end

function ClientAssetsReleaseSelector.expectedInstallPaths(version)
    version = assert(tonumber(version), 'numeric client version is required')
    local thingsRoot = string.format('data/things/%d/', version)
    return {
        thingsRoot = thingsRoot,
        soundsRoot = string.format('data/sounds/%d/', version),
        extrasRoot = 'bin/',
        completionMarker = thingsRoot .. '.client-assets-complete',
        catalog = thingsRoot .. 'catalog-content.json',
        manifestHash = thingsRoot .. 'assets.json.sha256'
    }
end

function ClientAssetsReleaseSelector.hasRequiredRuntimePaths(version, catalog, fileExists)
    if type(catalog) ~= 'table' or type(fileExists) ~= 'function' then
        return false
    end

    local paths = ClientAssetsReleaseSelector.expectedInstallPaths(version)
    if not fileExists(paths.catalog) or not fileExists(paths.manifestHash) then
        return false
    end

    local hasAppearances = false
    local hasStaticData = false
    for _, entry in ipairs(catalog) do
        local entryType = entry.type
        if entryType == 'appearances' or entryType == 'staticdata' or entryType == 'proficiencies' then
            if type(entry.file) ~= 'string' or not fileExists(paths.thingsRoot .. entry.file) then
                return false
            end
            if entryType == 'appearances' then
                hasAppearances = true
            elseif entryType == 'staticdata' then
                hasStaticData = true
            end
        end
    end

    return hasAppearances and hasStaticData
end

return ClientAssetsReleaseSelector
