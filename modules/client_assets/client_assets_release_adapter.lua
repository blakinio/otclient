ClientAssetsReleaseAdapter = ClientAssetsReleaseAdapter or {}

local Selector = rawget(_G, 'ClientAssetsReleaseSelector') or dofile('client_assets_release_selector')
local originalGetJSON = nil
local wrappedGetJSON = nil
local originalDownload = nil
local wrappedDownload = nil
local archiveSha256ByUrl = {}
local MISSING_ARCHIVE_DIGEST = {}
local GITHUB_API_HEADERS = {
    Accept = 'application/vnd.github+json',
    ['X-GitHub-Api-Version'] = '2026-03-10'
}

local function serviceConfig()
    return Services and Services.clientAssets
end

local function logInfo(message)
    if g_logger and type(g_logger.info) == 'function' then
        g_logger.info('[client_assets] ' .. tostring(message))
    end
end

local function withGitHubApiHeaders(callback)
    if type(HTTP.addCustomHeader) ~= 'function' or type(HTTP.removeCustomHeader) ~= 'function' then
        return callback()
    end

    HTTP.addCustomHeader(GITHUB_API_HEADERS)
    local ok, result = pcall(callback)
    for name in pairs(GITHUB_API_HEADERS) do
        pcall(HTTP.removeCustomHeader, name)
    end
    if not ok then
        error(result, 0)
    end
    return result
end

local function rememberArchiveDigests(releases)
    archiveSha256ByUrl = {}
    if type(releases) ~= 'table' then
        return
    end

    for _, release in ipairs(releases) do
        if type(release) == 'table' and type(release.assets) == 'table' then
            for _, asset in ipairs(release.assets) do
                local url = type(asset) == 'table' and asset.browser_download_url or nil
                if type(url) == 'string' and url ~= '' and Selector.isArchivePath(asset.name) then
                    archiveSha256ByUrl[url] = Selector.assetSha256(asset) or MISSING_ARCHIVE_DIGEST
                end
            end
        end
    end
end

local function verifyDownloadedArchive(path, expectedSha256)
    local ok, contents = pcall(function()
        return g_resources.readFileContents('/downloads/' .. tostring(path))
    end)
    if not ok or type(contents) ~= 'string' then
        return false, string.format('Unable to read downloaded client asset archive for SHA-256 verification: %s', tostring(contents))
    end

    local actualSha256 = tostring(g_crypt.sha256(contents) or ''):lower()
    if actualSha256 ~= expectedSha256 then
        return false, string.format('Invalid SHA-256 for %s. Expected %s, got %s.', tostring(path), expectedSha256, actualSha256)
    end

    return true
end

function ClientAssetsReleaseAdapter.init()
    if wrappedGetJSON or wrappedDownload or not HTTP or type(HTTP.getJSON) ~= 'function' then
        return
    end

    originalGetJSON = HTTP.getJSON
    wrappedGetJSON = function(url, callback)
        if not Selector.isConfiguredReleasesUrl(url, serviceConfig()) or type(callback) ~= 'function' then
            return originalGetJSON(url, callback)
        end

        return withGitHubApiHeaders(function()
            return originalGetJSON(url, function(data, err)
                if not err and type(data) == 'table' then
                    data = Selector.prepareReleases(data)
                    rememberArchiveDigests(data)
                end
                return callback(data, err)
            end)
        end)
    end
    HTTP.getJSON = wrappedGetJSON

    if type(HTTP.download) == 'function' then
        originalDownload = HTTP.download
        wrappedDownload = function(url, path, callback, progressCallback)
            local expectedSha256 = archiveSha256ByUrl[url]
            if expectedSha256 == nil or type(callback) ~= 'function' then
                return originalDownload(url, path, callback, progressCallback)
            end
            if expectedSha256 == MISSING_ARCHIVE_DIGEST then
                return callback(path, nil, string.format(
                    'Configured client asset archive is missing an authoritative SHA-256 digest: %s.',
                    tostring(url)))
            end

            return originalDownload(url, path, function(downloadPath, checksum, err)
                if err then
                    return callback(downloadPath, checksum, err)
                end

                local ok, hashError = verifyDownloadedArchive(downloadPath, expectedSha256)
                if not ok then
                    return callback(downloadPath, checksum, hashError)
                end

                logInfo(string.format('Verified downloaded asset archive SHA-256 for %s.', url))
                return callback(downloadPath, checksum, nil)
            end, progressCallback)
        end
        HTTP.download = wrappedDownload
    end
end

function ClientAssetsReleaseAdapter.terminate()
    if wrappedGetJSON and HTTP and HTTP.getJSON == wrappedGetJSON then
        HTTP.getJSON = originalGetJSON
    end
    if wrappedDownload and HTTP and HTTP.download == wrappedDownload then
        HTTP.download = originalDownload
    end

    originalGetJSON = nil
    wrappedGetJSON = nil
    originalDownload = nil
    wrappedDownload = nil
    archiveSha256ByUrl = {}
end
