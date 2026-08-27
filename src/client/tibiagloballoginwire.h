#pragma once

#include <array>
#include <cstdint>
#include <string_view>
#include <vector>

namespace otclient::tibia_global_login
{
inline std::vector<uint8_t> encodeLogin(
    uint32_t challengeTimestamp,
    uint32_t challengeRandom,
    std::string_view sessionKey,
    std::string_view characterName,
    const std::array<uint8_t, 16>& xteaKey)
{
    (void)challengeTimestamp;
    (void)challengeRandom;
    (void)sessionKey;
    (void)characterName;
    (void)xteaKey;
    return {};
}
} // namespace otclient::tibia_global_login
