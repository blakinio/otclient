#pragma once

#include <framework/net/outputmessage.h>

#include <gtest/gtest.h>

#include <cstdint>
#include <initializer_list>
#include <vector>

namespace otclient::test {

class OutputMessageInspector
{
public:
    explicit OutputMessageInspector(const OutputMessage& message) : m_message(message) {}

    [[nodiscard]] std::vector<uint8_t> bytes() const
    {
        const auto buffer = const_cast<OutputMessage&>(m_message).getBuffer();
        return { buffer.begin(), buffer.end() };
    }

    testing::AssertionResult equals(const std::initializer_list<uint8_t> expected) const
    {
        const auto actual = bytes();
        if (actual == std::vector<uint8_t>(expected))
            return testing::AssertionSuccess();

        return testing::AssertionFailure()
            << "wire bytes differ (expected " << expected.size()
            << " bytes, got " << actual.size() << ')';
    }

private:
    const OutputMessage& m_message;
};

} // namespace otclient::test
