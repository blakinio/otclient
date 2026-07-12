#pragma once

#include <framework/net/inputmessage.h>

#include <gtest/gtest.h>

namespace otclient::test {

inline testing::AssertionResult cursorIs(const InputMessage& message, const int expected)
{
    const auto& mutableMessage = const_cast<InputMessage&>(message);
    if (mutableMessage.getReadPos() == expected)
        return testing::AssertionSuccess();
    return testing::AssertionFailure() << "expected readPos " << expected
                                       << ", got " << mutableMessage.getReadPos();
}

inline testing::AssertionResult unreadIs(const InputMessage& message, const int expected)
{
    const auto& mutableMessage = const_cast<InputMessage&>(message);
    if (mutableMessage.getUnreadSize() == expected)
        return testing::AssertionSuccess();
    return testing::AssertionFailure() << "expected " << expected
                                       << " unread bytes, got " << mutableMessage.getUnreadSize();
}

inline testing::AssertionResult consumed(const InputMessage& message)
{
    const auto& mutableMessage = const_cast<InputMessage&>(message);
    if (mutableMessage.getUnreadSize() == 0 && mutableMessage.eof())
        return testing::AssertionSuccess();
    return testing::AssertionFailure() << "message is not fully consumed: unread="
                                       << mutableMessage.getUnreadSize();
}

} // namespace otclient::test
