/*
 * Copyright (c) 2010-2026 OTClient <https://github.com/edubart/otclient>
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */

#include "game.h"
#include "item.h"
#include "protocolgame.h"
#include "tibiagloballoginwire.h"
#include "framework/net/outputmessage.h"
#include "protocolcodes.h"
#include "thingtypemanager.h"
#include "thingtype.h"
#include "framework/util/crypt.h"

#ifndef USE_PRECOMPILED_HEADERS
#include <algorithm>
#endif

void ProtocolGame::onSend() {}
void ProtocolGame::sendExtendedOpcode(const uint8_t opcode, const std::string& buffer)
{
    if (m_enableSendExtendedOpcode) {
        const auto& msg = std::make_shared<OutputMessage>();
        msg->addU8(Proto::ClientExtendedOpcode);
        msg->addU8(opcode);
        msg->addString(buffer);
        send(msg);
    } else {
        g_logger.error("Unable to send extended opcode {}, extended opcodes are not enabled", opcode);
    }
}

void ProtocolGame::sendLoginPacket(const uint32_t challengeTimestamp, const uint8_t challengeRandom)
{
    const auto& msg = std::make_shared<OutputMessage>();

    const bool currentTibiaGlobalLogin =
        g_game.getClientVersion() == 1532 &&
        g_game.getProtocolVersion() == 1532 &&
        g_game.getFeature(Otc::GameSessionKey) &&
        g_game.getFeature(Otc::GameChallengeOnLogin);

    if (currentTibiaGlobalLogin) {
        // Trusted current writer evidence requires the sequenced >=1405 framing
        // path. Never fall back to the disproven legacy raw/RSA body for this
        // exact-current login mode.
        if (!g_game.getFeature(Otc::GameSequencedPackets)) {
            g_logger.error("Current Tibia Global login requires sequenced packets");
            return;
        }

        generateXteaKey();
        const auto keyBytes = otclient::tibia_global_login::xteaKeyBytes(m_xteaKey);
        const auto wire = otclient::tibia_global_login::encodeLogin(
            challengeTimestamp,
            challengeRandom,
            m_sessionKey,
            m_characterName,
            keyBytes);

        msg->addBytes(std::string_view(
            reinterpret_cast<const char*>(wire.data()),
            wire.size()));

        // Current first login message carries the future XTEA key itself, so
        // it must reach the generic writer before XTEA is enabled. Sequence
        // framing is current and can be enabled for this first message.
        enabledSequencedPackets();
        send(msg);
        enableXteaEncryption();
        return;
    }

    msg->addU8(Proto::ClientPendingGame);
    msg->addU16(g_game.getOs());
    msg->addU16(g_game.getProtocolVersion());

    if (g_game.getFeature(Otc::GameClientVersion))
        msg->addU32(g_game.getClientVersion());

    if (g_game.getClientVersion() >= 1281) {
        msg->addString(std::to_string(g_game.getClientVersion()));
    }

    if (g_game.getClientVersion() >= 1334) {
        msg->addString(g_things.getAssetIdentifier());
    } else if (g_game.getFeature(Otc::GameContentRevision)) {
        msg->addU16(g_things.getContentRevision());
    }

    if (g_game.getFeature(Otc::GamePreviewState))
        msg->addU8(0);

    const int offset = msg->getMessageSize();

    if (g_game.getFeature(Otc::GameLoginPacketEncryption)) {
        // first RSA byte must be 0
        msg->addU8(0);
        // xtea key
        generateXteaKey();
        msg->addU32(m_xteaKey[0]);
        msg->addU32(m_xteaKey[1]);
        msg->addU32(m_xteaKey[2]);
        msg->addU32(m_xteaKey[3]);
    }

    msg->addU8(0); // is gm set?

    if (g_game.getFeature(Otc::GameSessionKey)) {
        msg->addString(m_sessionKey);
        msg->addString(m_characterName);

    } else {
        if (g_game.getFeature(Otc::GameAccountNames))
            msg->addString(m_accountName);
        else
            msg->addU32(stdext::from_string<uint32_t>(m_accountName));

        msg->addString(m_characterName);
        msg->addString(m_accountPassword);

        if (g_game.getFeature(Otc::GameAuthenticator))
            msg->addString(m_authenticatorToken);
    }

    if (g_game.getFeature(Otc::GameChallengeOnLogin)) {
        msg->addU32(challengeTimestamp);
        msg->addU8(challengeRandom);
    }

    const auto& extended = callLuaField<std::string>("getLoginExtendedData");
    if (!extended.empty())
        msg->addString(extended);

    // complete the bytes for rsa encryption with zeros
    const int paddingBytes = g_crypt.rsaGetSize() - (msg->getMessageSize() - offset);
    assert(paddingBytes >= 0);
    msg->addPaddingBytes(paddingBytes);

    // encrypt with RSA
    if (g_game.getFeature(Otc::GameLoginPacketEncryption))
        msg->encryptRsa();

    if (g_game.getFeature(Otc::GameProtocolChecksum))
        enableChecksum();

    send(msg);

    if (g_game.getFeature(Otc::GameLoginPacketEncryption))
        enableXteaEncryption();

    if (g_game.getFeature(Otc::GameSequencedPackets))
        enabledSequencedPackets();
}

void ProtocolGame::sendEnterGame()
{
    const auto& msg = std::make_shared<OutputMessage>();
    msg->addU8(Proto::ClientEnterGame);
    send(msg);
}

void ProtocolGame::sendLogout()
{
    const auto& msg = std::make_shared<OutputMessage>();
    msg->addU8(Proto::ClientLeaveGame);
    send(msg);
}

void ProtocolGame::sendPing()
{
    if (g_game.getFeature(Otc::GameExtendedClientPing))
        sendExtendedOpcode(2, "");
    else {
        const auto& msg = std::make_shared<OutputMessage>();
        msg->addU8(Proto::ClientPing);
        Protocol::send(msg);
    }
}

void ProtocolGame::sendPingBack()
{
    const auto& msg = std::make_shared<OutputMessage>();
    msg->addU8(Proto::ClientPingBack);
    send(msg);
}

void ProtocolGame::sendAutoWalk(const std::vector<Otc::Direction>& path)
{
    const auto& msg = std::make_shared<OutputMessage>();
    msg->addU8(Proto::ClientAutoWalk);
    msg->addU8(path.size());
    for (const Otc::Direction dir : path) {
        uint8_t byte;
        switch (dir) {
            case Otc::East:
                byte = 1;
                break;
            case Otc::NorthEast:
                byte = 2;
                break;
            case Otc::North:
                byte = 3;
                break;
            case Otc::NorthWest:
                byte = 4;
                break;
            case Otc::West:
                byte = 5;
                break;
            case Otc::SouthWest:
                byte = 6;
                break;
            case Otc::South:
                byte = 7;
                break;
            case Otc::SouthEast:
                byte = 8;
                break;
            default:
                byte = 0;
                break;
        }
        msg->addU8(byte);
    }
    send(msg);
}
