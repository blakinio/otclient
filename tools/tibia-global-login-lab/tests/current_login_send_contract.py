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
assert 'CURRENT_TIBIA_GLOBAL_LOGIN_TRANSCODE' in output
assert 'g_crypt.rsaEncrypt' in output

# Exact current 15.32 is challenge-driven and uses sequence framing from the
# connection start, so the first server challenge and first typed login share
# the same framing mode. Legacy modes keep their checksum behavior.
assert 'currentTibiaGlobalLoginTransport' in protocol_game
assert 'g_game.getClientVersion() == 1532' in protocol_game
assert 'g_game.getProtocolVersion() == 1532' in protocol_game
assert 'g_game.getFeature(Otc::GameChallengeOnLogin)' in protocol_game
assert 'g_game.getFeature(Otc::GameSequencedPackets)' in protocol_game
assert 'enabledSequencedPackets();' in protocol_game
assert 'else if (g_game.getFeature(Otc::GameProtocolChecksum))' in protocol_game

print('CURRENT_TIBIA_LOGIN_SEND_INTEGRATION_CONTRACT=PASS')
