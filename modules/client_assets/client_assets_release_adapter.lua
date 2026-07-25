ClientAssetsReleaseAdapter = ClientAssetsReleaseAdapter or {}

local Selector = rawget(_G, 'ClientAssetsReleaseSelector') or dofile('client_assets_release_selector')
local originalGetJSON = nil
local wrappedGetJSON = nil

function ClientAssetsReleaseAdapter.init()
    if wrappedGetJSON or not HTTP or type(HTTP.getJSON) ~= 'function' then
        return
    end

    originalGetJSON = HTTP.getJSON
    wrappedGetJSON = function(url, callback)
        if not Selector.isGitHubReleasesUrl(url) or type(callback) ~= 'function' then
            return originalGetJSON(url, callback)
        end

        return originalGetJSON(url, function(data, err)
            if not err and type(data) == 'table' then
                data = Selector.prepareReleases(data)
            end
            return callback(data, err)
        end)
    end
    HTTP.getJSON = wrappedGetJSON
end

function ClientAssetsReleaseAdapter.terminate()
    if wrappedGetJSON and HTTP and HTTP.getJSON == wrappedGetJSON then
        HTTP.getJSON = originalGetJSON
    end
    originalGetJSON = nil
    wrappedGetJSON = nil
end
