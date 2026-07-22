OterynSessionGuard = OterynSessionGuard or {}

local originalDoLogin

local function requireFreshSession()
    local errorBox = displayErrorBox(
        tr('Login Error'),
        tr('Your Oteryn game session can no longer be reused. Sign in with Oteryn again.')
    )
    connect(errorBox, {
        onOk = function()
            CharacterList.hide(true)
        end
    })
end

function OterynSessionGuard.init()
    if originalDoLogin or not CharacterList or not CharacterList.doLogin then
        return
    end

    originalDoLogin = CharacterList.doLogin
    CharacterList.doLogin = function(...)
        if not G.oterynGameSession then
            return originalDoLogin(...)
        end

        if G.oterynGameSessionConsumed or type(G.sessionKey) ~= 'string' or G.sessionKey == '' then
            requireFreshSession()
            return
        end

        -- CharacterList's normal path may defer a login while another game
        -- connection is still active. A one-shot Oteryn session must never be
        -- retained for such a deferred replay, so fail closed instead.
        if g_game.isOnline() then
            requireFreshSession()
            return
        end

        local result = originalDoLogin(...)

        -- g_game.loginWorld copies the session credential into ProtocolGame
        -- synchronously on the normal offline path. Clear the global copy as
        -- soon as CharacterList.doLogin returns and mark it non-replayable.
        G.sessionKey = ''
        G.oterynGameSessionConsumed = true
        return result
    end
end

function OterynSessionGuard.terminate()
    if originalDoLogin and CharacterList then
        CharacterList.doLogin = originalDoLogin
    end
    originalDoLogin = nil
end

return OterynSessionGuard
