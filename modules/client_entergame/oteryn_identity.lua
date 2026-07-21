OterynIdentity = OterynIdentity or {}

local Core = OterynIdentityCore
local activeFlow
local oterynButton
local enterGameWindow
local legacyDoLogin
local originalWindowHeight
local hostTextEdit
local callbackPath = '/oteryn/oauth/callback'

local function destroyWidget(widget)
    if widget then
        widget:destroy()
    end
end

local function getIdentityConfig()
    if not Services or type(Services.oterynIdentity) ~= 'table' then
        return nil
    end
    return Services.oterynIdentity
end

local function getServerConfig(host)
    if not Servers_init or type(Servers_init) ~= 'table' then
        return nil
    end
    return Servers_init[host]
end

local function getSelectedContext()
    if not enterGameWindow then
        return nil
    end

    local hostWidget = enterGameWindow:getChildById('serverHostTextEdit')
    local portWidget = enterGameWindow:getChildById('serverPortTextEdit')
    local clientWidget = enterGameWindow:getChildById('clientComboBox')
    if not hostWidget or not portWidget or not clientWidget then
        return nil
    end

    local host = hostWidget:getText()
    return {
        host = host,
        port = tonumber(portWidget:getText()),
        clientVersion = tonumber(clientWidget:getText()),
        server = getServerConfig(host)
    }
end

local function secureHex(bytes)
    local targetLength = math.max(1, tonumber(bytes) or 32) * 2
    local chunks = {}
    local length = 0
    while length < targetLength do
        local uuid = g_crypt.genUUID()
        if type(uuid) ~= 'string' or uuid == '' then
            return nil
        end
        local hex = uuid:gsub('%-', '')
        if #hex ~= 32 or hex:find('[^0-9a-fA-F]') then
            return nil
        end
        chunks[#chunks + 1] = hex
        length = length + #hex
    end
    return table.concat(chunks):sub(1, targetLength)
end

local function buildForm(fields)
    local keys = {}
    for key in pairs(fields) do
        keys[#keys + 1] = key
    end
    table.sort(keys)

    local output = {}
    for _, key in ipairs(keys) do
        if fields[key] ~= nil then
            output[#output + 1] = Core.urlEncode(key) .. '=' .. Core.urlEncode(fields[key])
        end
    end
    return table.concat(output, '&')
end

local function safeJsonDecode(value)
    if type(value) == 'table' then
        return value
    end
    if type(value) ~= 'string' or value == '' then
        return nil
    end
    local ok, decoded = pcall(json.decode, value)
    return ok and decoded or nil
end

local function removeFlowTimeout(flow)
    if flow and flow.timeoutEvent then
        removeEvent(flow.timeoutEvent)
        flow.timeoutEvent = nil
    end
end

local function closeFlowListener(flow)
    if flow and flow.listener then
        flow.listener:close()
        flow.listener = nil
    end
end

local function cancelHttpOperation(flow)
    if flow and flow.httpOperation then
        HTTP.cancel(flow.httpOperation)
        flow.httpOperation = nil
    end
end

local function clearSensitiveFlowFields(flow)
    if not flow then
        return
    end
    flow.codeVerifier = nil
    flow.state = nil
    flow.authorizationCode = nil
    flow.gameTicket = nil
    flow.accessToken = nil
    flow.refreshToken = nil
end

local function finishFlow(flow)
    if not flow or activeFlow ~= flow then
        return
    end
    removeFlowTimeout(flow)
    closeFlowListener(flow)
    cancelHttpOperation(flow)
    destroyWidget(flow.waitingBox)
    flow.waitingBox = nil
    clearSensitiveFlowFields(flow)
    activeFlow = nil
end

local function failFlow(flow, message)
    if not flow or activeFlow ~= flow then
        return
    end
    finishFlow(flow)
    local errorBox = displayErrorBox(tr('Login Error'), tr(message))
    connect(errorBox, {
        onOk = EnterGame.show
    })
end

local function selectLoopbackListener(state)
    local seed = tonumber(state:sub(1, 8), 16) or 0
    local firstPort = 49152 + (seed % 16384)
    for attempt = 0, 31 do
        local port = 49152 + ((firstPort - 49152 + attempt * 37) % 16384)
        local listener = Server.create(-port)
        if listener then
            return listener, port
        end
    end
    return nil, nil
end

local function requireSafeEndpoints(identity, server)
    local allowInsecureLoopback = identity.allowInsecureLoopback == true
    return Core.isSafeEndpoint(identity.authorizationEndpoint, allowInsecureLoopback) and
        Core.isSafeEndpoint(identity.tokenEndpoint, allowInsecureLoopback) and
        Core.isSafeEndpoint(server.oterynIdentity.loginEndpoint, allowInsecureLoopback)
end

local function buildCharacters(response)
    if type(response.worlds) ~= 'table' or type(response.characters) ~= 'table' then
        return nil
    end

    local worlds = {}
    for _, world in ipairs(response.worlds) do
        if world.id == nil or type(world.name) ~= 'string' or type(world.externaladdressprotected) ~= 'string' or
            tonumber(world.externalportprotected) == nil then
            return nil
        end
        worlds[world.id] = {
            name = world.name,
            ip = world.externaladdressprotected,
            port = tonumber(world.externalportprotected),
            previewState = tonumber(world.previewstate) == 1,
            pvptype = world.pvptype
        }
    end

    local characters = {}
    for index, character in ipairs(response.characters) do
        local world = worlds[character.worldid]
        if not world or type(character.name) ~= 'string' or character.name == '' then
            return nil
        end
        characters[index] = {
            name = character.name,
            level = character.level,
            main = character.ismaincharacter,
            dailyreward = character.dailyrewardstate,
            hidden = character.ishidden,
            vocation = character.vocation,
            outfitid = character.outfitid,
            headcolor = character.headcolor,
            torsocolor = character.torsocolor,
            legscolor = character.legscolor,
            detailcolor = character.detailcolor,
            addonsflags = character.addonsflags,
            worldName = world.name,
            worldIp = world.ip,
            worldPort = world.port,
            previewState = world.previewState,
            pvptype = world.pvptype
        }
    end
    return characters
end

local function completeLogin(flow, response)
    if activeFlow ~= flow then
        return
    end
    if type(response) ~= 'table' or tonumber(response.protocol_version) ~= 1 or type(response.session) ~= 'table' then
        failFlow(flow, 'The login server returned an invalid response.')
        return
    end

    local sessionKey = response.session.sessionkey
    if type(sessionKey) ~= 'string' or sessionKey == '' then
        failFlow(flow, 'The login server returned an invalid session.')
        return
    end

    local characters = buildCharacters(response)
    if not characters then
        failFlow(flow, 'The login server returned an invalid character list.')
        return
    end

    local premiumUntil = tonumber(response.session.premiumuntil) or 0
    local account = {
        status = response.session.status or '',
        premDays = math.max(0, math.floor((premiumUntil - os.time()) / 86400)),
        subStatus = premiumUntil > os.time() and SubscriptionStatus.Premium or SubscriptionStatus.Free
    }

    -- The Oteryn path intentionally leaves primary credentials empty. Modern
    -- game-world login must use GameSessionKey, which serializes sessionKey and
    -- character name instead of account/password.
    G.account = ''
    G.password = ''
    G.authenticatorToken = ''
    G.sessionKey = sessionKey
    G.host = flow.host
    G.port = flow.port
    G.clientVersion = flow.clientVersion

    g_settings.set('host', flow.host)
    g_settings.set('port', flow.port)
    g_settings.set('client-version', flow.clientVersion)
    g_settings.set('last-auth-mode', 'oteryn_identity')

    finishFlow(flow)
    EnterGame.hide()
    CharacterList.create(characters, account)
    CharacterList.show()
end

local function exchangeTicketWithLoginServer(flow)
    if activeFlow ~= flow then
        return
    end

    local ticket = flow.gameTicket
    if type(ticket) ~= 'string' or ticket == '' then
        failFlow(flow, 'Oteryn did not issue a game login ticket.')
        return
    end

    local request = {
        protocol_version = 1,
        auth_mode = 'oteryn_identity',
        game_ticket = ticket,
        client_version = flow.clientVersion
    }

    local endpoint = flow.server.oterynIdentity.loginEndpoint
    flow.httpOperation = HTTP.postJSON(endpoint, request, function(response, err)
        if activeFlow ~= flow then
            return
        end
        flow.httpOperation = nil
        if err then
            local decoded = safeJsonDecode(response)
            local code = decoded and decoded.error_code or nil
            failFlow(flow, Core.mapLoginServerError(code))
            return
        end
        response = safeJsonDecode(response)
        if not response then
            failFlow(flow, 'The login server returned an invalid response.')
            return
        end
        if response.error_code then
            failFlow(flow, Core.mapLoginServerError(response.error_code))
            return
        end
        completeLogin(flow, response)
    end)

    -- HTTP owns the queued request body now. Drop the Lua reference immediately;
    -- the ticket is never written to settings and is not retained for retries.
    flow.gameTicket = nil
end

local function exchangeAuthorizationCode(flow)
    if activeFlow ~= flow then
        return
    end

    local identity = flow.identity
    local body = buildForm({
        grant_type = 'authorization_code',
        client_id = identity.clientId,
        code = flow.authorizationCode,
        redirect_uri = flow.redirectUri,
        code_verifier = flow.codeVerifier,
        audience = flow.server.oterynIdentity.audience
    })

    flow.httpOperation = HTTP.post(identity.tokenEndpoint, body, function(data, err)
        if activeFlow ~= flow then
            return
        end
        flow.httpOperation = nil
        local response = safeJsonDecode(data)
        if err then
            failFlow(flow, Core.mapOAuthError(response and response.error or nil))
            return
        end
        if type(response) ~= 'table' then
            failFlow(flow, 'Oteryn returned an invalid authentication response.')
            return
        end
        if response.error then
            failFlow(flow, Core.mapOAuthError(response.error))
            return
        end

        -- OAuth access/refresh credentials, if returned by the platform, are not
        -- persisted because this repository currently has no OS credential-store
        -- abstraction. The game ticket is the only credential forwarded onward.
        flow.accessToken = response.access_token
        flow.refreshToken = response.refresh_token
        flow.gameTicket = response.game_login_ticket
        local ticketTtl = tonumber(response.game_login_ticket_expires_in)
        local maximumTtl = tonumber(identity.maxGameTicketTtlSeconds) or 60
        if type(flow.gameTicket) ~= 'string' or flow.gameTicket == '' or not ticketTtl or ticketTtl <= 0 or ticketTtl > maximumTtl then
            failFlow(flow, 'Oteryn returned an invalid game login ticket.')
            return
        end
        if response.game_login_ticket_audience and response.game_login_ticket_audience ~= flow.server.oterynIdentity.audience then
            failFlow(flow, 'Oteryn returned a game login ticket for a different server.')
            return
        end

        flow.authorizationCode = nil
        flow.codeVerifier = nil
        flow.accessToken = nil
        flow.refreshToken = nil
        exchangeTicketWithLoginServer(flow)
    end)

    flow.authorizationCode = nil
end

local function onLoopbackRequest(flow, first, second, third, fourth)
    if activeFlow ~= flow then
        return
    end

    -- LuaObject callbacks may expose only explicit arguments or include the
    -- object as the first value depending on binding context. Accept both forms.
    local target, callbackError
    if type(first) == 'string' then
        target, callbackError = first, second
    else
        target, callbackError = second, third
    end

    if callbackError and callbackError ~= '' then
        if flow.listener then
            flow.listener:acceptNext()
        end
        return
    end

    local result, validationError = Core.parseCallbackTarget(target, callbackPath, flow.state)
    if not result then
        if validationError == 'state_mismatch' or validationError == 'path_mismatch' or validationError == 'invalid_callback' or validationError == 'duplicate_parameter' then
            if flow.listener then
                flow.listener:acceptNext()
            end
            return
        end
        failFlow(flow, 'Authentication failed. Please try again.')
        return
    end

    if result.kind == 'error' then
        failFlow(flow, Core.mapOAuthError(result.error))
        return
    end
    if not Core.consumeCallback(flow.lifecycle) then
        return
    end

    flow.authorizationCode = result.code
    closeFlowListener(flow)
    exchangeAuthorizationCode(flow)
end

local function openAuthorization(flow)
    local identity = flow.identity
    local challengeHex = g_crypt.sha256(flow.codeVerifier)
    local challenge = Core.pkceChallengeFromSha256Hex(challengeHex)
    if not challenge then
        failFlow(flow, 'Unable to initialize secure authentication.')
        return
    end

    local query = buildForm({
        response_type = 'code',
        client_id = identity.clientId,
        redirect_uri = flow.redirectUri,
        scope = identity.scope or 'game.login',
        code_challenge = challenge,
        code_challenge_method = 'S256',
        state = flow.state
    })
    local authorizationUrl = identity.authorizationEndpoint .. (identity.authorizationEndpoint:find('?', 1, true) and '&' or '?') .. query

    flow.listener.onHttpRequest = function(first, second, third, fourth)
        onLoopbackRequest(flow, first, second, third, fourth)
    end
    flow.listener:acceptNext()

    flow.waitingBox = displayCancelBox(tr('Waiting for authentication'), tr('Complete sign-in in your browser.'))
    connect(flow.waitingBox, {
        onCancel = function()
            if activeFlow == flow then
                OterynIdentity.cancel()
            end
        end
    })

    g_platform.openUrl(authorizationUrl)
end

local function beginAfterAssets(context)
    local identity = getIdentityConfig()
    local server = context.server
    if not identity or identity.enabled ~= true or not Core.serverSupportsOteryn(server) then
        local errorBox = displayErrorBox(tr('Login Error'), tr('Sign in with Oteryn is not configured for this server.'))
        connect(errorBox, { onOk = EnterGame.show })
        return
    end
    if not g_platform.isDesktop() or not Server then
        local errorBox = displayErrorBox(tr('Login Error'), tr('Sign in with Oteryn is not available on this platform.'))
        connect(errorBox, { onOk = EnterGame.show })
        return
    end
    if type(identity.clientId) ~= 'string' or identity.clientId == '' or not requireSafeEndpoints(identity, server) then
        local errorBox = displayErrorBox(tr('Login Error'), tr('Sign in with Oteryn is not securely configured.'))
        connect(errorBox, { onOk = EnterGame.show })
        return
    end

    g_game.setClientVersion(context.clientVersion)
    g_game.setProtocolVersion(g_game.getClientProtocolVersion(context.clientVersion))
    g_game.chooseRsa(context.host)
    if not g_game.getFeature(GameSessionKey) then
        local errorBox = displayErrorBox(tr('Login Error'), tr('This server does not support session-key game login required by Oteryn.'))
        connect(errorBox, { onOk = EnterGame.show })
        return
    end
    if modules.game_things.isLoaded and not modules.game_things.isLoaded() then
        local errorBox = displayErrorBox(tr('Login Error'), tr('Required client assets are not loaded.'))
        connect(errorBox, { onOk = EnterGame.show })
        return
    end

    local state = secureHex(32)
    local verifier = secureHex(32)
    if not state or not verifier or #verifier < 43 then
        local errorBox = displayErrorBox(tr('Login Error'), tr('Unable to initialize secure authentication.'))
        connect(errorBox, { onOk = EnterGame.show })
        return
    end

    local listener, port = selectLoopbackListener(state)
    if not listener then
        local errorBox = displayErrorBox(tr('Login Error'), tr('Unable to open the local authentication callback.'))
        connect(errorBox, { onOk = EnterGame.show })
        return
    end

    local timeoutMillis = math.max(10000, math.min(300000, tonumber(identity.callbackTimeoutMillis) or 120000))
    local flow = {
        identity = identity,
        server = server,
        host = context.host,
        port = context.port,
        clientVersion = context.clientVersion,
        state = state,
        codeVerifier = verifier,
        listener = listener,
        redirectUri = string.format('http://127.0.0.1:%d%s', port, callbackPath),
        lifecycle = Core.newFlow(g_clock.realMillis(), timeoutMillis)
    }
    activeFlow = flow

    flow.timeoutEvent = scheduleEvent(function()
        if activeFlow == flow and Core.timeoutFlow(flow.lifecycle, g_clock.realMillis()) then
            failFlow(flow, 'Authentication timed out. Please try again.')
        end
    end, timeoutMillis)

    openAuthorization(flow)
end

function OterynIdentity.start()
    if activeFlow then
        return
    end
    if g_game.isOnline() then
        local errorBox = displayErrorBox(tr('Login Error'), tr('Cannot login while already in game.'))
        connect(errorBox, { onOk = EnterGame.show })
        return
    end

    local context = getSelectedContext()
    if not context or not context.host or context.host == '' or not context.port or not context.clientVersion then
        local errorBox = displayErrorBox(tr('Login Error'), tr('Select a valid server and client version first.'))
        connect(errorBox, { onOk = EnterGame.show })
        return
    end

    if context.clientVersion >= 1281 and modules.client_assets and modules.client_assets.ensureClientVersion and
        (not modules.client_assets.isEnabled or modules.client_assets.isEnabled()) and
        not modules.client_assets.isClientVersionInstalled(context.clientVersion) then
        modules.client_assets.ensureClientVersion(context.clientVersion, function(success, message)
            if success then
                beginAfterAssets(context)
                return
            end
            local errorBox = displayErrorBox(tr('Login Error'), message or tr('Unable to download client assets.'))
            connect(errorBox, { onOk = EnterGame.show })
        end)
        return
    end

    beginAfterAssets(context)
end

function OterynIdentity.cancel()
    local flow = activeFlow
    if not flow then
        return
    end
    Core.cancelFlow(flow.lifecycle)
    finishFlow(flow)
    EnterGame.show()
end

function OterynIdentity.updateUi()
    if not enterGameWindow or not oterynButton then
        return
    end
    local context = getSelectedContext()
    local identity = getIdentityConfig()
    local enabled = identity and identity.enabled == true and context and Core.serverSupportsOteryn(context.server)
    oterynButton:setVisible(enabled and true or false)
    oterynButton:setEnabled(enabled and activeFlow == nil)

    local legacyAllowed = not context or Core.legacyAllowed(context.server)
    local ids = {
        'accountNameTextEdit', 'accountPasswordTextEdit', 'rememberEmailBox', 'autoLoginBox', 'httpLoginBox'
    }
    for _, id in ipairs(ids) do
        local widget = enterGameWindow:getChildById(id)
        if widget then
            widget:setEnabled(legacyAllowed)
        end
    end
end

function OterynIdentity.init()
    enterGameWindow = rootWidget:recursiveGetChildById('enterGame')
    if not enterGameWindow then
        return
    end

    originalWindowHeight = enterGameWindow:getHeight()
    enterGameWindow:setHeight(originalWindowHeight + 32)
    oterynButton = g_ui.createWidget('QtButton', enterGameWindow)
    oterynButton:setId('oterynLoginButton')
    oterynButton:setText(tr('Sign in with Oteryn'))
    oterynButton:setHeight(24)
    oterynButton:addAnchor(AnchorLeft, 'parent', AnchorLeft)
    oterynButton:addAnchor(AnchorRight, 'parent', AnchorRight)
    oterynButton:addAnchor(AnchorBottom, 'parent', AnchorBottom)
    oterynButton.onClick = OterynIdentity.start

    hostTextEdit = enterGameWindow:getChildById('serverHostTextEdit')
    if hostTextEdit then
        connect(hostTextEdit, { onTextChange = OterynIdentity.updateUi })
    end

    legacyDoLogin = EnterGame.doLogin
    EnterGame.doLogin = function(...)
        local context = getSelectedContext()
        if context and context.server and context.server.authMode == 'oteryn_identity' and not Core.legacyAllowed(context.server) then
            OterynIdentity.start()
            return
        end
        return legacyDoLogin(...)
    end

    OterynIdentity.updateUi()
end

function OterynIdentity.terminate()
    if activeFlow then
        OterynIdentity.cancel()
    end
    if hostTextEdit then
        disconnect(hostTextEdit, { onTextChange = OterynIdentity.updateUi })
        hostTextEdit = nil
    end
    if legacyDoLogin and EnterGame then
        EnterGame.doLogin = legacyDoLogin
    end
    legacyDoLogin = nil
    if oterynButton then
        oterynButton:destroy()
        oterynButton = nil
    end
    if enterGameWindow and originalWindowHeight then
        enterGameWindow:setHeight(originalWindowHeight)
    end
    enterGameWindow = nil
    originalWindowHeight = nil
end

return OterynIdentity
