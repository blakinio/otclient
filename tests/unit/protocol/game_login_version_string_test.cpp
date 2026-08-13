#include <gtest/gtest.h>

#include <client/client.h>
#include <client/gameconfig.h>
#include <framework/luaengine/luainterface.h>

TEST(GameLoginVersionString, FallsBackToNumericClientVersionWhenUnset)
{
    GameConfig config;

    EXPECT_EQ(config.getGameLoginVersionString(1532), "1532");
}

TEST(GameLoginVersionString, UsesConfiguredFullClientVersionForSerialization)
{
    GameConfig config;
    config.setClientVersionString("15.32.df7b29");

    EXPECT_EQ(config.getGameLoginVersionString(1532), "15.32.df7b29");
}

TEST(GameLoginVersionString, LuaSingletonBindingSetsAndReadsFullVersion)
{
    g_lua.init();
    Client::registerLuaFunctions();

    EXPECT_NO_THROW(g_lua.runBuffer(R"lua(
        g_gameConfig.setClientVersionString('15.32.df7b29')
        assert(g_gameConfig.getClientVersionString() == '15.32.df7b29')
    )lua", "game-login-version-binding-test"));
    EXPECT_EQ(g_gameConfig.getClientVersionString(), "15.32.df7b29");

    g_gameConfig.setClientVersionString({});
    g_lua.terminate();
}
