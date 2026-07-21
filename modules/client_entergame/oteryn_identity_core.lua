OterynIdentityCore = OterynIdentityCore or {}

local BASE64_ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
local SENSITIVE_CALLBACK_KEYS = {
    code = true,
    state = true,
    error = true,
    error_description = true
}

local function hexToBytes(hex)
    if type(hex) ~= 'string' or #hex % 2 ~= 0 or hex:find('[^0-9a-fA-F]') then
        return nil
    end

    local bytes = {}
    for i = 1, #hex, 2 do
        bytes[#bytes + 1] = string.char(tonumber(hex:sub(i, i + 1), 16))
    end
    return table.concat(bytes)
end

local function base64Encode(data)
    local output = {}
    for i = 1, #data, 3 do
        local a = data:byte(i) or 0
        local b = data:byte(i + 1) or 0
        local c = data:byte(i + 2) or 0
        local remaining = math.min(3, #data - i + 1)
        local value = a * 65536 + b * 256 + c

        local i1 = math.floor(value / 262144) % 64
        local i2 = math.floor(value / 4096) % 64
        local i3 = math.floor(value / 64) % 64
        local i4 = value % 64

        output[#output + 1] = BASE64_ALPHABET:sub(i1 + 1, i1 + 1)
        output[#output + 1] = BASE64_ALPHABET:sub(i2 + 1, i2 + 1)
        output[#output + 1] = remaining >= 2 and BASE64_ALPHABET:sub(i3 + 1, i3 + 1) or '='
        output[#output + 1] = remaining >= 3 and BASE64_ALPHABET:sub(i4 + 1, i4 + 1) or '='
    end
    return table.concat(output)
end

local function urlDecode(value)
    value = tostring(value or ''):gsub('+', ' ')
    local invalid = false
    value = value:gsub('%%([0-9a-fA-F][0-9a-fA-F])', function(hex)
        return string.char(tonumber(hex, 16))
    end)
    if value:find('%%') then
        invalid = true
    end
    return invalid and nil or value
end

function OterynIdentityCore.urlEncode(value)
    return (tostring(value or ''):gsub('([^%w%-._~])', function(char)
        return string.format('%%%02X', string.byte(char))
    end))
end

function OterynIdentityCore.pkceChallengeFromSha256Hex(sha256Hex)
    local digest = hexToBytes(sha256Hex)
    if not digest or #digest ~= 32 then
        return nil
    end
    return (base64Encode(digest):gsub('+', '-'):gsub('/', '_'):gsub('=', ''))
end

function OterynIdentityCore.parseCallbackTarget(target, expectedPath, expectedState)
    if type(target) ~= 'string' or type(expectedPath) ~= 'string' or type(expectedState) ~= 'string' then
        return nil, 'invalid_callback'
    end
    if target:find('#', 1, true) or target:find('://', 1, true) then
        return nil, 'invalid_callback'
    end

    local path, query = target:match('^([^?]*)(.*)$')
    if path ~= expectedPath then
        return nil, 'path_mismatch'
    end
    if query:sub(1, 1) == '?' then
        query = query:sub(2)
    elseif query ~= '' then
        return nil, 'invalid_callback'
    end

    local params = {}
    if query ~= '' then
        for pair in query:gmatch('[^&]+') do
            local rawKey, rawValue = pair:match('^([^=]*)=(.*)$')
            if not rawKey then
                rawKey, rawValue = pair, ''
            end
            local key = urlDecode(rawKey)
            local value = urlDecode(rawValue)
            if not key or not value or key == '' then
                return nil, 'invalid_callback'
            end
            if SENSITIVE_CALLBACK_KEYS[key] and params[key] ~= nil then
                return nil, 'duplicate_parameter'
            end
            params[key] = value
        end
    end

    if params.state ~= expectedState then
        return nil, 'state_mismatch'
    end
    if params.error and params.error ~= '' then
        return {
            kind = 'error',
            error = params.error
        }
    end
    if not params.code or params.code == '' then
        return nil, 'missing_code'
    end

    return {
        kind = 'code',
        code = params.code
    }
end

function OterynIdentityCore.isSafeEndpoint(url, allowInsecureLoopback)
    if type(url) ~= 'string' or url == '' then
        return false
    end
    if url:match('^https://') then
        return true
    end
    if allowInsecureLoopback and (url:match('^http://127%.0%.0%.1[:/]') or url == 'http://127.0.0.1') then
        return true
    end
    return false
end

function OterynIdentityCore.serverSupportsOteryn(server)
    if type(server) ~= 'table' or type(server.oterynIdentity) ~= 'table' then
        return false
    end
    local auth = server.oterynIdentity
    return server.authMode == 'oteryn_identity' and auth.enabled == true and
        tonumber(auth.protocolVersion) == 1 and type(auth.audience) == 'string' and auth.audience ~= '' and
        type(auth.loginEndpoint) == 'string' and auth.loginEndpoint ~= ''
end

function OterynIdentityCore.legacyAllowed(server)
    if type(server) ~= 'table' then
        return true
    end
    return server.legacyAuthEnabled ~= false
end

function OterynIdentityCore.mapOAuthError(code)
    if code == 'access_denied' then
        return 'Authentication was cancelled or denied.'
    end
    if code == 'temporarily_unavailable' or code == 'server_error' then
        return 'Oteryn is temporarily unavailable. Please try again.'
    end
    if code == 'invalid_grant' then
        return 'Authentication expired. Please try again.'
    end
    return 'Authentication failed. Please try again.'
end

function OterynIdentityCore.mapLoginServerError(code)
    if code == 'ticket_expired' then
        return 'The game login ticket expired. Please sign in again.'
    end
    if code == 'ticket_reused' then
        return 'The game login ticket was already used. Please sign in again.'
    end
    if code == 'ticket_invalid' or code == 'ticket_audience_mismatch' then
        return 'The game login ticket was rejected. Please sign in again.'
    end
    if code == 'rate_limited' then
        return 'Too many login attempts. Please wait and try again.'
    end
    return 'The login server is unavailable. Please try again.'
end

function OterynIdentityCore.newFlow(nowMillis, timeoutMillis)
    return {
        status = 'waiting',
        startedAt = tonumber(nowMillis) or 0,
        timeoutMillis = math.max(1000, tonumber(timeoutMillis) or 120000),
        callbackConsumed = false
    }
end

function OterynIdentityCore.cancelFlow(flow)
    if type(flow) ~= 'table' or flow.status ~= 'waiting' then
        return false
    end
    flow.status = 'cancelled'
    return true
end

function OterynIdentityCore.timeoutFlow(flow, nowMillis)
    if type(flow) ~= 'table' or flow.status ~= 'waiting' then
        return false
    end
    if (tonumber(nowMillis) or 0) - flow.startedAt < flow.timeoutMillis then
        return false
    end
    flow.status = 'timed_out'
    return true
end

function OterynIdentityCore.consumeCallback(flow)
    if type(flow) ~= 'table' or flow.status ~= 'waiting' or flow.callbackConsumed then
        return false
    end
    flow.callbackConsumed = true
    flow.status = 'exchanging_code'
    return true
end

return OterynIdentityCore
