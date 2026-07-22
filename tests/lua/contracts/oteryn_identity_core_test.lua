local sourceDir = assert(os.getenv('OTCLIENT_SOURCE_DIR'), 'OTCLIENT_SOURCE_DIR is required')
local Core = dofile(sourceDir .. '/modules/client_entergame/oteryn_identity_core.lua')

test('Oteryn PKCE encodes a SHA-256 digest as base64url without padding', function()
  local digest = 'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad'
  assertEqual('ungWv48Bz-pBQUDeXa4iI7ADYaOWF3qctBD_YfIAFa0', Core.pkceChallengeFromSha256Hex(digest))
end)

test('Oteryn callback accepts exact path state and authorization code', function()
  local result, err = Core.parseCallbackTarget('/callback?code=abc123&state=expected', '/callback', 'expected')
  assertNil(err)
  assertEqual('code', result.kind)
  assertEqual('abc123', result.code)
end)

test('Oteryn callback rejects wrong path state and duplicate sensitive parameters', function()
  local result, err = Core.parseCallbackTarget('/wrong?code=abc&state=expected', '/callback', 'expected')
  assertNil(result)
  assertEqual('path_mismatch', err)

  result, err = Core.parseCallbackTarget('/callback?code=abc&state=wrong', '/callback', 'expected')
  assertNil(result)
  assertEqual('state_mismatch', err)

  result, err = Core.parseCallbackTarget('/callback?code=abc&code=def&state=expected', '/callback', 'expected')
  assertNil(result)
  assertEqual('duplicate_parameter', err)
end)

test('Oteryn endpoint policy requires HTTPS except explicit literal loopback development', function()
  assertTrue(Core.isSafeEndpoint('https://identity.example.test/oauth/authorize', false))
  assertFalse(Core.isSafeEndpoint('http://identity.example.test/oauth/authorize', true))
  assertFalse(Core.isSafeEndpoint('http://localhost/oauth/authorize', true))
  assertTrue(Core.isSafeEndpoint('http://127.0.0.1:8080/oauth/authorize', true))
end)

test('Oteryn server support is explicit and protocol versioned', function()
  assertTrue(Core.serverSupportsOteryn({
    authMode = 'oteryn_identity',
    oterynIdentity = { enabled = true, protocolVersion = 1 }
  }))
  assertFalse(Core.serverSupportsOteryn({
    authMode = 'legacy',
    oterynIdentity = { enabled = true, protocolVersion = 1 }
  }))
  assertFalse(Core.serverSupportsOteryn({
    authMode = 'oteryn_identity',
    oterynIdentity = { enabled = true, protocolVersion = 2 }
  }))
end)

test('Oteryn Gateway response maps characters only through authoritative returned world ids', function()
  local normalized, err = Core.normalizeGatewayLoginResponse({
    protocol_version = 1,
    session = { credential = 'session-secret', expires_at = '2026-07-22T10:00:00Z' },
    worlds = {
      { id = 7, slug = 'oteryn-eu', name = 'Oteryn', region = 'EU', host = 'game.example.test', port = 7172 }
    },
    characters = {
      { id = 11, name = 'Alpha', level = 100, vocation = 4, world_id = 7 }
    }
  })

  assertNil(err)
  assertEqual('session-secret', normalized.credential)
  assertEqual('game.example.test', normalized.characters[1].worldIp)
  assertEqual(7172, normalized.characters[1].worldPort)
  assertEqual('Oteryn', normalized.characters[1].worldName)
  assertEqual(7, normalized.characters[1].worldId)
end)

test('Oteryn Gateway response fails closed on unknown world references and duplicate worlds', function()
  local normalized, err = Core.normalizeGatewayLoginResponse({
    protocol_version = 1,
    session = { credential = 'session-secret', expires_at = '2026-07-22T10:00:00Z' },
    worlds = {
      { id = 7, name = 'Oteryn', host = 'game.example.test', port = 7172 }
    },
    characters = {
      { name = 'Alpha', world_id = 8 }
    }
  })
  assertNil(normalized)
  assertEqual('invalid_character', err)

  normalized, err = Core.normalizeGatewayLoginResponse({
    protocol_version = 1,
    session = { credential = 'session-secret', expires_at = '2026-07-22T10:00:00Z' },
    worlds = {
      { id = 7, name = 'Oteryn', host = 'game.example.test', port = 7172 },
      { id = 7, name = 'Duplicate', host = 'other.example.test', port = 7173 }
    },
    characters = {}
  })
  assertNil(normalized)
  assertEqual('invalid_world', err)
end)

test('Oteryn flow lifecycle permits one callback then refuses replay', function()
  local flow = Core.newFlow(1000, 5000)
  assertTrue(Core.consumeCallback(flow))
  assertFalse(Core.consumeCallback(flow))
  assertFalse(Core.cancelFlow(flow))
end)
