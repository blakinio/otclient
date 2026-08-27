from pathlib import Path

root = Path(__file__).resolve().parents[3]
output = (root / 'src/framework/net/outputmessage.cpp').read_text(encoding='utf-8')
protocol = (root / 'src/framework/net/protocol.cpp').read_text(encoding='utf-8')
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

# The first typed login packet uses the current sequence framing even though
# the legacy builder enables its normal sequenced mode after send().
assert 'isCurrentTibiaGlobalLoginEnvelope' in protocol
assert 'currentTibiaGlobalLoginEnvelope || m_sequencedPackets' in protocol
assert 'outputMessage->writeSequence(m_packetNumber++)' in protocol

print('CURRENT_TIBIA_LOGIN_SEND_INTEGRATION_CONTRACT=PASS')
