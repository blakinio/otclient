#include <framework/global.h>

#include <gtest/gtest.h>

#include "support/builders/thing_builders.h"

#include <client/mapobservationrecorder.h>
#include <client/tile.h>

#include <framework/core/eventdispatcher.h>

namespace otclient::test {

namespace {

std::filesystem::path outputPath(const std::string_view name)
{
    return std::filesystem::temp_directory_path() / ("otclient-map-observation-" + std::string(name) + ".jsonl");
}

void resetOutput(const std::filesystem::path& path)
{
    std::error_code error;
    std::filesystem::remove(path, error);
    ASSERT_FALSE(error) << error.message();
}

} // namespace

TEST(MapObservationRecorder, DisabledRecorderDoesNotCreateAnArtifact)
{
    const auto path = outputPath("disabled");
    resetOutput(path);
    const auto tile = TileBuilder(Position(100, 100, 7)).add(ItemBuilder().withId(3031).build()).build();

    g_mapObservationRecorder.setOutputPath(path.string());
    g_mapObservationRecorder.setEnabled(false);
    g_mapObservationRecorder.recordTileSnapshot(tile->getPosition(), tile);
    g_dispatcher.poll();

    EXPECT_FALSE(std::filesystem::exists(path));
}

TEST(MapObservationRecorder, WritesOrderedFullEmptyAndPartialRecords)
{
    const auto path = outputPath("records");
    resetOutput(path);
    const auto first = ItemBuilder().withId(3031).build();
    const auto second = CreatureBuilder().withId(424242).build();
    const auto fullTile = TileBuilder(Position(100, 100, 7)).add(first).add(second).build();
    const auto emptyTile = TileBuilder(Position(101, 100, 7)).build();

    g_mapObservationRecorder.setOutputPath(path.string());
    g_mapObservationRecorder.setEnabled(true);
    g_mapObservationRecorder.recordTileSnapshot(fullTile->getPosition(), fullTile);
    g_mapObservationRecorder.recordTileSnapshot(emptyTile->getPosition(), emptyTile);
    g_mapObservationRecorder.recordTileDelta(fullTile->getPosition(), "delete", 1);
    g_dispatcher.poll();

    std::ifstream input(path, std::ios::binary);
    ASSERT_TRUE(input.is_open());
    std::vector<nlohmann::ordered_json> records;
    for (std::string line; std::getline(input, line);)
        records.push_back(nlohmann::ordered_json::parse(line));

    ASSERT_EQ(3U, records.size());
    EXPECT_EQ("FULL", records[0]["completeness"]);
    EXPECT_EQ(0, records[0]["things"][0]["stack_position"]);
    EXPECT_EQ(1, records[0]["things"][1]["stack_position"]);
    EXPECT_EQ(3031, records[0]["things"][0]["identity"]["client_appearance_id"]);
    EXPECT_EQ(424242, records[0]["things"][1]["identity"]["client_creature_id"]);
    EXPECT_EQ("EMPTY", records[1]["completeness"]);
    EXPECT_TRUE(records[1]["things"].empty());
    EXPECT_EQ("PARTIAL", records[2]["completeness"]);
    EXPECT_EQ("delete", records[2]["changes"][0]["operation"]);
    EXPECT_FALSE(records[2]["changes"][0].contains("thing"));
    EXPECT_FALSE(records[0]["session_id"].get<std::string>().empty());

    g_mapObservationRecorder.setEnabled(false);
    resetOutput(path);
}

TEST(MapObservationRecorder, SinkFailureIsVisibleAndDoesNotThrow)
{
    const auto directory = std::filesystem::temp_directory_path();
    const auto tile = TileBuilder(Position(100, 100, 7)).build();

    g_mapObservationRecorder.setOutputPath(directory.string());
    g_mapObservationRecorder.setEnabled(true);
    EXPECT_NO_THROW(g_mapObservationRecorder.recordTileSnapshot(tile->getPosition(), tile));
    EXPECT_NO_THROW(g_dispatcher.poll());
    EXPECT_TRUE(g_mapObservationRecorder.hasWriteFailure());
    g_mapObservationRecorder.setEnabled(false);
}

} // namespace otclient::test
