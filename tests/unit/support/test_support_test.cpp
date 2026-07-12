#include <framework/pch.h>

#include <gtest/gtest.h>

#include "support/mocks/fake_game_state.h"
#include "support/mocks/fake_protocol_callback_receiver.h"
#include "support/mocks/fake_resources.h"
#include "support/test_environment/test_environment.h"

#include <framework/core/resourcemanager.h>

namespace otclient::test {

TEST(TestEnvironment, RemovesMountedResourcesWhenDestroyed)
{
    const auto root = std::filesystem::current_path();
    const auto before = g_resources.getSearchPaths();

    {
        TestEnvironment environment(root);
        EXPECT_EQ(before.size() + 1, g_resources.getSearchPaths().size());
        environment.reset();
        EXPECT_EQ(1U, environment.generation());
    }

    EXPECT_EQ(before, g_resources.getSearchPaths());
}

TEST(TestEnvironment, ConsecutiveInstancesDoNotShareMutableGeneration)
{
    const auto root = std::filesystem::current_path();
    {
        TestEnvironment first(root);
        first.reset();
        first.reset();
        EXPECT_EQ(2U, first.generation());
    }
    {
        TestEnvironment second(root);
        EXPECT_EQ(0U, second.generation());
    }
}

TEST(FakeResources, LoadsTheSameFixtureDeterministically)
{
    FakeResources resources;
    resources.add("packets/world-light.hex", "82 FF 00");

    EXPECT_EQ("82 FF 00", resources.read("packets/world-light.hex"));
    EXPECT_EQ(resources.read("packets/world-light.hex"), resources.read("packets/world-light.hex"));
}

TEST(FakeGameState, ResetClearsLocalPlayerResourceBalances)
{
    FakeLocalPlayer player;
    player.setResource(Otc::RESOURCE_CHARM, 99);
    ASSERT_EQ(99U, player.resource(Otc::RESOURCE_CHARM));

    player.reset();

    EXPECT_EQ(0U, player.resource(Otc::RESOURCE_CHARM));
}

TEST(FakeProtocolCallbackReceiver, PreservesCallbackOrderAndCanReset)
{
    FakeProtocolCallbackReceiver receiver;
    receiver.onResourceBalance(30, 12);
    receiver.onResourceBalance(31, 34);

    EXPECT_EQ((std::vector<FakeProtocolCallbackReceiver::ResourceBalance>{ { 30, 12 }, { 31, 34 } }),
              receiver.resourceBalances());
    receiver.reset();
    EXPECT_TRUE(receiver.resourceBalances().empty());
}

} // namespace otclient::test
