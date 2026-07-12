#include <framework/global.h>

#define private public
#include <client/thingtype.h>
#undef private

#include "thing_builders.h"

#include <client/creature.h>
#include <client/thing.h>
#include <client/tile.h>

namespace otclient::test {

namespace {

std::shared_ptr<ThingType> makeThingType(const ThingCategory category, const uint64_t flags)
{
    auto type = std::make_shared<ThingType>();
    type->m_null = false;
    type->m_category = category;
    type->m_flags = flags;
    type->m_size = Size(1, 1);
    type->m_realSize = 32;
    type->m_layers = 1;
    type->m_animationPhases = 1;
    type->m_opacity = 1.f;
    return type;
}

class SyntheticItem final : public Thing
{
public:
    SyntheticItem(const uint16_t id, std::shared_ptr<ThingType> type) : m_type(std::move(type))
    {
        m_clientId = id;
    }

    bool isItem() const override { return true; }

protected:
    ThingType* getThingType() const override { return m_type.get(); }

private:
    std::shared_ptr<ThingType> m_type;
};

class SyntheticCreature final : public Creature
{
public:
    SyntheticCreature(const uint32_t id, std::shared_ptr<ThingType> type) : m_type(std::move(type))
    {
        setId(id);
        setRemovedSilently(false);
    }

    void onAppear() override { setRemovedSilently(false); }
    void onDisappear() override { setRemovedSilently(true); }
    void onPositionChange(const Position&, const Position& oldPosition) override
    {
        setOldPositionSilently(oldPosition);
    }
    void terminateWalk() override
    {
        m_walking = false;
        m_walkOffset = {};
    }

    ThingType* getThingType() const override { return m_type.get(); }

private:
    std::shared_ptr<ThingType> m_type;
};

} // namespace

ThingTypeBuilder& ThingTypeBuilder::withFlag(const ThingFlagAttr flag)
{
    m_flags |= flag;
    return *this;
}

std::shared_ptr<ThingType> ThingTypeBuilder::build() const
{
    return makeThingType(ThingCategoryItem, m_flags);
}

ItemBuilder& ItemBuilder::withId(const uint16_t id)
{
    m_id = id;
    return *this;
}

ItemBuilder& ItemBuilder::withFlag(const ThingFlagAttr flag)
{
    m_flags |= flag;
    return *this;
}

ThingPtr ItemBuilder::build() const
{
    return std::make_shared<SyntheticItem>(m_id, makeThingType(ThingCategoryItem, m_flags));
}

CreatureBuilder& CreatureBuilder::withId(const uint32_t id)
{
    m_id = id;
    return *this;
}

CreaturePtr CreatureBuilder::build() const
{
    return std::make_shared<SyntheticCreature>(m_id, makeThingType(ThingCategoryCreature, 0));
}

TileBuilder::TileBuilder(Position position) : m_tile(std::make_shared<Tile>(position)) {}

TileBuilder& TileBuilder::add(const ThingPtr& thing, const int stackPosition)
{
    m_tile->addThing(thing, stackPosition);
    return *this;
}

} // namespace otclient::test
