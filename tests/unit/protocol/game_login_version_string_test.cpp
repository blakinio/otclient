#include <gtest/gtest.h>

#include <client/gameconfig.h>

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
