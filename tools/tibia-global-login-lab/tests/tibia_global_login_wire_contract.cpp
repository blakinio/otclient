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

    const std::vector<uint8_t> expected{
        0x08, 0x0a, 0xc2, 0x3e, 0x2a,
        0x08, 0x07, 0x10, 0xfc, 0x0b, 0x18, 0xfc, 0x0b,
        0x22, 0x01, 0x53, 0x2a, 0x01, 0x43, 0x3a, 0x1a,
        0x18, 0xf8, 0xac, 0xd1, 0x91, 0x01, 0x20, 0x5a, 0x2a, 0x10,
        0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
        0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f,
    };

    const auto direct = otclient::tibia_global_login::encodeLogin(
        0x12345678u, 0x5au, "S", "C", converted);
    if (direct != expected) {
        std::cerr << "CURRENT_TIBIA_LOGIN_WIRE_CONTRACT=FAIL actual_size=" << direct.size()
                  << " expected_size=" << expected.size() << '\n';
        return 1;
    }

    std::vector<uint8_t> legacy;
    addU8(legacy, 0x0a);       // historical pending-game opcode
    addU16(legacy, 10);        // OTClient Linux OS value
    addU16(legacy, 1532);      // protocol version
    addU32(legacy, 1532);      // client version
    addString(legacy, "1532");
    addString(legacy, std::string(64, 'a'));
    addU8(legacy, 0);          // preview
    addU8(legacy, 0);          // historical RSA zero byte
    legacy.insert(legacy.end(), xteaKey.begin(), xteaKey.end());
    addU8(legacy, 0);          // historical GM byte
    addString(legacy, "S");
    addString(legacy, "C");
    addU32(legacy, 0x12345678u);
    addU8(legacy, 0x5a);

    const auto transcoded = otclient::tibia_global_login::transcodeLegacy1532(legacy);
    if (transcoded != expected) {
        std::cerr << "CURRENT_TIBIA_LOGIN_TRANSCODE=FAIL actual_size=" << transcoded.size()
                  << " expected_size=" << expected.size() << '\n';
        return 1;
    }

    std::cout << "CURRENT_TIBIA_LOGIN_XTEA_KEY_BYTES=PASS\n";
    std::cout << "CURRENT_TIBIA_LOGIN_WIRE_CONTRACT=PASS\n";
    std::cout << "CURRENT_TIBIA_LOGIN_TRANSCODE=PASS\n";
    return 0;
}
