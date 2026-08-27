#include <client/tibiagloballoginwire.h>

#include <array>
#include <cstdint>
#include <iostream>
#include <vector>

int main()
{
    std::array<uint8_t, 16> xteaKey{};
    for (uint8_t i = 0; i < xteaKey.size(); ++i)
        xteaKey[i] = i;

    const auto actual = otclient::tibia_global_login::encodeLogin(
        0x12345678u,
        0x5au,
        "S",
        "C",
        xteaKey);

    const std::vector<uint8_t> expected{
        0x08, 0x0a, 0xc2, 0x3e, 0x2a,
        0x08, 0x07, 0x10, 0xfc, 0x0b, 0x18, 0xfc, 0x0b,
        0x22, 0x01, 0x53, 0x2a, 0x01, 0x43, 0x3a, 0x1a,
        0x18, 0xf8, 0xac, 0xd1, 0x91, 0x01, 0x20, 0x5a, 0x2a, 0x10,
        0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07,
        0x08, 0x09, 0x0a, 0x0b, 0x0c, 0x0d, 0x0e, 0x0f,
    };

    if (actual == expected) {
        std::cout << "CURRENT_TIBIA_LOGIN_WIRE_CONTRACT=PASS\n";
        return 0;
    }

    std::cerr << "CURRENT_TIBIA_LOGIN_WIRE_CONTRACT=FAIL actual_size=" << actual.size()
              << " expected_size=" << expected.size() << '\n';
    return 1;
}
