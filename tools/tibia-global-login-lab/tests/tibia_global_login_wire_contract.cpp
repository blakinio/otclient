#include <client/tibiagloballoginwire.h>

#include <array>
#include <cstdint>
#include <iostream>
#include <vector>

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

    const auto actual = otclient::tibia_global_login::encodeLogin(
        0x12345678u,
        0x5au,
        "S",
        "C",
        converted);

    const std::vector<uint8_t> expected{
        0x08, 0x0a, 0xc2, 0x3e, 0x2a,
        0x08, 0x07, 0x10, 0xfc, 0x0b, 0x18, 0xfc, 0x0b,
        0x22, 0x01, 0x53, 0x2a, 0x01, 0x43, 0x3a, 0x1a,
        0x18, 0xf8, 0xac, 0xd1, 0x91, 0x01, 0x20, 0x5a, 0x2a, 0x10,
        0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
        0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f,
    };

    if (actual == expected) {
        std::cout << "CURRENT_TIBIA_LOGIN_XTEA_KEY_BYTES=PASS\n";
        std::cout << "CURRENT_TIBIA_LOGIN_WIRE_CONTRACT=PASS\n";
        return 0;
    }

    std::cerr << "CURRENT_TIBIA_LOGIN_WIRE_CONTRACT=FAIL actual_size=" << actual.size()
              << " expected_size=" << expected.size() << '\n';
    return 1;
}
