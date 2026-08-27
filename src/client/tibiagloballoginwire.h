#pragma once

#include <array>
#include <cstdint>
#include <string_view>
#include <vector>

namespace otclient::tibia_global_login
{
namespace detail
{
inline void appendVarint(std::vector<uint8_t>& out, uint64_t value)
{
    while (value >= 0x80) {
        out.push_back(static_cast<uint8_t>((value & 0x7f) | 0x80));
        value >>= 7;
    }
    out.push_back(static_cast<uint8_t>(value));
}

inline void appendTag(std::vector<uint8_t>& out, const uint32_t fieldNumber, const uint8_t wireType)
{
    appendVarint(out, (static_cast<uint64_t>(fieldNumber) << 3) | wireType);
}

inline void appendVarintField(std::vector<uint8_t>& out, const uint32_t fieldNumber, const uint64_t value)
{
    appendTag(out, fieldNumber, 0);
    appendVarint(out, value);
}

inline void appendBytesField(std::vector<uint8_t>& out, const uint32_t fieldNumber, const std::string_view bytes)
{
    appendTag(out, fieldNumber, 2);
    appendVarint(out, bytes.size());
    for (const char byte : bytes)
        out.push_back(static_cast<uint8_t>(byte));
}

inline void appendMessageField(std::vector<uint8_t>& out, const uint32_t fieldNumber, const std::vector<uint8_t>& message)
{
    appendTag(out, fieldNumber, 2);
    appendVarint(out, message.size());
    out.insert(out.end(), message.begin(), message.end());
}
} // namespace detail

inline std::vector<uint8_t> encodeLogin(
    const uint32_t challengeTimestamp,
    const uint32_t challengeRandom,
    const std::string_view sessionKey,
    const std::string_view characterName,
    const std::array<uint8_t, 16>& xteaKey)
{
    // Exact-current LoginRSAEncryptedBlock subset whose value provenance is
    // available to Track B: challenge values and the 16-byte XTEA key.
    std::vector<uint8_t> protectedBlock;
    protectedBlock.reserve(32);
    detail::appendVarintField(protectedBlock, 3, challengeTimestamp);
    detail::appendVarintField(protectedBlock, 4, challengeRandom);
    detail::appendBytesField(
        protectedBlock,
        5,
        std::string_view(reinterpret_cast<const char*>(xteaKey.data()), xteaKey.size()));

    // Exact current GameclientMessageLogin wire shape. Field 4/5 consume the
    // existing authorized Track B retained-session and selected-character
    // values. Unsupported descriptor/user-facing names remain deliberately
    // unspecified outside this compatibility seam.
    std::vector<uint8_t> login;
    login.reserve(sessionKey.size() + characterName.size() + protectedBlock.size() + 32);
    detail::appendVarintField(login, 1, 7);       // exact Linux current value
    detail::appendVarintField(login, 2, 1532);    // exact current client value
    detail::appendVarintField(login, 3, 1532);    // exact current normalized build value
    detail::appendBytesField(login, 4, sessionKey);
    detail::appendBytesField(login, 5, characterName);
    detail::appendMessageField(login, 7, protectedBlock);

    // Exact current top-level envelope: message type 10 plus field 1000 login.
    std::vector<uint8_t> envelope;
    envelope.reserve(login.size() + 8);
    detail::appendVarintField(envelope, 1, 10);
    detail::appendMessageField(envelope, 1000, login);
    return envelope;
}
} // namespace otclient::tibia_global_login
