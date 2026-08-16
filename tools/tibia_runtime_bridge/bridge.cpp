#include <QtCore/QByteArray>
#include <QtCore/QCoreApplication>
#include <QtCore/QCryptographicHash>
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

struct RegionReadResult {
    bool ok{};
    std::vector<Region> regions;
    std::string error;
};

struct ScanResult {
    bool ok{};
    std::vector<std::uintptr_t> hits;
    std::string error;
};

std::atomic<std::uintptr_t> g_mainBase{0};
std::vector<TargetProfile> g_targets;
std::string g_socketPath;
std::string g_bootIdSha256;
std::string g_clientVersion;
std::string g_clientSha256;
pid_t g_pid{};
std::uint64_t g_processStartTicks{};
std::uint64_t g_clientSize{};

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

bool isLowerSha256(const std::string& value)
{
    return value.size() == 64 && std::all_of(value.begin(), value.end(), [](const unsigned char ch) {
        return (ch >= '0' && ch <= '9') || (ch >= 'a' && ch <= 'f');
    });
}

std::string sha256Text(const std::string& value)
{
    return QCryptographicHash::hash(QByteArray::fromStdString(value), QCryptographicHash::Sha256)
        .toHex()
        .toStdString();
}

bool readProcessStartTicks(std::uint64_t& output)
{
    std::ifstream statFile("/proc/self/stat");
    if (!statFile.is_open()) {
        return false;
    }
    std::string raw;
    std::getline(statFile, raw);
    const auto close = raw.rfind(')');
    if (close == std::string::npos || close + 2 >= raw.size()) {
        return false;
    }
    std::stringstream fields(raw.substr(close + 2));
    std::string token;
    for (int index = 0; index <= 19; ++index) {
        if (!(fields >> token)) {
            return false;
        }
        if (index == 19) {
            char* end = nullptr;
            errno = 0;
            const auto value = std::strtoull(token.c_str(), &end, 10);
            if (errno != 0 || end == nullptr || *end != '\0' || value == 0) {
                return false;
            }
            output = static_cast<std::uint64_t>(value);
        }
    }
    return output != 0;
}

bool loadIdentityEnvelope()
{
    const char* version = std::getenv("OTCLIENT_TIBIA_RE_CLIENT_VERSION");
    const char* sha256 = std::getenv("OTCLIENT_TIBIA_RE_BINARY_SHA256");
    if (version == nullptr || *version == '\0' || sha256 == nullptr || !isLowerSha256(sha256)) {
        return false;
    }

    std::ifstream bootFile("/proc/sys/kernel/random/boot_id");
    if (!bootFile.is_open()) {
        return false;
    }
    std::string bootId;
    std::getline(bootFile, bootId);
    if (bootId.empty()) {
        return false;
    }

    struct stat executableStat {};
    if (::stat("/proc/self/exe", &executableStat) != 0 || executableStat.st_size <= 0) {
        return false;
    }

    std::uint64_t processStartTicks = 0;
    if (!readProcessStartTicks(processStartTicks)) {
        return false;
    }

    g_bootIdSha256 = sha256Text(bootId);
    g_clientVersion = version;
    g_clientSha256 = sha256;
    g_pid = ::getpid();
    g_processStartTicks = processStartTicks;
    g_clientSize = static_cast<std::uint64_t>(executableStat.st_size);
    return !g_bootIdSha256.empty() && g_pid > 0;
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

RegionReadResult readWritableRegions()
{
    std::ifstream maps("/proc/self/maps");
    if (!maps.is_open()) {
        return {false, {}, "PROC_MAPS_OPEN_FAILED"};
    }

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
    if (maps.bad()) {
        return {false, {}, "PROC_MAPS_READ_FAILED"};
    }
    if (regions.empty()) {
        return {false, {}, "PROC_MAPS_NO_WRITABLE_REGIONS"};
    }
    return {true, std::move(regions), {}};
}

bool inRegion(const std::vector<Region>& regions, const std::uintptr_t address)
{
    return std::any_of(regions.begin(), regions.end(), [&](const Region& region) {
        return region.begin <= address && address < region.end;
    });
}

ScanResult findVptrHits(const std::uintptr_t expectedVptr)
{
    constexpr std::size_t chunkSize = 1024 * 1024;
    const int fd = ::open("/proc/self/mem", O_RDONLY | O_CLOEXEC);
    if (fd < 0) {
        return {false, {}, "PROC_MEM_OPEN_FAILED"};
    }

    const auto regionResult = readWritableRegions();
    if (!regionResult.ok) {
        ::close(fd);
        return {false, {}, regionResult.error};
    }

    const auto& regions = regionResult.regions;
    std::vector<std::uintptr_t> hits;
    std::vector<unsigned char> buffer(chunkSize);
    for (const auto region : regions) {
        std::uintptr_t cursor = region.begin;
        while (cursor < region.end) {
            const auto remaining = static_cast<std::size_t>(region.end - cursor);
            const auto wanted = std::min(chunkSize, remaining);
            ssize_t count = -1;
            do {
                count = ::pread(fd, buffer.data(), wanted, static_cast<off_t>(cursor));
            } while (count < 0 && errno == EINTR);
            if (count < 0) {
                ::close(fd);
                return {false, {}, "PROC_MEM_READ_FAILED"};
            }
            if (count == 0) {
                ::close(fd);
                return {false, {}, "PROC_MEM_UNEXPECTED_EOF"};
            }
            if (static_cast<std::size_t>(count) != wanted) {
                ::close(fd);
                return {false, {}, "PROC_MEM_SHORT_READ"};
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
    return {true, std::move(hits), {}};
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
    const auto scan = findVptrHits(expectedVptr);
    if (!scan.ok) {
        return errorJson(scan.error);
    }

    std::size_t validated = 0;
    std::vector<std::string> classes;
    for (const auto address : scan.hits) {
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
           << "\",\"scan_status\":\"OK\""
           << ",\"vptr_hits\":" << scan.hits.size()
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
               << (g_mainBase.load() != 0 ? "true" : "false")
               << ",\"boot_id_sha256\":\"" << jsonEscape(g_bootIdSha256) << '"'
               << ",\"pid\":" << g_pid
               << ",\"process_start_ticks\":" << g_processStartTicks
               << ",\"client_version\":\"" << jsonEscape(g_clientVersion) << '"'
               << ",\"client_size\":" << g_clientSize
               << ",\"client_sha256\":\"" << jsonEscape(g_clientSha256) << "\"}";
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
    if (g_mainBase.load() == 0 || !loadIdentityEnvelope() || !loadTargets()) {
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
