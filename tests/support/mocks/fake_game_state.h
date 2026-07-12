#pragma once

#include <client/const.h>

#include <cstdint>
#include <unordered_map>

namespace otclient::test {

class FakeGameState
{
public:
    void setResource(const Otc::ResourceTypes_t type, const uint64_t value) { m_resources[type] = value; }
    [[nodiscard]] uint64_t resource(const Otc::ResourceTypes_t type) const
    {
        const auto it = m_resources.find(type);
        return it == m_resources.end() ? 0 : it->second;
    }
    void reset() { m_resources.clear(); }

private:
    std::unordered_map<Otc::ResourceTypes_t, uint64_t> m_resources;
};

using FakeLocalPlayer = FakeGameState;

} // namespace otclient::test
