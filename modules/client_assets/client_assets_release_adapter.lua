ClientAssetsReleaseAdapter = ClientAssetsReleaseAdapter or {}

local Selector = rawget(_G, 'ClientAssetsReleaseSelector') or dofile('client_assets_release_selector')
local originalGetJSON = nil
local wrappedGetJSON = nil
local originalDownload = nil
local wrappedDownload = nil
local ensureWrappers = {}
local archiveSha256ByUrl = {}
local MISSING_ARCHIVE_DIGEST = {}
local GITHUB_API_HEADERS = {
    Accept = 'application/vnd.github+json',
    ['X-GitHub-Api-Version'] = '2026-03-10'
}
local activeGitHubHeaderRequests = 0

local function serviceConfig()
    return Services and Services.clientAssets
end

local function logInfo(message)
    if g_logger and type(g_logger.info) == 'function' then
        g_logger.info('[client_assets] ' .. tostring(message))
    end
end

local function logWarning(message)
    if g_logger and type(g_logger.warning) == 'function' then
        g_logger.warning('[client_assets] ' .. tostring(message))
    end
end

local function configuredRepository()
    local config = serviceConfig()
    local repository = type(config) == 'table' and config.repository or nil
    if type(repository) == 'string' and repository:match('^[%w_.-]+/[%w_.-]+$') then
        return repository
    end

    local releasesUrl = type(config) == 'table' and config.releasesUrl or nil
    if type(releasesUrl) == 'string' then
        repository = releasesUrl:match('^https://api%.github%.com/repos/([^/]+/[^/]+)/releases')
        if repository then
            return repository
        end
    end

    return 'dudantas/tibia-client'
end

local function configuredReleasesUrl()
    local config = serviceConfig()
    local releasesUrl = type(config) == 'table' and config.releasesUrl or nil
    if type(releasesUrl) ~= 'string' or releasesUrl == '' then
        releasesUrl = string.format('https://api.github.com/repos/%s/releases', configuredRepository())
    end

    if not releasesUrl:find('per_page=', 1, true) then
        releasesUrl = releasesUrl .. (releasesUrl:find('?', 1, true) and '&' or '?') .. 'per_page=100'
    end
    return releasesUrl
end

local function isConfiguredReleaseDownloadUrl(url)
    if type(url) ~= 'string' then
        return false
    end

    local prefix = string.format('https://github.com/%s/releases/download/', configuredRepository()):lower()
    return url:sub(1, #prefix):lower() == prefix
end

local function addGitHubApiHeaders()
    if not HTTP or type(HTTP.addCustomHeader) ~= 'function' or type(HTTP.removeCustomHeader) ~= 'function' then
        return false
    end

    if activeGitHubHeaderRequests == 0 then
        HTTP.addCustomHeader(GITHUB_API_HEADERS)
    end
    activeGitHubHeaderRequests = activeGitHubHeaderRequests + 1
    return true
end

local function removeGitHubApiHeaders()
    if activeGitHubHeaderRequests <= 0 then
        return
    end

    activeGitHubHeaderRequests = activeGitHubHeaderRequests - 1
    if activeGitHubHeaderRequests == 0 and HTTP and type(HTTP.removeCustomHeader) == 'function' then
        for name in pairs(GITHUB_API_HEADERS) do
            pcall(HTTP.removeCustomHeader, name)
        end
    end
end

local function clearGitHubApiHeaders()
    if activeGitHubHeaderRequests > 0 and HTTP and type(HTTP.removeCustomHeader) == 'function' then
        for name in pairs(GITHUB_API_HEADERS) do
            pcall(HTTP.removeCustomHeader, name)
        end
    end
    activeGitHubHeaderRequests = 0
end

local function rememberArchiveDigests(releases)
    archiveSha256ByUrl = {}
    local boundDigests = 0
    local missingDigests = 0
    if type(releases) ~= 'table' then
        return boundDigests, missingDigests
    end

    for _, release in ipairs(releases) do
        if type(release) == 'table' and type(release.assets) == 'table' then
            for _, asset in ipairs(release.assets) do
                local url = type(asset) == 'table' and asset.browser_download_url or nil
                if type(url) == 'string' and url ~= '' and Selector.isArchivePath(asset.name) then
                    local digest = Selector.assetSha256(asset)
                    archiveSha256ByUrl[url] = digest or MISSING_ARCHIVE_DIGEST
                    if digest then
                        boundDigests = boundDigests + 1
                    else
                        missingDigests = missingDigests + 1
                    end
                end
            end
        end
    end

    return boundDigests, missingDigests
end

local function finishReleaseCatalog(data, err)
    if not err and type(data) == 'table' then
        data = Selector.prepareReleases(data)
        local boundDigests, missingDigests = rememberArchiveDigests(data)
        logInfo(string.format(
            'Bound %d configured release archive SHA-256 digest(s); %d selected archive(s) lacked a digest.',
            boundDigests,
            missingDigests))
    end
    return data, err
end

local function requestReleaseCatalog(url, callback)
    local headersAdded = addGitHubApiHeaders()
    local responseHandled = false
    local function finishHeaders()
        if responseHandled then
            return
        end
        responseHandled = true
        if headersAdded then
            removeGitHubApiHeaders()
        end
    end

    local ok, result = pcall(originalGetJSON, url, function(data, err)
        finishHeaders()
        data, err = finishReleaseCatalog(data, err)
        return callback(data, err)
    end)
    if not ok then
        finishHeaders()
        error(result, 0)
    end
    return result
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

local function failMissingDigest(url, path, callback)
    logWarning(string.format('Refusing configured release archive without an authoritative SHA-256 digest: %s.', tostring(url)))
    return callback(path, nil, string.format(
        'Configured client asset archive is missing an authoritative SHA-256 digest: %s.',
        tostring(url)))
end

local function downloadVerified(url, path, callback, progressCallback, expectedSha256)
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

local function releaseWrappersAreInstalled()
    return HTTP and
        wrappedGetJSON and HTTP.getJSON == wrappedGetJSON and
        wrappedDownload and HTTP.download == wrappedDownload
end

local function forgetDetachedHttpWrappers()
    if wrappedGetJSON and (not HTTP or HTTP.getJSON ~= wrappedGetJSON) then
        originalGetJSON = nil
        wrappedGetJSON = nil
    end
    if wrappedDownload and (not HTTP or HTTP.download ~= wrappedDownload) then
        originalDownload = nil
        wrappedDownload = nil
    end
end

local function installHttpWrappers()
    if not HTTP or type(HTTP.getJSON) ~= 'function' or type(HTTP.download) ~= 'function' then
        return false
    end
    if releaseWrappersAreInstalled() then
        return true
    end

    forgetDetachedHttpWrappers()

    if not wrappedGetJSON then
        originalGetJSON = HTTP.getJSON
        wrappedGetJSON = function(url, callback)
            if not Selector.isConfiguredReleasesUrl(url, serviceConfig()) or type(callback) ~= 'function' then
                return originalGetJSON(url, callback)
            end
            return requestReleaseCatalog(url, callback)
        end
        HTTP.getJSON = wrappedGetJSON
    end

    if not wrappedDownload then
        originalDownload = HTTP.download
        wrappedDownload = function(url, path, callback, progressCallback)
            if type(callback) ~= 'function' then
                return originalDownload(url, path, callback, progressCallback)
            end

            local expectedSha256 = archiveSha256ByUrl[url]
            if expectedSha256 == MISSING_ARCHIVE_DIGEST then
                return failMissingDigest(url, path, callback)
            end
            if expectedSha256 then
                return downloadVerified(url, path, callback, progressCallback, expectedSha256)
            end
            if not isConfiguredReleaseDownloadUrl(url) then
                return originalDownload(url, path, callback, progressCallback)
            end

            logInfo(string.format('Refreshing configured release digests before downloading %s.', url))
            return requestReleaseCatalog(configuredReleasesUrl(), function(_, err)
                if err then
                    return callback(path, nil, string.format(
                        'Unable to resolve an authoritative SHA-256 digest for %s: %s.',
                        tostring(url),
                        tostring(err)))
                end

                expectedSha256 = archiveSha256ByUrl[url]
                if expectedSha256 == nil or expectedSha256 == MISSING_ARCHIVE_DIGEST then
                    return failMissingDigest(url, path, callback)
                end
                return downloadVerified(url, path, callback, progressCallback, expectedSha256)
            end)
        end
        HTTP.download = wrappedDownload
    end

    return releaseWrappersAreInstalled()
end

local function wrapEnsureClientVersion(target)
    if type(target) ~= 'table' or type(target.ensureClientVersion) ~= 'function' then
        return
    end

    for _, entry in ipairs(ensureWrappers) do
        if entry.target == target then
            return
        end
    end

    local original = target.ensureClientVersion
    local wrapped = function(version, callback)
        if not installHttpWrappers() then
            local message = 'Unable to enable release archive SHA-256 verification because HTTP is unavailable.'
            logWarning(message)
            if type(callback) == 'function' then
                return callback(false, message)
            end
            return false
        end
        return original(version, callback)
    end

    target.ensureClientVersion = wrapped
    ensureWrappers[#ensureWrappers + 1] = {
        target = target,
        original = original,
        wrapped = wrapped
    }
end

local function installEnsureClientVersionWrappers()
    if modules and type(modules.client_assets) == 'table' then
        wrapEnsureClientVersion(modules.client_assets)
    end
    if type(ClientAssets) == 'table' then
        wrapEnsureClientVersion(ClientAssets)
    end
end

function ClientAssetsReleaseAdapter.init()
    installEnsureClientVersionWrappers()
    installHttpWrappers()
end

function ClientAssetsReleaseAdapter.terminate()
    clearGitHubApiHeaders()

    for index = #ensureWrappers, 1, -1 do
        local entry = ensureWrappers[index]
        if entry.target.ensureClientVersion == entry.wrapped then
            entry.target.ensureClientVersion = entry.original
        end
    end
    ensureWrappers = {}

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
