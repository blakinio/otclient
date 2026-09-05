#pragma once

#include <array>
#include <cstddef>
#include <cstdint>
#include <span>
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

inline bool readU8(const std::span<const uint8_t> bytes, std::size_t& pos, uint8_t& value)
{
    if (pos >= bytes.size())
        return false;
    value = bytes[pos++];
    return true;
}

inline bool readU16(const std::span<const uint8_t> bytes, std::size_t& pos, uint16_t& value)
{
    if (bytes.size() - pos < 2)
        return false;
    value = static_cast<uint16_t>(bytes[pos]) |
            (static_cast<uint16_t>(bytes[pos + 1]) << 8);
    pos += 2;
    return true;
}

inline bool readU32(const std::span<const uint8_t> bytes, std::size_t& pos, uint32_t& value)
{
    if (bytes.size() - pos < 4)
        return false;
    value = static_cast<uint32_t>(bytes[pos]) |
            (static_cast<uint32_t>(bytes[pos + 1]) << 8) |
            (static_cast<uint32_t>(bytes[pos + 2]) << 16) |
            (static_cast<uint32_t>(bytes[pos + 3]) << 24);
    pos += 4;
    return true;
}

inline bool readString(const std::span<const uint8_t> bytes, std::size_t& pos, std::string_view& value)
{
    uint16_t size = 0;
    if (!readU16(bytes, pos, size) || bytes.size() - pos < size)
        return false;
    value = std::string_view(
        reinterpret_cast<const char*>(bytes.data() + pos), size);
    pos += size;
    return true;
}
} // namespace detail

inline std::array<uint8_t, 16> xteaKeyBytes(const std::array<uint32_t, 4>& words)
{
    std::array<uint8_t, 16> bytes{};
    for (std::size_t wordIndex = 0; wordIndex < words.size(); ++wordIndex) {
        for (std::size_t byteIndex = 0; byteIndex < sizeof(uint32_t); ++byteIndex) {
            bytes[wordIndex * sizeof(uint32_t) + byteIndex] =
                static_cast<uint8_t>((words[wordIndex] >> (byteIndex * 8)) & 0xffu);
        }
    }
    return bytes;
}

inline std::vector<uint8_t> encodeLogin(
    const uint32_t challengeTimestamp,
    const uint32_t challengeRandom,
    const std::string_view sessionKey,
    const std::string_view characterName,
    const std::array<uint8_t, 16>& xteaKey)
{
    std::vector<uint8_t> protectedBlock;
    protectedBlock.reserve(32);
    detail::appendVarintField(protectedBlock, 3, challengeTimestamp);
    detail::appendVarintField(protectedBlock, 4, challengeRandom);
    detail::appendBytesField(
        protectedBlock,
        5,
        std::string_view(reinterpret_cast<const char*>(xteaKey.data()), xteaKey.size()));

    std::vector<uint8_t> login;
    login.reserve(sessionKey.size() + characterName.size() + protectedBlock.size() + 32);
    detail::appendVarintField(login, 1, 7);
    detail::appendVarintField(login, 2, 1532);
    detail::appendVarintField(login, 3, 1532);
    detail::appendBytesField(login, 4, sessionKey);
    detail::appendBytesField(login, 5, characterName);
    detail::appendMessageField(login, 7, protectedBlock);

    std::vector<uint8_t> envelope;
    envelope.reserve(login.size() + 8);
    detail::appendVarintField(envelope, 1, 10);
    detail::appendMessageField(envelope, 1000, login);
    return envelope;
}

inline std::vector<uint8_t> transcodeLegacy1532(
    const std::span<const uint8_t> legacy,
    const bool challengeOnLogin)
{
    std::size_t pos = 0;
    uint8_t opcode = 0;
    uint16_t os = 0;
    uint16_t protocolVersion = 0;
    uint32_t clientVersion = 0;
    std::string_view versionString;
    std::string_view assetIdentifier;
    uint8_t preview = 0;
    uint8_t rsaZero = 0;
    uint8_t gm = 0;
    std::string_view retainedValue;
    std::string_view selectedCharacter;
    uint32_t challengeTimestamp = 0;
    uint8_t challengeRandom = 0;

    if (!detail::readU8(legacy, pos, opcode) || opcode != 0x0a ||
        !detail::readU16(legacy, pos, os) ||
        !detail::readU16(legacy, pos, protocolVersion) || protocolVersion != 1532 ||
        !detail::readU32(legacy, pos, clientVersion) || clientVersion != 1532 ||
        !detail::readString(legacy, pos, versionString) || versionString != "1532" ||
        !detail::readString(legacy, pos, assetIdentifier) || assetIdentifier.size() != 64 ||
        !detail::readU8(legacy, pos, preview) ||
        !detail::readU8(legacy, pos, rsaZero) || rsaZero != 0) {
        return {};
    }

    (void)os;
    (void)preview;

    if (legacy.size() - pos < 16)
        return {};
    std::array<uint8_t, 16> xteaKey{};
    for (std::size_t i = 0; i < xteaKey.size(); ++i)
        xteaKey[i] = legacy[pos + i];
    pos += xteaKey.size();

    if (!detail::readU8(legacy, pos, gm) || gm != 0 ||
        !detail::readString(legacy, pos, retainedValue) || retainedValue.empty() ||
        !detail::readString(legacy, pos, selectedCharacter) || selectedCharacter.empty()) {
        return {};
    }

    if (challengeOnLogin &&
        (!detail::readU32(legacy, pos, challengeTimestamp) ||
         !detail::readU8(legacy, pos, challengeRandom))) {
        return {};
    }

    return encodeLogin(
        challengeTimestamp,
        challengeRandom,
        retainedValue,
        selectedCharacter,
        xteaKey);
}
} // namespace otclient::tibia_global_login
