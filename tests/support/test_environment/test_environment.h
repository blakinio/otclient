#pragma once

#include <framework/core/logger.h>

#include <filesystem>
#include <string>

namespace otclient::test {

class TestEnvironment
{
public:
    explicit TestEnvironment(const std::filesystem::path& resourceRoot);
    ~TestEnvironment();

    TestEnvironment(const TestEnvironment&) = delete;
    TestEnvironment& operator=(const TestEnvironment&) = delete;

    void reset();
    [[nodiscard]] unsigned generation() const { return m_generation; }

private:
    std::string m_resourceRoot;
    Fw::LogLevel m_previousLogLevel;
    unsigned m_generation{ 0 };
};

} // namespace otclient::test
