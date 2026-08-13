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

TEST(MapObservationRecorder, DisabledRecorderLeavesUnknownAsNoObservation)
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

TEST(MapObservationRecorder, WritesOrderedFullEmptyPartialAndTransitionRecords)
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
    g_mapObservationRecorder.recordTileDelta(fullTile->getPosition(), "add", 0, first);
    g_mapObservationRecorder.recordTileDelta(fullTile->getPosition(), "change", 1, second);
    g_mapObservationRecorder.recordTileDelta(fullTile->getPosition(), "delete", 1);
    g_mapObservationRecorder.recordTransition(Position(100, 100, 7), Position(101, 100, 7));
    g_dispatcher.poll();

    std::ifstream input(path, std::ios::binary);
    ASSERT_TRUE(input.is_open());
    std::vector<nlohmann::ordered_json> records;
    for (std::string line; std::getline(input, line);)
        records.push_back(nlohmann::ordered_json::parse(line));

    ASSERT_EQ(6U, records.size());
    EXPECT_EQ("FULL", records[0]["completeness"]);
    ASSERT_EQ(fullTile->getThings().size(), records[0]["things"].size());
    for (size_t index = 0; index < fullTile->getThings().size(); ++index) {
        const auto& thing = fullTile->getThings()[index];
        const auto& observation = records[0]["things"][index];
        EXPECT_EQ(static_cast<int>(index), observation["stack_position"]);
        if (thing->isCreature())
            EXPECT_EQ(thing->getId(), observation["identity"]["client_creature_id"]);
        else
            EXPECT_EQ(thing->getClientId(), observation["identity"]["client_appearance_id"]);
    }
    EXPECT_EQ("EMPTY", records[1]["completeness"]);
    EXPECT_TRUE(records[1]["things"].empty());
    EXPECT_EQ("PARTIAL", records[2]["completeness"]);
    EXPECT_EQ("add", records[2]["changes"][0]["operation"]);
    EXPECT_EQ(3031, records[2]["changes"][0]["thing"]["identity"]["client_appearance_id"]);
    EXPECT_EQ("change", records[3]["changes"][0]["operation"]);
    EXPECT_EQ(424242, records[3]["changes"][0]["thing"]["identity"]["client_creature_id"]);
    EXPECT_EQ("delete", records[4]["changes"][0]["operation"]);
    EXPECT_FALSE(records[4]["changes"][0].contains("thing"));
    EXPECT_EQ("transition_event", records[5]["record_type"]);
    EXPECT_EQ("decoded_state", records[5]["evidence"]);
    EXPECT_EQ(100, records[5]["before_position"]["x"]);
    EXPECT_EQ(101, records[5]["after_position"]["x"]);
    EXPECT_FALSE(records[0]["session_id"].get<std::string>().empty());

    const auto serialized = records[0].dump();
    EXPECT_EQ(std::string::npos, serialized.find("password"));
    EXPECT_EQ(std::string::npos, serialized.find("token"));
    EXPECT_EQ(std::string::npos, serialized.find("cookie"));

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
