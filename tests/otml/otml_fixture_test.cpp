#include <gtest/gtest.h>

#include <framework/otml/otmldocument.h>

#include <filesystem>
#include <fstream>

namespace {

OTMLDocumentPtr parseFixture(const std::string& name)
{
    const auto path = std::filesystem::path(OTCLIENT_SOURCE_DIR) / "tests/fixtures/otml" / name;
    std::ifstream stream(path);
    if (!stream)
        throw std::runtime_error("unable to open OTML fixture " + path.string());
    return OTMLDocument::parse(stream, path.generic_string());
}

} // namespace

TEST(OTMLFixture, NestedStyleCommentsAliasesAndEmptyValuesParseDeterministically)
{
    const auto first = parseFixture("nested_styles.otml");
    const auto second = parseFixture("nested_styles.otml");

    const auto firstPanel = first->get("BasePanel < UIWidget");
    const auto secondPanel = second->get("BasePanel < UIWidget");
    ASSERT_NE(nullptr, firstPanel);
    ASSERT_NE(nullptr, secondPanel);
    EXPECT_EQ("120", firstPanel->valueAt("width"));
    EXPECT_EQ("", firstPanel->valueAt("empty-value"));
    EXPECT_EQ("#33AAFF", firstPanel->get("Header < UIWidget")->valueAt("color"));
    EXPECT_EQ(first->emit(), second->emit());
}

TEST(OTMLFixture, OddIndentationIsRejectedWithSourceContext)
{
    EXPECT_THROW(parseFixture("invalid_indentation.otml"), OTMLException);
}
