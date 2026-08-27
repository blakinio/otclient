#include <client/tibiagloballoginwire.h>

#include <array>
#include <cstdint>
#include <iostream>
#include <string_view>
#include <vector>

namespace
{
void addU8(std::vector<uint8_t>& out, const uint8_t value) { out.push_back(value); }
void addU16(std::vector<uint8_t>& out, const uint16_t value)
{
    out.push_back(static_cast<uint8_t>(value));
    out.push_back(static_cast<uint8_t>(value >> 8));
}
void addU32(std::vector<uint8_t>& out, const uint32_t value)
{
    for (unsigned shift = 0; shift < 32; shift += 8)
        out.push_back(static_cast<uint8_t>(value >> shift));
}
void addString(std::vector<uint8_t>& out, const std::string_view value)
{
    addU16(out, static_cast<uint16_t>(value.size()));
    out.insert(out.end(), value.begin(), value.end());
}
void addLegacyPrefix(std::vector<uint8_t>& legacy, const std::array<uint8_t, 16>& xteaKey)
{
    addU8(legacy, 0x0a);
    addU16(legacy, 10);
    addU16(legacy, 1532);
    addU32(legacy, 1532);
    addString(legacy, "1532");
    addString(legacy, std::string(64, 'a'));
    addU8(legacy, 0);
    addU8(legacy, 0);
    legacy.insert(legacy.end(), xteaKey.begin(), xteaKey.end());
    addU8(legacy, 0);
    addString(legacy, "S");
    addString(legacy, "C");
}
} // namespace

int main()
{
    const std::array<uint32_t, 4> xteaWords{
        0x03020100u,
        0x07060504u,
        0x0b0a0908u,
        0x0f0e0d0cu,
    };
    const std::array<uint8_t, 16> xteaKey{
        0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
        0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f,
    };

    const auto converted = otclient::tibia_global_login::xteaKeyBytes(xteaWords);
    if (converted != xteaKey) {
        std::cerr << "CURRENT_TIBIA_LOGIN_XTEA_KEY_BYTES=FAIL\n";
        return 1;
    }

    const std::vector<uint8_t> expectedChallenge{
        0x08, 0x0a, 0xc2, 0x3e, 0x2a,
        0x08, 0x07, 0x10, 0xfc, 0x0b, 0x18, 0xfc, 0x0b,
        0x22, 0x01, 0x53, 0x2a, 0x01, 0x43, 0x3a, 0x1a,
        0x18, 0xf8, 0xac, 0xd1, 0x91, 0x01, 0x20, 0x5a, 0x2a, 0x10,
        0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
        0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f,
    };
    const std::vector<uint8_t> expectedClientFirst{
        0x08, 0x0a, 0xc2, 0x3e, 0x26,
        0x08, 0x07, 0x10, 0xfc, 0x0b, 0x18, 0xfc, 0x0b,
        0x22, 0x01, 0x53, 0x2a, 0x01, 0x43, 0x3a, 0x16,
        0x18, 0x00, 0x20, 0x00, 0x2a, 0x10,
        0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
        0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f,
    };

    const auto direct = otclient::tibia_global_login::encodeLogin(
        0x12345678u, 0x5au, "S", "C", converted);
    if (direct != expectedChallenge) {
        std::cerr << "CURRENT_TIBIA_LOGIN_WIRE_CONTRACT=FAIL\n";
        return 1;
    }

    std::vector<uint8_t> challengedLegacy;
    addLegacyPrefix(challengedLegacy, xteaKey);
    addU32(challengedLegacy, 0x12345678u);
    addU8(challengedLegacy, 0x5a);
    const auto challenged = otclient::tibia_global_login::transcodeLegacy1532(challengedLegacy, true);
    if (challenged != expectedChallenge) {
        std::cerr << "CURRENT_TIBIA_LOGIN_CHALLENGED_TRANSCODE=FAIL\n";
        return 1;
    }

    std::vector<uint8_t> clientFirstLegacy;
    addLegacyPrefix(clientFirstLegacy, xteaKey);
    const auto clientFirst = otclient::tibia_global_login::transcodeLegacy1532(clientFirstLegacy, false);
    if (clientFirst != expectedClientFirst) {
        std::cerr << "CURRENT_TIBIA_LOGIN_CLIENT_FIRST_TRANSCODE=FAIL actual_size=" << clientFirst.size()
                  << " expected_size=" << expectedClientFirst.size() << '\n';
        return 1;
    }

    std::cout << "CURRENT_TIBIA_LOGIN_XTEA_KEY_BYTES=PASS\n";
    std::cout << "CURRENT_TIBIA_LOGIN_WIRE_CONTRACT=PASS\n";
    std::cout << "CURRENT_TIBIA_LOGIN_CHALLENGED_TRANSCODE=PASS\n";
    std::cout << "CURRENT_TIBIA_LOGIN_CLIENT_FIRST_TRANSCODE=PASS\n";
    return 0;
}
