#include "input_message_builder.h"

#include <limits>
#include <stdexcept>
#include <string>

namespace otclient::test {

InputMessageBuilder& InputMessageBuilder::addU8(const uint8_t value)
{
    m_bytes.push_back(value);
    return *this;
}

InputMessageBuilder& InputMessageBuilder::addU16(const uint16_t value)
{
    m_bytes.push_back(static_cast<uint8_t>(value));
    m_bytes.push_back(static_cast<uint8_t>(value >> 8));
    return *this;
}

InputMessageBuilder& InputMessageBuilder::addU32(const uint32_t value)
{
    for (unsigned shift = 0; shift < 32; shift += 8)
        m_bytes.push_back(static_cast<uint8_t>(value >> shift));
    return *this;
}

InputMessageBuilder& InputMessageBuilder::addU64(const uint64_t value)
{
    for (unsigned shift = 0; shift < 64; shift += 8)
        m_bytes.push_back(static_cast<uint8_t>(value >> shift));
    return *this;
}

InputMessageBuilder& InputMessageBuilder::addString(const std::string_view value)
{
    if (value.size() > std::numeric_limits<uint16_t>::max())
        throw std::length_error("InputMessage string fixture exceeds U16 length");

    addU16(static_cast<uint16_t>(value.size()));
    m_bytes.insert(m_bytes.end(), value.begin(), value.end());
    return *this;
}

InputMessageBuilder& InputMessageBuilder::addPosition(const Position& position)
{
    return addU16(static_cast<uint16_t>(position.x))
        .addU16(static_cast<uint16_t>(position.y))
        .addU8(position.z);
}

InputMessageBuilder& InputMessageBuilder::addBytes(const std::initializer_list<uint8_t> values)
{
    m_bytes.insert(m_bytes.end(), values);
    return *this;
}

InputMessagePtr InputMessageBuilder::build() const
{
    const std::string buffer(m_bytes.begin(), m_bytes.end());
    auto message = std::make_shared<InputMessage>();
    message->setBuffer(buffer);
    message->setReadPos(static_cast<uint16_t>(message->getMaxHeaderSize()));
    return message;
}

} // namespace otclient::test
