from pathlib import Path

root = Path(__file__).resolve().parents[3]
output = (root / 'src/framework/net/outputmessage.cpp').read_text(encoding='utf-8')
protocol_game = (root / 'src/client/protocolgame.cpp').read_text(encoding='utf-8')
senders = (root / 'src/client/protocolgamesend.cpp').read_text(encoding='utf-8')

# Regression guard for the accidental whole-file truncation failure mode.
assert len(senders) > 50_000, len(senders)
assert 'void ProtocolGame::sendRequestChannels()' in senders
assert 'void ProtocolGame::sendApplyWheelPoints(' in senders

# Exact-current application body replaces the legacy RSA block before the
# generic transport layer, without changing the legacy builder for other modes.
assert '#include "client/tibiagloballoginwire.h"' in output
assert 'transcodeLegacy1532' in output
assert 'g_game.getFeature(Otc::GameChallengeOnLogin)' in output
assert 'CURRENT_TIBIA_GLOBAL_LOGIN_TRANSCODE' in output
assert 'g_crypt.rsaEncrypt' in output

# Durable Track B evidence disproved server-first challenge behavior for the
# selected endpoint. Exact 15.32 retained-session mode therefore starts sequence
# framing at connect and remains client-first when GameChallengeOnLogin is off.
assert 'currentTibiaGlobalLoginTransport' in protocol_game
assert 'g_game.getClientVersion() == 1532' in protocol_game
assert 'g_game.getProtocolVersion() == 1532' in protocol_game
assert 'g_game.getFeature(Otc::GameSessionKey)' in protocol_game
assert 'g_game.getFeature(Otc::GameSequencedPackets)' in protocol_game
assert 'enabledSequencedPackets();' in protocol_game
assert 'else if (g_game.getFeature(Otc::GameProtocolChecksum))' in protocol_game
assert 'if (!g_game.getFeature(Otc::GameChallengeOnLogin))' in protocol_game
assert 'sendLoginPacket(0, 0);' in protocol_game

# Modern XTEA framing consumes the padding-count byte in Protocol::xteaDecrypt.
# The first ProtocolGame receive must not consume the same byte a second time.
protocol = (root / 'src/framework/net/protocol.cpp').read_text(encoding='utf-8')
protocol_h = (root / 'src/framework/net/protocol.h').read_text(encoding='utf-8')
assert 'const uint8_t paddingSize = inputMessage->getU8();' in protocol
assert 'bool isXteaEncryptionEnabled() const' in protocol_h
assert 'if (!isXteaEncryptionEnabled())' in protocol_game
print('CURRENT_TIBIA_LOGIN_SEND_INTEGRATION_CONTRACT=PASS')
