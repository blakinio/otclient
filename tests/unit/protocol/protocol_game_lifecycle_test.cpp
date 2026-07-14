#include <framework/global.h>

#include <gtest/gtest.h>

#include <client/game.h>
#include <client/protocolgame.h>
#include <client/protocolgamecallbackguard.h>

class GameLifecycleTestAccess
{
public:
    static void setProtocolGame(Game& game, ProtocolGamePtr protocol) { game.m_protocolGame = std::move(protocol); }
    static const ProtocolGamePtr& protocolGame(const Game& game) { return game.m_protocolGame; }
    static void setOnline(Game& game, const bool online) { game.m_online = online; }
    static bool isOnline(const Game& game) { return game.m_online; }

    static void processDisconnect(Game& game, const ProtocolGamePtr& sourceProtocol) { game.processDisconnect(sourceProtocol); }
    static void processConnectionError(Game& game, const ProtocolGamePtr& sourceProtocol, const std::error_code& error)
    {
        game.processConnectionError(sourceProtocol, error);
    }
    static bool processGameEnd(Game& game, const ProtocolGamePtr& sourceProtocol) { return game.processGameEnd(sourceProtocol); }
};

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
    GameLifecycleTestAccess::setProtocolGame(game, replacementProtocol);
    GameLifecycleTestAccess::setOnline(game, false);

    GameLifecycleTestAccess::processDisconnect(game, staleProtocol);

    EXPECT_EQ(GameLifecycleTestAccess::protocolGame(game), replacementProtocol);
}

TEST(ProtocolGameLifecycle, CurrentGameDisconnectClearsCapturedSession)
{
    Game game;
    const auto currentProtocol = std::make_shared<ProtocolGame>();
    GameLifecycleTestAccess::setProtocolGame(game, currentProtocol);
    GameLifecycleTestAccess::setOnline(game, false);

    GameLifecycleTestAccess::processDisconnect(game, currentProtocol);

    EXPECT_FALSE(GameLifecycleTestAccess::protocolGame(game));
}

TEST(ProtocolGameLifecycle, StaleConnectionErrorCannotClearReplacementSession)
{
    Game game;
    const auto staleProtocol = std::make_shared<ProtocolGame>();
    const auto replacementProtocol = std::make_shared<ProtocolGame>();
    GameLifecycleTestAccess::setProtocolGame(game, replacementProtocol);
    GameLifecycleTestAccess::setOnline(game, false);

    GameLifecycleTestAccess::processConnectionError(game, staleProtocol, asio::error::eof);

    EXPECT_EQ(GameLifecycleTestAccess::protocolGame(game), replacementProtocol);
}

TEST(ProtocolGameLifecycle, CurrentConnectionErrorClearsCapturedSession)
{
    Game game;
    const auto currentProtocol = std::make_shared<ProtocolGame>();
    GameLifecycleTestAccess::setProtocolGame(game, currentProtocol);
    GameLifecycleTestAccess::setOnline(game, false);

    GameLifecycleTestAccess::processConnectionError(game, currentProtocol, asio::error::eof);

    EXPECT_FALSE(GameLifecycleTestAccess::protocolGame(game));
}

TEST(ProtocolGameLifecycle, StaleGameEndCannotMutateReplacementState)
{
    Game game;
    const auto staleProtocol = std::make_shared<ProtocolGame>();
    const auto replacementProtocol = std::make_shared<ProtocolGame>();
    GameLifecycleTestAccess::setProtocolGame(game, replacementProtocol);
    GameLifecycleTestAccess::setOnline(game, true);

    const auto ended = GameLifecycleTestAccess::processGameEnd(game, staleProtocol);

    EXPECT_FALSE(ended);
    EXPECT_TRUE(GameLifecycleTestAccess::isOnline(game));
    EXPECT_EQ(GameLifecycleTestAccess::protocolGame(game), replacementProtocol);
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
