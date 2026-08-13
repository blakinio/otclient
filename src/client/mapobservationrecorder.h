#pragma once

#include "declarations.h"

#include <deque>
#include <fstream>
#include <nlohmann/json.hpp>

class MapObservationRecorder final
{
public:
    void setEnabled(bool enabled);
    bool isEnabled() const { return m_enabled; }
    bool hasWriteFailure() const { return m_writeFailed; }
    void setOutputPath(std::string path);
    const std::string& getOutputPath() const { return m_outputPath; }

    void recordTileSnapshot(const Position& position, const TilePtr& tile);
    void recordTileDelta(const Position& position, std::string_view operation, int stackPosition, const ThingPtr& thing = nullptr);
    void recordTransition(const Position& beforePosition, const Position& afterPosition);

private:
    void loadConfiguration();
    bool ensureOutput();
    void enqueueRecord(const nlohmann::ordered_json& record);
    void drainPendingRecords();
    nlohmann::ordered_json producer() const;
    nlohmann::ordered_json serializeThing(const ThingPtr& thing, int stackPosition) const;

    bool m_enabled{ false };
    bool m_writeFailed{ false };
    bool m_drainScheduled{ false };
    bool m_configurationLoaded{ false };
    bool m_queueOverflowLogged{ false };
    uint64_t m_sequence{ 0 };
    uint64_t m_sessionGeneration{ 0 };
    std::string m_outputPath;
    std::string m_sessionId;
    std::deque<std::string> m_pendingRecords;
    std::ofstream m_output;
};

extern MapObservationRecorder g_mapObservationRecorder;
