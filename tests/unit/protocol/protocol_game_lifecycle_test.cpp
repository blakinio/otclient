#include <framework/global.h>

#include <gtest/gtest.h>

#define private public
#define protected public
#include <client/game.h>
#undef protected
#undef private

#include <client/protocolgame.h>
#include <client/protocolgamecallbackguard.h>

TEST(ProtocolGameLifecycle, StaleCallbackCannotMutateReplacementSession)
{
    const auto firstProtocol = std::make_shared<ProtocolGame>();
    const auto secondProtocol = std::make_shared<ProtocolGame>();
    ProtocolGamePtr currentProtocol = secondProtocol;
    bool callbackInvoked = false;

    const auto staleHandled = otclient::detail::runIfCurrentProtocolGame(firstProtocol, currentProtocol, [&] {
        callbackInvoked = true;
        currentProtocol.reset();
    });

    EXPECT_FALSE(staleHandled);
    EXPECT_FALSE(callbackInvoked);
    EXPECT_EQ(currentProtocol, secondProtocol);
}

TEST(ProtocolGameLifecycle, CallbackReplacementIsDetectedAfterReentrantBoundary)
{
    const auto firstProtocol = std::make_shared<ProtocolGame>();
    const auto secondProtocol = std::make_shared<ProtocolGame>();
    ProtocolGamePtr currentProtocol = firstProtocol;
    bool callbackInvoked = false;

    const auto remainedCurrent = otclient::detail::runWhileCurrentProtocolGame(
        firstProtocol,
        [&] { return currentProtocol; },
        [&] {
            callbackInvoked = true;
            currentProtocol = secondProtocol;
        });

    EXPECT_FALSE(remainedCurrent);
    EXPECT_TRUE(callbackInvoked);
    EXPECT_EQ(currentProtocol, secondProtocol);
}

TEST(ProtocolGameLifecycle, CurrentCallbackWithoutReplacementRemainsCurrent)
{
    const auto current = std::make_shared<ProtocolGame>();
    ProtocolGamePtr currentProtocol = current;
    int callbackCount = 0;

    const auto remainedCurrent = otclient::detail::runWhileCurrentProtocolGame(
        current,
        [&] { return currentProtocol; },
        [&] { ++callbackCount; });

    EXPECT_TRUE(remainedCurrent);
    EXPECT_EQ(callbackCount, 1);
    EXPECT_EQ(currentProtocol, current);
}

TEST(ProtocolGameLifecycle, StaleGameDisconnectCannotClearReplacementSession)
{
    Game game;
    const auto staleProtocol = std::make_shared<ProtocolGame>();
    const auto replacementProtocol = std::make_shared<ProtocolGame>();
    game.m_protocolGame = replacementProtocol;
    game.m_online = false;

    game.processDisconnect(staleProtocol);

    EXPECT_EQ(game.m_protocolGame, replacementProtocol);
}

TEST(ProtocolGameLifecycle, CurrentGameDisconnectClearsCapturedSession)
{
    Game game;
    const auto currentProtocol = std::make_shared<ProtocolGame>();
    game.m_protocolGame = currentProtocol;
    game.m_online = false;

    game.processDisconnect(currentProtocol);

    EXPECT_FALSE(game.m_protocolGame);
}

TEST(ProtocolGameLifecycle, StaleConnectionErrorCannotClearReplacementSession)
{
    Game game;
    const auto staleProtocol = std::make_shared<ProtocolGame>();
    const auto replacementProtocol = std::make_shared<ProtocolGame>();
    game.m_protocolGame = replacementProtocol;
    game.m_online = false;

    game.processConnectionError(staleProtocol, asio::error::eof);

    EXPECT_EQ(game.m_protocolGame, replacementProtocol);
}

TEST(ProtocolGameLifecycle, CurrentConnectionErrorClearsCapturedSession)
{
    Game game;
    const auto currentProtocol = std::make_shared<ProtocolGame>();
    game.m_protocolGame = currentProtocol;
    game.m_online = false;

    game.processConnectionError(currentProtocol, asio::error::eof);

    EXPECT_FALSE(game.m_protocolGame);
}

TEST(ProtocolGameLifecycle, StaleGameEndCannotMutateReplacementState)
{
    Game game;
    const auto staleProtocol = std::make_shared<ProtocolGame>();
    const auto replacementProtocol = std::make_shared<ProtocolGame>();
    game.m_protocolGame = replacementProtocol;
    game.m_online = true;

    const auto ended = game.processGameEnd(staleProtocol);

    EXPECT_FALSE(ended);
    EXPECT_TRUE(game.m_online);
    EXPECT_EQ(game.m_protocolGame, replacementProtocol);
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
