#include "mapobservationrecorder.h"

#include "game.h"
#include "item.h"
#include "tile.h"

#include <framework/core/eventdispatcher.h>
#include <framework/core/logger.h>

MapObservationRecorder g_mapObservationRecorder;

void MapObservationRecorder::setEnabled(const bool enabled)
{
    m_enabled = enabled;
    m_writeFailed = false;
    m_sequence = 0;
    m_pendingRecords.clear();
    m_drainScheduled = false;
    m_sessionId = enabled ? "map-observation-" + std::to_string(++m_sessionGeneration) : "";
    if (!enabled && m_output.is_open())
        m_output.close();
}

void MapObservationRecorder::setOutputPath(std::string path)
{
    if (m_output.is_open())
        m_output.close();
    m_outputPath = std::move(path);
    m_pendingRecords.clear();
    m_writeFailed = false;
}

bool MapObservationRecorder::ensureOutput()
{
    if (!m_enabled || m_writeFailed)
        return false;
    if (m_output.is_open())
        return true;
    if (m_outputPath.empty()) {
        g_logger.warning("Map observation recorder is enabled without an output path");
        m_writeFailed = true;
        return false;
    }
    m_output.open(m_outputPath, std::ios::out | std::ios::app | std::ios::binary);
    if (!m_output.is_open()) {
        g_logger.error("Map observation recorder could not open its output file");
        m_writeFailed = true;
        return false;
    }
    return true;
}

nlohmann::ordered_json MapObservationRecorder::producer() const
{
    return {
        { "revision", BUILD_REVISION },
        { "client_version", std::to_string(g_game.getClientVersion()) },
        { "protocol_version", g_game.getProtocolVersion() }
    };
}

nlohmann::ordered_json MapObservationRecorder::serializeThing(const ThingPtr& thing, const int stackPosition) const
{
    nlohmann::ordered_json identity;
    if (thing->isCreature())
        identity["client_creature_id"] = thing->getId();
    else
        identity["client_appearance_id"] = thing->getClientId();

    nlohmann::ordered_json result{
        { "stack_position", stackPosition },
        { "category", thing->isItem() ? "item" : thing->isCreature() ? "creature" : thing->isEffect() ? "effect" : thing->isMissile() ? "missile" : "unknown" },
        { "identity", std::move(identity) },
        { "state", nlohmann::ordered_json::object() }
    };
    if (thing->isItem())
        result["subtype"] = thing->static_self_cast<Item>()->getSubType();
    return result;
}

void MapObservationRecorder::enqueueRecord(const nlohmann::ordered_json& record)
{
    if (!m_enabled || m_writeFailed)
        return;
    constexpr size_t maxPendingRecords = 256;
    if (m_pendingRecords.size() >= maxPendingRecords) {
        g_logger.warning("Map observation recorder dropped an observation because its bounded queue is full");
        return;
    }
    m_pendingRecords.push_back(record.dump());
    if (!m_drainScheduled) {
        m_drainScheduled = true;
        g_dispatcher.deferEvent([this] { drainPendingRecords(); });
    }
}

void MapObservationRecorder::drainPendingRecords()
{
    m_drainScheduled = false;
    if (!m_enabled || !ensureOutput())
        return;
    constexpr size_t maxRecordsPerDrain = 32;
    for (size_t index = 0; index < maxRecordsPerDrain && !m_pendingRecords.empty(); ++index) {
        m_output << m_pendingRecords.front() << '\n';
        m_pendingRecords.pop_front();
    }
    if (!m_output.good()) {
        g_logger.error("Map observation recorder failed while writing an observation");
        m_output.close();
        m_writeFailed = true;
        m_pendingRecords.clear();
        return;
    }
    if (!m_pendingRecords.empty()) {
        m_drainScheduled = true;
        g_dispatcher.deferEvent([this] { drainPendingRecords(); });
    }
}

void MapObservationRecorder::recordTileSnapshot(const Position& position, const TilePtr& tile)
{
    if (!m_enabled)
        return;
    nlohmann::ordered_json record{
        { "schema_version", 1 },
        { "record_type", "tile_snapshot" },
        { "sequence", ++m_sequence },
        { "session_id", m_sessionId },
        { "producer", producer() },
        { "position", { { "x", position.x }, { "y", position.y }, { "z", position.z } } }
    };
    nlohmann::ordered_json things = nlohmann::ordered_json::array();
    if (tile) {
        const auto& values = tile->getThings();
        for (size_t index = 0; index < values.size(); ++index)
            things.push_back(serializeThing(values[index], static_cast<int>(index)));
    }
    record["completeness"] = things.empty() ? "EMPTY" : "FULL";
    record["things"] = std::move(things);
    enqueueRecord(record);
}

void MapObservationRecorder::recordTileDelta(const Position& position, std::string_view operation, const int stackPosition, const ThingPtr& thing)
{
    if (!m_enabled)
        return;
    nlohmann::ordered_json change{ { "operation", operation }, { "stack_position", stackPosition } };
    if (thing)
        change["thing"] = serializeThing(thing, stackPosition);
    enqueueRecord({
        { "schema_version", 1 },
        { "record_type", "tile_delta" },
        { "sequence", ++m_sequence },
        { "session_id", m_sessionId },
        { "producer", producer() },
        { "position", { { "x", position.x }, { "y", position.y }, { "z", position.z } } },
        { "completeness", "PARTIAL" },
        { "changes", nlohmann::ordered_json::array({ std::move(change) }) }
    });
}
