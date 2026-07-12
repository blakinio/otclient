#include <gtest/gtest.h>

#include "support/builders/output_message_inspector.h"

#include <client/position.h>
#include <framework/net/outputmessage.h>

namespace otclient::test {

TEST(OutputMessage, WritesUnsignedIntegersInLittleEndianOrder)
{
    OutputMessage message;
    message.addU8(0x12);
    message.addU16(0x3456);
    message.addU32(0x789ABCDE);
    message.addU64(0x0123456789ABCDEFULL);

    EXPECT_TRUE(OutputMessageInspector(message).equals({
        0x12,
        0x56, 0x34,
        0xDE, 0xBC, 0x9A, 0x78,
        0xEF, 0xCD, 0xAB, 0x89, 0x67, 0x45, 0x23, 0x01
    }));
    EXPECT_EQ(15, message.getMessageSize());
}

TEST(OutputMessage, WritesStringsWithU16LengthPrefix)
{
    OutputMessage message;
    message.addString("OTC");

    EXPECT_TRUE(OutputMessageInspector(message).equals({ 0x03, 0x00, 'O', 'T', 'C' }));
    EXPECT_EQ(5, message.getMessageSize());
}

TEST(OutputMessage, EncodesPositionAsTwoU16CoordinatesAndOneU8Floor)
{
    OutputMessage message;
    const Position position(0x1234, 0x5678, 0x09);

    message.addU16(static_cast<uint16_t>(position.x));
    message.addU16(static_cast<uint16_t>(position.y));
    message.addU8(position.z);

    EXPECT_TRUE(OutputMessageInspector(message).equals({ 0x34, 0x12, 0x78, 0x56, 0x09 }));
}

TEST(OutputMessage, AppendingFieldsDoesNotOverwriteEarlierBytes)
{
    OutputMessage message;
    message.addBytes(std::string_view("\xAA\xBB", 2));
    message.addU16(0x1234);
    message.addU8(0xCC);

    EXPECT_TRUE(OutputMessageInspector(message).equals({ 0xAA, 0xBB, 0x34, 0x12, 0xCC }));
    EXPECT_EQ(5, message.getMessageSize());
}

TEST(OutputMessage, SetBufferResetsPreviousBodyBeforeAppending)
{
    OutputMessage message;
    message.addU32(0xFFFFFFFF);
    message.setBuffer(std::string("\x01\x02", 2));
    message.addU8(0x03);

    EXPECT_TRUE(OutputMessageInspector(message).equals({ 0x01, 0x02, 0x03 }));
    EXPECT_EQ(3, message.getMessageSize());
}

} // namespace otclient::test
