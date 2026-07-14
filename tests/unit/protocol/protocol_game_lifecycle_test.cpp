#include <framework/global.h>

#include <gtest/gtest.h>

#include <client/protocolgame.h>
#include <client/protocolgamecallbackguard.h>

TEST(ProtocolGameLifecycle, StaleCallbackCannotMutateReplacementSession)
{
    const auto firstProtocol = std::make_shared<ProtocolGame>();
    const auto secondProtocol = std::make_shared<ProtocolGame>();
    ProtocolGamePtr currentProtocol = firstProtocol;
    bool callbackInvoked = false;

    currentProtocol = secondProtocol;

    const auto staleHandled = otclient::detail::runIfCurrentProtocolGame(firstProtocol, currentProtocol, [&] {
        callbackInvoked = true;
        currentProtocol.reset();
    });

    EXPECT_FALSE(staleHandled);
    EXPECT_FALSE(callbackInvoked);
    EXPECT_EQ(currentProtocol, secondProtocol);
}

TEST(ProtocolGameLifecycle, CurrentCallbackStillRunsAndDuplicateBecomesStale)
{
    const auto current = std::make_shared<ProtocolGame>();
    ProtocolGamePtr currentProtocol = current;
    int callbackCount = 0;

    const auto currentHandled = otclient::detail::runIfCurrentProtocolGame(current, currentProtocol, [&] {
        ++callbackCount;
        currentProtocol.reset();
    });

    EXPECT_TRUE(currentHandled);
    EXPECT_EQ(callbackCount, 1);
    EXPECT_FALSE(currentProtocol);

    const auto duplicateHandled = otclient::detail::runIfCurrentProtocolGame(current, currentProtocol, [&] {
        ++callbackCount;
    });

    EXPECT_FALSE(duplicateHandled);
    EXPECT_EQ(callbackCount, 1);
}

TEST(ProtocolGameLifecycle, NullSourceIsIgnored)
{
    const auto currentProtocol = std::make_shared<ProtocolGame>();
    ProtocolGamePtr sourceProtocol;
    bool callbackInvoked = false;

    const auto handled = otclient::detail::runIfCurrentProtocolGame(sourceProtocol, currentProtocol, [&] {
        callbackInvoked = true;
    });

    EXPECT_FALSE(handled);
    EXPECT_FALSE(callbackInvoked);
}
