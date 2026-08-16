#include <QtCore/QCoreApplication>
#include <QtCore/QMetaObject>
#include <QtCore/QObject>

#include <algorithm>
#include <atomic>
#include <cerrno>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <dlfcn.h>
#include <fcntl.h>
#include <fstream>
#include <link.h>
#include <sstream>
#include <string>
#include <thread>
#include <utility>
#include <vector>

#include <sys/socket.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/un.h>
#include <unistd.h>

namespace {

struct TargetProfile {
    std::string name;
    std::uintptr_t vptrOffset{};
    std::string expectedQtClass;
};

struct Region {
    std::uintptr_t begin{};
    std::uintptr_t end{};
};

std::atomic<std::uintptr_t> g_mainBase{0};
std::vector<TargetProfile> g_targets;
std::string g_socketPath;

std::string jsonEscape(const std::string& input)
{
    std::string output;
    output.reserve(input.size() + 8);
    for (const unsigned char ch : input) {
        switch (ch) {
        case '\\': output += "\\\\"; break;
        case '"': output += "\\\""; break;
        case '\n': output += "\\n"; break;
        case '\r': output += "\\r"; break;
        case '\t': output += "\\t"; break;
        default:
            if (ch < 0x20) {
                char buffer[7]{};
                std::snprintf(buffer, sizeof(buffer), "\\u%04x", static_cast<unsigned int>(ch));
                output += buffer;
            } else {
                output += static_cast<char>(ch);
            }
        }
    }
    return output;
}

std::string errorJson(const std::string& code)
{
    return "{\"ok\":false,\"error\":\"" + jsonEscape(code) + "\"}";
}

int phdrCallback(dl_phdr_info* info, std::size_t, void*)
{
    if (info != nullptr && (info->dlpi_name == nullptr || info->dlpi_name[0] == '\0')) {
        g_mainBase.store(static_cast<std::uintptr_t>(info->dlpi_addr));
        return 1;
    }
    return 0;
}

bool parseHexOffset(const std::string& text, std::uintptr_t& output)
{
    if (text.empty()) {
        return false;
    }
    char* end = nullptr;
    errno = 0;
    const auto value = std::strtoull(text.c_str(), &end, 16);
    if (errno != 0 || end == nullptr || *end != '\0' || value == 0) {
        return false;
    }
    output = static_cast<std::uintptr_t>(value);
    return true;
}

bool loadTargets()
{
    const char* raw = std::getenv("OTCLIENT_TIBIA_RE_TARGETS");
    if (raw == nullptr || *raw == '\0') {
        return false;
    }
    std::stringstream input(raw);
    std::string item;
    while (std::getline(input, item, ';')) {
        const auto first = item.find(',');
        const auto second = first == std::string::npos ? std::string::npos : item.find(',', first + 1);
        if (first == std::string::npos || second == std::string::npos) {
            return false;
        }
        TargetProfile target;
        target.name = item.substr(0, first);
        target.expectedQtClass = item.substr(second + 1);
        if (target.name.empty() || target.expectedQtClass.empty() ||
            !parseHexOffset(item.substr(first + 1, second - first - 1), target.vptrOffset)) {
            return false;
        }
        g_targets.push_back(std::move(target));
    }
    return !g_targets.empty();
}

std::vector<Region> readWritableRegions()
{
    std::ifstream maps("/proc/self/maps");
    std::string line;
    std::vector<Region> regions;
    while (std::getline(maps, line)) {
        unsigned long long begin = 0;
        unsigned long long end = 0;
        char permissions[5]{};
        if (std::sscanf(line.c_str(), "%llx-%llx %4s", &begin, &end, permissions) != 3) {
            continue;
        }
        if (permissions[0] != 'r' || permissions[1] != 'w') {
            continue;
        }
        if (end <= begin || end - begin > (512ull << 20)) {
            continue;
        }
        regions.push_back({static_cast<std::uintptr_t>(begin), static_cast<std::uintptr_t>(end)});
    }
    return regions;
}

bool inRegion(const std::vector<Region>& regions, const std::uintptr_t address)
{
    return std::any_of(regions.begin(), regions.end(), [&](const Region& region) {
        return region.begin <= address && address < region.end;
    });
}

std::vector<std::uintptr_t> findVptrHits(const std::uintptr_t expectedVptr)
{
    constexpr std::size_t chunkSize = 1024 * 1024;
    const int fd = ::open("/proc/self/mem", O_RDONLY | O_CLOEXEC);
    if (fd < 0) {
        return {};
    }

    const auto regions = readWritableRegions();
    std::vector<std::uintptr_t> hits;
    std::vector<unsigned char> buffer(chunkSize);
    for (const auto region : regions) {
        std::uintptr_t cursor = region.begin;
        while (cursor < region.end) {
            const auto remaining = static_cast<std::size_t>(region.end - cursor);
            const auto wanted = std::min(chunkSize, remaining);
            const auto count = ::pread(fd, buffer.data(), wanted, static_cast<off_t>(cursor));
            if (count <= 0) {
                cursor += wanted;
                continue;
            }
            const auto usable = static_cast<std::size_t>(count);
            for (std::size_t offset = 0; offset + 2 * sizeof(std::uintptr_t) <= usable; offset += alignof(std::uintptr_t)) {
                std::uintptr_t value{};
                std::uintptr_t privateData{};
                std::memcpy(&value, buffer.data() + offset, sizeof(value));
                if (value != expectedVptr) {
                    continue;
                }
                std::memcpy(&privateData, buffer.data() + offset + sizeof(value), sizeof(privateData));
                if (privateData == 0 || !inRegion(regions, privateData)) {
                    continue;
                }
                hits.push_back(cursor + offset);
            }
            cursor += wanted;
        }
    }
    ::close(fd);
    std::sort(hits.begin(), hits.end());
    hits.erase(std::unique(hits.begin(), hits.end()), hits.end());
    return hits;
}

const TargetProfile* findTarget(const std::string& name)
{
    const auto it = std::find_if(g_targets.begin(), g_targets.end(), [&](const TargetProfile& target) {
        return target.name == name;
    });
    return it == g_targets.end() ? nullptr : &*it;
}

std::string discoverOnQtThread(const TargetProfile& target)
{
    const auto mainBase = g_mainBase.load();
    if (mainBase == 0) {
        return errorJson("MAIN_BASE_UNAVAILABLE");
    }
    const auto expectedVptr = mainBase + target.vptrOffset;
    const auto hits = findVptrHits(expectedVptr);
    std::size_t validated = 0;
    std::vector<std::string> classes;
    for (const auto address : hits) {
        auto* object = reinterpret_cast<QObject*>(address);
        const QMetaObject* meta = object->metaObject();
        if (meta == nullptr || meta->className() == nullptr) {
            continue;
        }
        const std::string className(meta->className());
        classes.push_back(className);
        if (className == target.expectedQtClass) {
            ++validated;
        }
    }

    std::ostringstream output;
    output << "{\"ok\":true,\"target\":\"" << jsonEscape(target.name)
           << "\",\"vptr_hits\":" << hits.size()
           << ",\"validated_hits\":" << validated
           << ",\"expected_qt_class\":\"" << jsonEscape(target.expectedQtClass) << "\",\"classes\":[";
    for (std::size_t index = 0; index < classes.size(); ++index) {
        if (index != 0) {
            output << ',';
        }
        output << '"' << jsonEscape(classes[index]) << '"';
    }
    output << "]}";
    return output.str();
}

std::string dispatchCommand(const std::string& command)
{
    if (command == "PING") {
        std::ostringstream output;
        output << "{\"ok\":true,\"command\":\"PING\",\"main_base_resolved\":"
               << (g_mainBase.load() != 0 ? "true" : "false") << '}';
        return output.str();
    }

    constexpr const char* prefix = "DISCOVER ";
    if (command.rfind(prefix, 0) != 0) {
        return errorJson("UNKNOWN_COMMAND");
    }
    const std::string targetName = command.substr(std::strlen(prefix));
    const TargetProfile* target = findTarget(targetName);
    if (target == nullptr) {
        return errorJson("UNKNOWN_TARGET");
    }
    auto* app = QCoreApplication::instance();
    if (app == nullptr) {
        return errorJson("QCOREAPPLICATION_UNAVAILABLE");
    }
    std::string result;
    const bool invoked = QMetaObject::invokeMethod(app, [&]() {
        result = discoverOnQtThread(*target);
    }, Qt::BlockingQueuedConnection);
    return invoked ? result : errorJson("QT_INVOKE_FAILED");
}

void ipcServer()
{
    for (int attempt = 0; attempt < 400 && QCoreApplication::instance() == nullptr; ++attempt) {
        std::this_thread::sleep_for(std::chrono::milliseconds(25));
    }
    dl_iterate_phdr(phdrCallback, nullptr);
    if (g_mainBase.load() == 0 || !loadTargets()) {
        return;
    }

    const char* socketEnv = std::getenv("OTCLIENT_TIBIA_RE_SOCKET");
    if (socketEnv == nullptr || *socketEnv == '\0') {
        return;
    }
    g_socketPath = socketEnv;

    sockaddr_un address{};
    if (g_socketPath.size() >= sizeof(address.sun_path)) {
        return;
    }

    ::umask(0077);
    ::unlink(g_socketPath.c_str());
    const int server = ::socket(AF_UNIX, SOCK_STREAM | SOCK_CLOEXEC, 0);
    if (server < 0) {
        return;
    }
    address.sun_family = AF_UNIX;
    std::strncpy(address.sun_path, g_socketPath.c_str(), sizeof(address.sun_path) - 1);
    if (::bind(server, reinterpret_cast<sockaddr*>(&address), sizeof(address)) != 0 ||
        ::chmod(g_socketPath.c_str(), 0600) != 0 || ::listen(server, 4) != 0) {
        ::close(server);
        ::unlink(g_socketPath.c_str());
        return;
    }

    for (;;) {
        const int client = ::accept4(server, nullptr, nullptr, SOCK_CLOEXEC);
        if (client < 0) {
            if (errno == EINTR) {
                continue;
            }
            break;
        }
        char buffer[512]{};
        const auto count = ::read(client, buffer, sizeof(buffer) - 1);
        std::string command = count > 0 ? std::string(buffer, static_cast<std::size_t>(count)) : std::string{};
        while (!command.empty() && (command.back() == '\n' || command.back() == '\r')) {
            command.pop_back();
        }
        std::string response = dispatchCommand(command);
        response.push_back('\n');
        const char* data = response.data();
        std::size_t remaining = response.size();
        while (remaining != 0) {
            const auto written = ::write(client, data, remaining);
            if (written <= 0) {
                break;
            }
            data += written;
            remaining -= static_cast<std::size_t>(written);
        }
        ::close(client);
    }
    ::close(server);
    ::unlink(g_socketPath.c_str());
}

__attribute__((constructor)) void initializeBridge()
{
    std::thread(ipcServer).detach();
}

} // namespace
