#include <gtest/gtest.h>

#include "support/assertions/message_assertions.h"
#include "support/builders/input_message_builder.h"

#include <framework/stdext/exception.h>

namespace otclient::test {

TEST(InputMessage, ReadsUnsignedIntegersInLittleEndianOrder)
{
    auto message = InputMessageBuilder()
        .addU8(0x12)
        .addU16(0x3456)
        .addU32(0x789ABCDE)
        .addU64(0x0123456789ABCDEFULL)
        .build();

    const int bodyStart = message->getReadPos();
    EXPECT_EQ(0x12, message->getU8());
    EXPECT_TRUE(cursorIs(*message, bodyStart + 1));
    EXPECT_EQ(0x3456, message->getU16());
    EXPECT_EQ(0x789ABCDEU, message->getU32());
    EXPECT_EQ(0x0123456789ABCDEFULL, message->getU64());
    EXPECT_TRUE(consumed(*message));
}

TEST(InputMessage, ReadsLengthPrefixedStringAndPositionFields)
{
    auto message = InputMessageBuilder()
        .addString("Redemption")
        .addPosition(Position(0x1234, 0x5678, 7))
        .build();

    EXPECT_EQ("Redemption", message->getString());
    const Position position(message->getU16(), message->getU16(), message->getU8());
    EXPECT_EQ(0x1234, position.x);
    EXPECT_EQ(0x5678, position.y);
    EXPECT_EQ(7, position.z);
    EXPECT_TRUE(consumed(*message));
}

TEST(InputMessage, TracksUnreadBytesAndEofFromBodyConsumption)
{
    auto message = InputMessageBuilder().addBytes({ 1, 2, 3 }).build();

    EXPECT_TRUE(unreadIs(*message, 3));
    EXPECT_FALSE(message->eof());
    EXPECT_EQ(1, message->getU8());
    EXPECT_TRUE(unreadIs(*message, 2));
    message->skipBytes(2);
    EXPECT_TRUE(consumed(*message));
}

TEST(InputMessage, SkipBytesMovesTheCursorWithoutChangingBodySize)
{
    auto message = InputMessageBuilder().addBytes({ 0xAA, 0xBB, 0xCC }).build();
    const int bodyStart = message->getReadPos();
    const auto bodySize = message->getMessageSize();

    message->skipBytes(1);

    EXPECT_TRUE(cursorIs(*message, bodyStart + 1));
    EXPECT_EQ(bodySize, message->getMessageSize());
    EXPECT_EQ(0xBB, message->getU8());
    EXPECT_EQ(0xCC, message->getU8());
    EXPECT_TRUE(consumed(*message));
}

TEST(InputMessage, ReadPastEndThrowsWithoutAdvancingTheCursor)
{
    auto message = InputMessageBuilder().addU8(0x7F).build();
    EXPECT_EQ(0x7F, message->getU8());
    const int end = message->getReadPos();

    EXPECT_THROW(message->getU8(), stdext::exception);
    EXPECT_TRUE(cursorIs(*message, end));
    EXPECT_TRUE(consumed(*message));
}

TEST(InputMessage, EmptyBodyStartsAtEof)
{
    auto message = InputMessageBuilder().build();

    EXPECT_EQ(0, message->getMessageSize());
    EXPECT_TRUE(consumed(*message));
    EXPECT_THROW(message->getU16(), stdext::exception);
}

TEST(InputMessage, BodySizeIsIndependentFromReservedHeaderCursorOffset)
{
    auto message = InputMessageBuilder().addBytes({ 0x10, 0x20 }).build();

    EXPECT_EQ(2, message->getMessageSize());
    EXPECT_EQ(message->getMaxHeaderSize(), message->getReadPos());
    EXPECT_GT(message->getReadPos(), message->getMessageSize());
    EXPECT_EQ(0x10, message->getU8());
    EXPECT_FALSE(message->eof());
    EXPECT_EQ(0x20, message->getU8());
    EXPECT_TRUE(consumed(*message));
}

TEST(InputMessageBuilder, PreservesDeclaredWireByteOrder)
{
    const InputMessageBuilder builder = InputMessageBuilder()
        .addU16(0x1234)
        .addU32(0x89ABCDEF);

    EXPECT_EQ((std::vector<uint8_t>{ 0x34, 0x12, 0xEF, 0xCD, 0xAB, 0x89 }), builder.bytes());
}

} // namespace otclient::test
