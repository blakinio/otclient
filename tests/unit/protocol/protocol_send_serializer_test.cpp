#include <framework/global.h>

#include <gtest/gtest.h>

#include <framework/net/protocol.h>

#include <condition_variable>
#include <mutex>
#include <thread>
#include <vector>

namespace otclient::test {

TEST(ProtocolSendSerializer, SerializesConcurrentCallbacks)
{
    detail::ProtocolSendSerializer serializer;
    std::mutex stateMutex;
    std::condition_variable stateChanged;
    bool firstEntered = false;
    bool releaseFirst = false;
    bool secondAttempted = false;
    bool secondEntered = false;
    std::vector<int> order;

    std::thread first([&] {
        serializer.serialize([&] {
            std::unique_lock stateLock(stateMutex);
            order.push_back(1);
            firstEntered = true;
            stateChanged.notify_all();
            stateChanged.wait(stateLock, [&] { return releaseFirst; });
        });
    });

    {
        std::unique_lock stateLock(stateMutex);
        stateChanged.wait(stateLock, [&] { return firstEntered; });
    }

    std::thread second([&] {
        {
            const std::scoped_lock stateLock(stateMutex);
            secondAttempted = true;
            stateChanged.notify_all();
        }

        serializer.serialize([&] {
            const std::scoped_lock stateLock(stateMutex);
            secondEntered = true;
            order.push_back(2);
            stateChanged.notify_all();
        });
    });

    {
        std::unique_lock stateLock(stateMutex);
        stateChanged.wait(stateLock, [&] { return secondAttempted; });
        EXPECT_FALSE(secondEntered);
        releaseFirst = true;
        stateChanged.notify_all();
    }

    first.join();
    second.join();

    EXPECT_TRUE(secondEntered);
    EXPECT_EQ((std::vector<int>{ 1, 2 }), order);
}

TEST(ProtocolSendSerializer, KeepsSequenceAllocationAndEnqueueInOneOrder)
{
    detail::ProtocolSendSerializer serializer;
    constexpr int messageCount = 32;
    int nextSequence = 0;
    std::vector<int> wireOrder;
    std::vector<std::thread> senders;
    senders.reserve(messageCount);

    for (int index = 0; index < messageCount; ++index) {
        senders.emplace_back([&] {
            serializer.serialize([&] {
                const int sequence = nextSequence++;
                wireOrder.push_back(sequence);
            });
        });
    }

    for (auto& sender : senders) {
        sender.join();
    }

    ASSERT_EQ(messageCount, static_cast<int>(wireOrder.size()));
    for (int index = 0; index < messageCount; ++index) {
        EXPECT_EQ(index, wireOrder[index]);
    }
}

TEST(ProtocolSendSerializer, AllowsSameThreadReentry)
{
    detail::ProtocolSendSerializer serializer;
    int callbackCount = 0;

    serializer.serialize([&] {
        ++callbackCount;
        serializer.serialize([&] { ++callbackCount; });
    });

    EXPECT_EQ(2, callbackCount);
}

} // namespace otclient::test
