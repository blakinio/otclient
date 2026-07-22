#include <framework/global.h>

#include <gtest/gtest.h>

#include "support/builders/input_message_builder.h"
#include "support/mocks/fake_protocol_callback_receiver.h"

#include <client/protocolcodes.h>
#include <framework/net/server.h>

#include <asio.hpp>

#include <array>
#include <chrono>
#include <string>

namespace otclient::test {

TEST(ProtocolLoopback, ReceivesOneWorldLightPacketFromLocalEphemeralPortAndCloses)
{
    // Protocol fixture: stable OTC opcode GameServerAmbient (0x82).
    // Fields: U8 opcode, U8 intensity, U8 color. Expected callback: (0x80, 0xD7).
    constexpr uint8_t bodySize = 3;
    const auto body = InputMessageBuilder()
        .addU8(Proto::GameServerAmbient)
        .addU8(0x80)
        .addU8(0xD7)
        .bytes();
    const std::array<uint8_t, bodySize + 2> wire{
        bodySize, 0x00, body[0], body[1], body[2]
    };

    asio::io_context io;
    asio::ip::tcp::acceptor server(io, { asio::ip::address_v4::loopback(), 0 });
    asio::ip::tcp::socket serverSocket(io);
    asio::ip::tcp::socket clientSocket(io);
    asio::steady_timer timeout(io, std::chrono::seconds(3));
    std::array<uint8_t, 2> receivedHeader{};
    std::array<uint8_t, bodySize> receivedBody{};
    FakeProtocolCallbackReceiver receiver;
    bool completed = false;
    bool timedOut = false;

    server.async_accept(serverSocket, [&](const std::error_code& error) {
        ASSERT_FALSE(error) << error.message();
        asio::async_write(serverSocket, asio::buffer(wire), [&](const std::error_code& writeError, std::size_t) {
            ASSERT_FALSE(writeError) << writeError.message();
            serverSocket.shutdown(asio::ip::tcp::socket::shutdown_both);
            serverSocket.close();
        });
    });

    clientSocket.async_connect(server.local_endpoint(), [&](const std::error_code& error) {
        ASSERT_FALSE(error) << error.message();
        asio::async_read(clientSocket, asio::buffer(receivedHeader), [&](const std::error_code& headerError, std::size_t) {
            ASSERT_FALSE(headerError) << headerError.message();
            ASSERT_EQ(bodySize, receivedHeader[0]);
            ASSERT_EQ(0, receivedHeader[1]);
            asio::async_read(clientSocket, asio::buffer(receivedBody), [&](const std::error_code& bodyError, std::size_t) {
                ASSERT_FALSE(bodyError) << bodyError.message();

                auto message = std::make_shared<InputMessage>();
                message->setBuffer(std::string(receivedBody.begin(), receivedBody.end()));
                message->setReadPos(static_cast<uint16_t>(message->getMaxHeaderSize()));
                ASSERT_EQ(Proto::GameServerAmbient, message->getU8());
                const auto intensity = message->getU8();
                const auto color = message->getU8();
                receiver.onWorldLight(intensity, color);
                EXPECT_TRUE(message->eof());
                EXPECT_EQ(0, message->getUnreadSize());

                completed = true;
                timeout.cancel();
                clientSocket.close();
            });
        });
    });

    timeout.async_wait([&](const std::error_code& error) {
        if (error == asio::error::operation_aborted)
            return;
        timedOut = true;
        clientSocket.close();
        serverSocket.close();
        server.close();
    });

    io.run();

    EXPECT_FALSE(timedOut);
    ASSERT_TRUE(completed);
    EXPECT_EQ((std::vector<FakeProtocolCallbackReceiver::WorldLight>{ { 0x80, 0xD7 } }), receiver.worldLights());
}

TEST(ServerLoopback, CreatesDistinctOsAssignedEphemeralPortsAndCloses)
{
    const auto first = Server::createLoopbackHttp();
    const auto second = Server::createLoopbackHttp();

    ASSERT_NE(nullptr, first);
    ASSERT_NE(nullptr, second);
    ASSERT_TRUE(first->isOpen());
    ASSERT_TRUE(second->isOpen());

    const int firstPort = first->getLocalPort();
    const int secondPort = second->getLocalPort();
    EXPECT_GE(firstPort, 1);
    EXPECT_LE(firstPort, 65535);
    EXPECT_GE(secondPort, 1);
    EXPECT_LE(secondPort, 65535);
    EXPECT_NE(firstPort, secondPort);

    first->close();
    second->close();
    EXPECT_FALSE(first->isOpen());
    EXPECT_FALSE(second->isOpen());
}

} // namespace otclient::test
