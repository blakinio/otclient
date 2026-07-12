#include <framework/pch.h>

#include "test_environment.h"

#include <framework/core/resourcemanager.h>

#include <stdexcept>

namespace otclient::test {

TestEnvironment::TestEnvironment(const std::filesystem::path& resourceRoot)
    : m_resourceRoot(std::filesystem::absolute(resourceRoot).generic_string()),
      m_previousLogLevel(g_logger.getLevel())
{
    g_logger.setLevel(Fw::LogFatal);
    g_resources.init(m_resourceRoot.c_str());
    if (!g_resources.addSearchPath(m_resourceRoot)) {
        g_resources.terminate();
        g_logger.setLevel(m_previousLogLevel);
        throw std::runtime_error("unable to mount test resource root");
    }
}

TestEnvironment::~TestEnvironment()
{
    reset();
    g_resources.removeSearchPath(m_resourceRoot);
    g_resources.terminate();
    g_logger.setLevel(m_previousLogLevel);
}

void TestEnvironment::reset()
{
    ++m_generation;
}

} // namespace otclient::test
