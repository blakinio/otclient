#include <framework/global.h>

#include <gtest/gtest.h>

#include "support/assertions/tile_assertions.h"
#include "support/builders/thing_builders.h"

#include <client/const.h>
#include <client/creature.h>
#include <client/tile.h>
#include <client/thingtype.h>

namespace otclient::test {

TEST(ThingTypeBuilder, AppliesOnlyRequestedSyntheticFlags)
{
    const auto type = ThingTypeBuilder()
        .withFlag(ThingFlagAttrGroundBorder)
        .withFlag(ThingFlagAttrMultiUse)
        .build();

    EXPECT_TRUE(type->isGroundBorder());
    EXPECT_TRUE(type->isMultiUse());
    EXPECT_FALSE(type->isGround());
    EXPECT_FALSE(type->isOnTop());
}

TEST(TileOrdering, EmptyTileHasNoSelectableThing)
{
    const auto tile = TileBuilder(Position(100, 100, 7)).build();

    EXPECT_TRUE(tile->isEmpty());
    EXPECT_EQ(nullptr, tile->getTopThing());
    EXPECT_EQ(nullptr, tile->getTopUseThing());
    EXPECT_EQ(nullptr, tile->getTopMultiUseThing());
}

TEST(TileOrdering, AutomaticInsertionGroupsGroundBorderBottomTopAndCommonItems)
{
    const auto common = ItemBuilder().withId(5).build();
    const auto top = ItemBuilder().withId(4).withFlag(ThingFlagAttrOnTop).build();
    const auto ground = ItemBuilder().withId(1).withFlag(ThingFlagAttrGround).build();
    const auto bottom = ItemBuilder().withId(3).withFlag(ThingFlagAttrOnBottom).build();
    const auto border = ItemBuilder().withId(2).withFlag(ThingFlagAttrGroundBorder).build();

    const auto tile = TileBuilder(Position(100, 100, 7))
        .add(common)
        .add(top)
        .add(ground)
        .add(bottom)
        .add(border)
        .build();

    EXPECT_TRUE(thingsAre(*tile, { ground, border, bottom, top, common }));
    EXPECT_TRUE(tile->hasTopItem());
    EXPECT_TRUE(tile->hasBottomItem());
    EXPECT_TRUE(tile->hasCommonItem());
}

TEST(TileSelection, MostRecentlyAddedCommonItemIsTopThingAndTopUseThing)
{
    const auto first = ItemBuilder().withId(1).build();
    const auto second = ItemBuilder().withId(2).build();
    const auto tile = TileBuilder(Position(100, 100, 7)).add(first).add(second).build();

    EXPECT_TRUE(thingsAre(*tile, { second, first }));
    EXPECT_EQ(second, tile->getTopThing());
    EXPECT_EQ(second, tile->getTopUseThing());
}

TEST(TileSelection, ForceUseItemWinsOverOtherUseCandidates)
{
    const auto ordinary = ItemBuilder().withId(1).build();
    const auto forceUse = ItemBuilder().withId(2).withFlag(ThingFlagAttrForceUse).build();
    const auto tile = TileBuilder(Position(100, 100, 7)).add(ordinary).add(forceUse).build();

    EXPECT_EQ(forceUse, tile->getTopUseThing());
}

TEST(TileSelection, CreatureWinsTopMultiUseSelection)
{
    const auto multiUse = ItemBuilder().withId(1).withFlag(ThingFlagAttrMultiUse).build();
    const auto creature = CreatureBuilder().withId(77).build();
    const auto tile = TileBuilder(Position(100, 100, 7)).add(multiUse).add(creature).build();

    EXPECT_EQ(creature, tile->getTopMultiUseThing());
}

TEST(TileMutation, RemovingAndReaddingItemUpdatesOrderWithoutDuplicates)
{
    const auto first = ItemBuilder().withId(1).build();
    const auto second = ItemBuilder().withId(2).build();
    const auto tile = TileBuilder(Position(100, 100, 7)).add(first).add(second).build();

    ASSERT_TRUE(tile->removeThing(second));
    EXPECT_TRUE(thingsAre(*tile, { first }));
    tile->addThing(second, -1);

    EXPECT_TRUE(thingsAre(*tile, { second, first }));
    EXPECT_EQ(2, tile->getThingCount());
}

TEST(TileSelection, GroundIsFallbackWhenNoInteractiveThingExists)
{
    const auto ground = ItemBuilder().withId(1).withFlag(ThingFlagAttrGround).build();
    const auto tile = TileBuilder(Position(100, 100, 7)).add(ground).build();

    EXPECT_EQ(ground, tile->getTopThing());
    EXPECT_EQ(ground, tile->getTopUseThing());
    EXPECT_EQ(ground, tile->getTopMultiUseThing());
}

} // namespace otclient::test
