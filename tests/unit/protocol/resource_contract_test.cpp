#include <gtest/gtest.h>

#include <client/const.h>
#include <client/protocolcodes.h>

#include <array>
#include <filesystem>
#include <fstream>
#include <map>
#include <regex>
#include <set>
#include <stdexcept>
#include <string>

namespace {

using Constants = std::map<std::string, uint32_t>;

std::string readConstantsFile()
{
    const auto path = std::filesystem::path(OTCLIENT_SOURCE_DIR) / "modules/gamelib/const.lua";
    std::ifstream stream(path);
    if (!stream)
        throw std::runtime_error("unable to open " + path.string());
    return { std::istreambuf_iterator<char>(stream), std::istreambuf_iterator<char>() };
}

Constants parseResourceTypes(const std::string& source)
{
    const auto tableStart = source.find("ResourceTypes = {");
    if (tableStart == std::string::npos)
        throw std::runtime_error("ResourceTypes table is missing");
    const auto tableEnd = source.find("\n}", tableStart);
    if (tableEnd == std::string::npos)
        throw std::runtime_error("ResourceTypes table is unterminated");

    const std::regex assignment(R"(([A-Z][A-Z0-9_]*)\s*=\s*([0-9]+))");
    Constants constants;
    const std::string table = source.substr(tableStart, tableEnd - tableStart);
    for (std::sregex_iterator it(table.begin(), table.end(), assignment), end; it != end; ++it)
        constants.emplace((*it)[1].str(), static_cast<uint32_t>(std::stoul((*it)[2].str())));
    return constants;
}

Constants parseGameFeatures(const std::string& source)
{
    const std::regex assignment(R"((?:^|\n)(Game[A-Za-z0-9_]+)\s*=\s*([0-9]+)\s*(?:\r?\n|$))");
    Constants constants;
    for (std::sregex_iterator it(source.begin(), source.end(), assignment), end; it != end; ++it)
        constants.emplace((*it)[1].str(), static_cast<uint32_t>(std::stoul((*it)[2].str())));
    return constants;
}

} // namespace

TEST(ResourceTypesContract, LuaIdentifiersAreUnique)
{
    const auto constants = parseResourceTypes(readConstantsFile());
    std::set<uint32_t> values;
    for (const auto& [name, value] : constants)
        EXPECT_TRUE(values.insert(value).second) << name << " duplicates resource id " << value;
}

TEST(ResourceTypesContract, SelectedLuaValuesMatchCppPublicEnum)
{
    const auto constants = parseResourceTypes(readConstantsFile());

    EXPECT_EQ(Otc::RESOURCE_BANK_BALANCE, constants.at("BANK_BALANCE"));
    EXPECT_EQ(Otc::RESOURCE_CHARM, constants.at("CHARM"));
    EXPECT_EQ(Otc::RESOURCE_FORGE_DUST, constants.at("FORGE_DUST"));
    EXPECT_EQ(Otc::RESOURCE_LESSER_FRAGMENT, constants.at("LESSER_FRAGMENT"));
    EXPECT_EQ(Otc::RESOURCE_GREATER_FRAGMENT, constants.at("GREATER_FRAGMENT"));
}

TEST(ResourceTypesContract, OnlyBankBalanceOwnsResourceIdentifierZero)
{
    const auto constants = parseResourceTypes(readConstantsFile());
    for (const auto& [name, value] : constants) {
        if (value == Otc::RESOURCE_BANK_BALANCE)
            EXPECT_EQ("BANK_BALANCE", name);
    }
}

TEST(ResourceTypesContract, FragmentContractUsesSingularNamesAndIds84And85)
{
    const auto constants = parseResourceTypes(readConstantsFile());

    EXPECT_EQ(84U, constants.at("LESSER_FRAGMENT"));
    EXPECT_EQ(85U, constants.at("GREATER_FRAGMENT"));
    EXPECT_FALSE(constants.contains("LESSER_FRAGMENTS"));
    EXPECT_FALSE(constants.contains("GREATER_FRAGMENTS"));
}

TEST(GameFeatureContract, SelectedLuaFeatureNamesMatchCpp)
{
    const auto constants = parseGameFeatures(readConstantsFile());

    EXPECT_EQ(Otc::GameProtocolChecksum, constants.at("GameProtocolChecksum"));
    EXPECT_EQ(Otc::GameSequencedPackets, constants.at("GameSequencedPackets"));
    EXPECT_EQ(Otc::GameVocationMonk, constants.at("GameVocationMonk"));
    EXPECT_EQ(Otc::GameTaskboard, constants.at("GameTaskboard"));
}

TEST(ProtocolCodeContract, SelectedStableServerOpcodesAreDistinctAndInGameRange)
{
    constexpr std::array<uint8_t, 5> opcodes{
        Proto::GameServerAmbient,
        Proto::GameServerCreatureMarks,
        Proto::GameServerPlayerData,
        Proto::GameServerPlayerSkills,
        Proto::GameServerResourceBalance,
    };
    const std::set<uint8_t> unique(opcodes.begin(), opcodes.end());

    EXPECT_EQ(opcodes.size(), unique.size());
    for (const auto opcode : opcodes)
        EXPECT_GE(opcode, Proto::GameServerFirstGameOpcode);
}
