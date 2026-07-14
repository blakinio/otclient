#pragma once

#include <client/declarations.h>
#include <client/position.h>

#include <cstdint>
#include <memory>

namespace otclient::test {

class ThingTypeBuilder
{
public:
    ThingTypeBuilder& withFlag(ThingFlagAttr flag);
    [[nodiscard]] std::shared_ptr<ThingType> build() const;

private:
    uint64_t m_flags{ 0 };
};

class ItemBuilder
{
public:
    ItemBuilder& withId(uint16_t id);
    ItemBuilder& withFlag(ThingFlagAttr flag);
    [[nodiscard]] ThingPtr build() const;

private:
    uint16_t m_id{ 1 };
    uint64_t m_flags{ 0 };
};

class CreatureBuilder
{
public:
    CreatureBuilder& withId(uint32_t id);
    [[nodiscard]] CreaturePtr build() const;

private:
    uint32_t m_id{ 1 };
};

class TileBuilder
{
public:
    explicit TileBuilder(Position position);
    TileBuilder& add(const ThingPtr& thing, int stackPosition = -1);
    [[nodiscard]] TilePtr build() const { return m_tile; }

private:
    TilePtr m_tile;
};

} // namespace otclient::test
