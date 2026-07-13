#pragma once

#include <client/position.h>
#include <framework/net/inputmessage.h>

#include <cstdint>
#include <initializer_list>
#include <memory>
#include <string_view>
#include <vector>

namespace otclient::test {

class InputMessageBuilder
{
public:
    InputMessageBuilder& addU8(uint8_t value);
    InputMessageBuilder& addU16(uint16_t value);
    InputMessageBuilder& addU32(uint32_t value);
    InputMessageBuilder& addU64(uint64_t value);
    InputMessageBuilder& addString(std::string_view value);
    InputMessageBuilder& addPosition(const Position& position);
    InputMessageBuilder& addBytes(std::initializer_list<uint8_t> values);

    [[nodiscard]] InputMessagePtr build() const;
    [[nodiscard]] const std::vector<uint8_t>& bytes() const { return m_bytes; }

private:
    std::vector<uint8_t> m_bytes;
};

} // namespace otclient::test
