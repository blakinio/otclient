#pragma once

#include <framework/net/inputmessage.h>

#include <gtest/gtest.h>

namespace otclient::test {

inline testing::AssertionResult cursorIs(InputMessage& message, const int expected)
{
    if (message.getReadPos() == expected)
        return testing::AssertionSuccess();
    return testing::AssertionFailure() << "expected readPos " << expected
                                       << ", got " << message.getReadPos();
}

inline testing::AssertionResult unreadIs(InputMessage& message, const int expected)
{
    if (message.getUnreadSize() == expected)
        return testing::AssertionSuccess();
    return testing::AssertionFailure() << "expected " << expected
                                       << " unread bytes, got " << message.getUnreadSize();
}

inline testing::AssertionResult consumed(InputMessage& message)
{
    if (message.getUnreadSize() == 0 && message.eof())
        return testing::AssertionSuccess();
    return testing::AssertionFailure() << "message is not fully consumed: unread="
                                       << message.getUnreadSize();
}

} // namespace otclient::test
