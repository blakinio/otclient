#include <gtest/gtest.h>

#include <framework/platform/platform.h>

#include <chrono>
#include <cstdlib>
#include <filesystem>
#include <fstream>
#include <iterator>
#include <optional>
#include <string>
#include <thread>
#include <utility>

#if !defined(WIN32) && !defined(__APPLE__) && !defined(__EMSCRIPTEN__) && !defined(ANDROID)
#include <sys/stat.h>
#include <unistd.h>
#endif

namespace {
#if !defined(WIN32) && !defined(__APPLE__) && !defined(__EMSCRIPTEN__) && !defined(ANDROID)
class EnvironmentVariableGuard
{
public:
    explicit EnvironmentVariableGuard(const char* name) :
        m_name(name)
    {
        if (const char* value = std::getenv(name))
            m_originalValue = value;
    }

    ~EnvironmentVariableGuard()
    {
        if (m_originalValue)
            setenv(m_name.c_str(), m_originalValue->c_str(), 1);
        else
            unsetenv(m_name.c_str());
    }

private:
    std::string m_name;
    std::optional<std::string> m_originalValue;
};

class TemporaryDirectoryGuard
{
public:
    explicit TemporaryDirectoryGuard(std::filesystem::path path) :
        m_path(std::move(path))
    {
        std::filesystem::create_directories(m_path);
    }

    ~TemporaryDirectoryGuard()
    {
        std::error_code ignored;
        std::filesystem::remove_all(m_path, ignored);
    }

    [[nodiscard]] const std::filesystem::path& path() const
    {
        return m_path;
    }

private:
    std::filesystem::path m_path;
};

std::string readFile(const std::filesystem::path& path)
{
    std::ifstream input(path, std::ios::binary);
    return { std::istreambuf_iterator<char>(input), std::istreambuf_iterator<char>() };
}
#endif
}

TEST(PlatformOpenUrlTest, PreservesCompleteUrlAsOneProcessArgument)
{
#if defined(WIN32) || defined(__APPLE__) || defined(__EMSCRIPTEN__) || defined(ANDROID)
    GTEST_SKIP() << "This regression exercises the Linux xdg-open process boundary.";
#else
    const auto uniqueSuffix = std::to_string(getpid()) + "-" +
        std::to_string(std::chrono::steady_clock::now().time_since_epoch().count());
    TemporaryDirectoryGuard temporaryDirectory(
        std::filesystem::temp_directory_path() / ("otclient-open-url-" + uniqueSuffix));

    const auto launcherPath = temporaryDirectory.path() / "xdg-open";
    const auto capturePath = temporaryDirectory.path() / "captured-arguments.txt";
    {
        std::ofstream launcher(launcherPath);
        ASSERT_TRUE(launcher.is_open());
        launcher << "#!/bin/sh\n"
                 << "{\n"
                 << "  printf '%s\\n' \"$#\"\n"
                 << "  printf '%s' \"$1\"\n"
                 << "} > \"$OTCLIENT_OPEN_URL_CAPTURE\"\n";
    }
    ASSERT_EQ(chmod(launcherPath.c_str(), 0755), 0);

    EnvironmentVariableGuard pathGuard("PATH");
    EnvironmentVariableGuard captureGuard("OTCLIENT_OPEN_URL_CAPTURE");
    const std::string originalPath = std::getenv("PATH") ? std::getenv("PATH") : "";
    const std::string testPath = temporaryDirectory.path().string() + ":" + originalPath;
    ASSERT_EQ(setenv("PATH", testPath.c_str(), 1), 0);
    ASSERT_EQ(setenv("OTCLIENT_OPEN_URL_CAPTURE", capturePath.c_str(), 1), 0);

    const std::string url =
        "https://platform.oteryn.test/oauth/authorize?client_id=native-client&response_type=code&"
        "scope=game%3Aticket&state=0123456789abcdef&code_challenge=challenge&code_challenge_method=S256";
    ASSERT_TRUE(g_platform.openUrl(url, true));

    std::string captured;
    for (int attempt = 0; attempt < 200; ++attempt) {
        if (std::filesystem::exists(capturePath)) {
            captured = readFile(capturePath);
            if (captured.size() >= url.size() + 2)
                break;
        }
        std::this_thread::sleep_for(std::chrono::milliseconds(10));
    }

    const auto separator = captured.find('\n');
    ASSERT_NE(separator, std::string::npos) << "The fake xdg-open process did not retain argument metadata.";
    EXPECT_EQ(captured.substr(0, separator), "1");
    EXPECT_EQ(captured.substr(separator + 1), url);
#endif
}
