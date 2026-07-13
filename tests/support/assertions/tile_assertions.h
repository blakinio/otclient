#pragma once

#include <client/tile.h>

#include <gtest/gtest.h>

#include <vector>

namespace otclient::test {

inline testing::AssertionResult thingsAre(const Tile& tile, const std::vector<ThingPtr>& expected)
{
    const auto& actual = const_cast<Tile&>(tile).getThings();
    if (actual == expected)
        return testing::AssertionSuccess();
    return testing::AssertionFailure() << "expected " << expected.size()
                                       << " tile things, got " << actual.size();
}

} // namespace otclient::test
