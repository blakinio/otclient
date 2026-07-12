#pragma once

#include <cstdint>
#include <string>
#include <utility>
#include <vector>

namespace otclient::test {

class FakeProtocolCallbackReceiver
{
public:
    struct WorldLight
    {
        uint8_t intensity;
        uint8_t color;

        bool operator==(const WorldLight&) const = default;
    };

    struct ResourceBalance
    {
        uint8_t type;
        uint64_t value;

        bool operator==(const ResourceBalance&) const = default;
    };

    void onResourceBalance(const uint8_t type, const uint64_t value)
    {
        m_resourceBalances.push_back({ type, value });
    }

    void onWorldLight(const uint8_t intensity, const uint8_t color)
    {
        m_worldLights.push_back({ intensity, color });
    }

    [[nodiscard]] const std::vector<ResourceBalance>& resourceBalances() const { return m_resourceBalances; }
    [[nodiscard]] const std::vector<WorldLight>& worldLights() const { return m_worldLights; }
    void reset()
    {
        m_resourceBalances.clear();
        m_worldLights.clear();
    }

private:
    std::vector<ResourceBalance> m_resourceBalances;
    std::vector<WorldLight> m_worldLights;
};

} // namespace otclient::test
