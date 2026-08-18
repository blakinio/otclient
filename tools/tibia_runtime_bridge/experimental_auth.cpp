#ifndef _GNU_SOURCE
#define _GNU_SOURCE
#endif

#include <QtCore/QByteArray>
#include <QtCore/QCoreApplication>
#include <QtCore/QCryptographicHash>
#include <QtCore/QFile>
#include <QtCore/QMetaMethod>
#include <QtCore/QMetaObject>
#include <QtCore/QObject>
#include <QtCore/QString>
#include <QtCore/QThread>

#include <algorithm>
#include <array>
#include <atomic>
#include <cerrno>
#include <chrono>
#include <cstddef>
#include <cstdint>
#include <cstdio>
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

constexpr std::uint64_t kClientSize = 51965216;
constexpr char kClientSha256[] = "e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe";
constexpr std::uintptr_t kGameClientVptrOffset = 0x3076908;
constexpr char kGameClientClass[] = "tibia::client::TGameClient";
constexpr int kGameClientLocalMethodCount = 44;
constexpr int kColdAuthMethodId = 17;
constexpr char kColdAuthSignature[] = "onRequestLoginWithCredentials(QString,QString)";
constexpr std::uintptr_t kColdAuthTargetOffset = 0xd06850;
constexpr std::array<unsigned char, 32> kColdAuthFence = {
    0x48, 0x8b, 0x51, 0x10, 0x48, 0x8b, 0x71, 0x08,
    0x48, 0x83, 0xc4, 0x48, 0x5b, 0x5d, 0xe9, 0x2d,
    0x38, 0x9e, 0xff, 0x0f, 0x1f, 0x44, 0x00, 0x00,
    0x48, 0x8b, 0xbf, 0xa0, 0x09, 0x00, 0x00, 0x48,
};
constexpr std::size_t kMaxCredentialBytes = 1024;
constexpr std::size_t kCredentialHeaderBytes = 8;
constexpr std::size_t kMaxCredentialFrameBytes = kCredentialHeaderBytes + 2 * kMaxCredentialBytes;

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

struct IpcRequest {
    bool ok{};
    std::string command;
    std::vector<int> fileDescriptors;
    std::string error;
};

std::atomic<std::uintptr_t> g_mainBase{0};
std::string g_authSocketPath;

void wipeMemory(void* data, const std::size_t size)
{
    auto* cursor = static_cast<volatile unsigned char*>(data);
    for (std::size_t index = 0; index < size; ++index) {
        cursor[index] = 0;
    }
}

void wipeByteArray(QByteArray& value)
{
    if (!value.isEmpty()) {
        wipeMemory(value.data(), static_cast<std::size_t>(value.size()));
    }
    value.clear();
}

void wipeQString(QString& value)
{
    value.detach();
    if (!value.isEmpty()) {
        wipeMemory(value.data(), static_cast<std::size_t>(value.size()) * sizeof(QChar));
    }
    value.clear();
}

class WipedBytes final {
public:
    explicit WipedBytes(const std::size_t size)
        : bytes(size)
    {
    }

    ~WipedBytes()
    {
        if (!bytes.empty()) {
            wipeMemory(bytes.data(), bytes.size());
        }
    }

    WipedBytes(const WipedBytes&) = delete;
    WipedBytes& operator=(const WipedBytes&) = delete;

    std::vector<unsigned char> bytes;
};

std::string errorJson(const std::string& code)
{
    return "{\"ok\":false,\"error\":\"" + code + "\"}";
}

int phdrCallback(dl_phdr_info* info, std::size_t, void*)
{
    if (info != nullptr && (info->dlpi_name == nullptr || info->dlpi_name[0] == '\0')) {
        g_mainBase.store(static_cast<std::uintptr_t>(info->dlpi_addr));
        return 1;
    }
    return 0;
}

bool verifyExactExecutable()
{
    struct stat executableStat {};
    if (::stat("/proc/self/exe", &executableStat) != 0 || executableStat.st_size != static_cast<off_t>(kClientSize)) {
        return false;
    }

    QFile executable("/proc/self/exe");
    if (!executable.open(QIODevice::ReadOnly)) {
        return false;
    }
    QCryptographicHash hash(QCryptographicHash::Sha256);
    while (!executable.atEnd()) {
        const QByteArray chunk = executable.read(1024 * 1024);
        if (chunk.isEmpty() && executable.error() != QFileDevice::NoError) {
            return false;
        }
        hash.addData(chunk);
    }
    return hash.result().toHex() == QByteArray(kClientSha256);
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
            if (count < 0 || static_cast<std::size_t>(count) != wanted) {
                ::close(fd);
                return {false, {}, count < 0 ? "PROC_MEM_READ_FAILED" : "PROC_MEM_SHORT_READ"};
            }

            for (std::size_t offset = 0; offset + 2 * sizeof(std::uintptr_t) <= wanted; offset += alignof(std::uintptr_t)) {
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

bool readSelfMemory(const std::uintptr_t address, void* output, const std::size_t size)
{
    const int fd = ::open("/proc/self/mem", O_RDONLY | O_CLOEXEC);
    if (fd < 0) {
        return false;
    }
    std::size_t completed = 0;
    while (completed < size) {
        ssize_t count = -1;
        do {
            count = ::pread(
                fd,
                static_cast<unsigned char*>(output) + completed,
                size - completed,
                static_cast<off_t>(address + completed));
        } while (count < 0 && errno == EINTR);
        if (count <= 0) {
            ::close(fd);
            return false;
        }
        completed += static_cast<std::size_t>(count);
    }
    ::close(fd);
    return true;
}

bool coldAuthFenceMatches()
{
    const auto mainBase = g_mainBase.load();
    if (mainBase == 0) {
        return false;
    }
    std::array<unsigned char, 32> actual{};
    return readSelfMemory(mainBase + kColdAuthTargetOffset, actual.data(), actual.size()) && actual == kColdAuthFence;
}

std::uint32_t readLe32(const unsigned char* bytes)
{
    return static_cast<std::uint32_t>(bytes[0]) |
        (static_cast<std::uint32_t>(bytes[1]) << 8u) |
        (static_cast<std::uint32_t>(bytes[2]) << 16u) |
        (static_cast<std::uint32_t>(bytes[3]) << 24u);
}

bool isMemfdLinkTarget(const std::string& target)
{
    return target.rfind("/memfd:", 0) == 0 || target.rfind("memfd:", 0) == 0;
}

std::string readCredentialMemfd(const int fd, QByteArray& email, QByteArray& password)
{
    if (fd < 0) {
        return "CREDENTIAL_FD_MISSING";
    }

    char linkPath[64]{};
    std::snprintf(linkPath, sizeof(linkPath), "/proc/self/fd/%d", fd);
    char linkTarget[256]{};
    const auto linkLength = ::readlink(linkPath, linkTarget, sizeof(linkTarget) - 1);
    if (linkLength <= 0) {
        return "CREDENTIAL_FD_IDENTITY_FAILED";
    }
    const std::string linkText(linkTarget, static_cast<std::size_t>(linkLength));
    if (!isMemfdLinkTarget(linkText)) {
        return "CREDENTIAL_FD_NOT_MEMFD";
    }

    struct stat descriptorStat {};
    if (::fstat(fd, &descriptorStat) != 0 || !S_ISREG(descriptorStat.st_mode)) {
        return "CREDENTIAL_FD_NOT_REGULAR";
    }
    if (descriptorStat.st_size < static_cast<off_t>(kCredentialHeaderBytes + 2) ||
        descriptorStat.st_size > static_cast<off_t>(kMaxCredentialFrameBytes)) {
        return "CREDENTIAL_FRAME_SIZE_INVALID";
    }

#if defined(F_GET_SEALS) && defined(F_SEAL_SEAL) && defined(F_SEAL_SHRINK) && defined(F_SEAL_GROW) && defined(F_SEAL_WRITE)
    const int seals = ::fcntl(fd, F_GET_SEALS);
    const int requiredSeals = F_SEAL_SEAL | F_SEAL_SHRINK | F_SEAL_GROW | F_SEAL_WRITE;
    if (seals < 0 || (seals & requiredSeals) != requiredSeals) {
        return "CREDENTIAL_MEMFD_NOT_SEALED";
    }
#else
    return "CREDENTIAL_MEMFD_SEALS_UNAVAILABLE";
#endif

    WipedBytes raw(static_cast<std::size_t>(descriptorStat.st_size));
    std::size_t completed = 0;
    while (completed < raw.bytes.size()) {
        ssize_t count = -1;
        do {
            count = ::pread(
                fd,
                raw.bytes.data() + completed,
                raw.bytes.size() - completed,
                static_cast<off_t>(completed));
        } while (count < 0 && errno == EINTR);
        if (count <= 0) {
            return "CREDENTIAL_MEMFD_READ_FAILED";
        }
        completed += static_cast<std::size_t>(count);
    }

    const std::uint32_t emailLength = readLe32(raw.bytes.data());
    const std::uint32_t passwordLength = readLe32(raw.bytes.data() + 4);
    if (emailLength == 0 || passwordLength == 0 ||
        emailLength > kMaxCredentialBytes || passwordLength > kMaxCredentialBytes) {
        return "CREDENTIAL_LENGTH_INVALID";
    }
    const std::size_t expectedSize = kCredentialHeaderBytes + emailLength + passwordLength;
    if (expectedSize != raw.bytes.size()) {
        return "CREDENTIAL_FRAME_LENGTH_MISMATCH";
    }

    const auto emailBegin = raw.bytes.begin() + static_cast<std::ptrdiff_t>(kCredentialHeaderBytes);
    const auto emailEnd = emailBegin + static_cast<std::ptrdiff_t>(emailLength);
    const auto passwordEnd = emailEnd + static_cast<std::ptrdiff_t>(passwordLength);
    if (std::find(emailBegin, emailEnd, 0) != emailEnd || std::find(emailEnd, passwordEnd, 0) != passwordEnd) {
        return "CREDENTIAL_NUL_FORBIDDEN";
    }

    email = QByteArray(reinterpret_cast<const char*>(raw.bytes.data() + kCredentialHeaderBytes), static_cast<qsizetype>(emailLength));
    password = QByteArray(
        reinterpret_cast<const char*>(raw.bytes.data() + kCredentialHeaderBytes + emailLength),
        static_cast<qsizetype>(passwordLength));
    return {};
}

bool decodeUtf8Exact(const QByteArray& bytes, QString& output)
{
    output = QString::fromUtf8(bytes);
    QByteArray roundTrip = output.toUtf8();
    const bool valid = roundTrip == bytes;
    wipeByteArray(roundTrip);
    return valid;
}

std::string authOnQtThread(const QByteArray& emailBytes, const QByteArray& passwordBytes)
{
    if (!coldAuthFenceMatches()) {
        return errorJson("COLD_AUTH_INSTRUCTION_FENCE_MISMATCH");
    }

    const auto mainBase = g_mainBase.load();
    if (mainBase == 0) {
        return errorJson("MAIN_BASE_UNAVAILABLE");
    }
    const auto scan = findVptrHits(mainBase + kGameClientVptrOffset);
    if (!scan.ok) {
        return errorJson(scan.error);
    }
    if (scan.hits.size() != 1) {
        return errorJson("GAME_CLIENT_VPTR_NOT_UNIQUE");
    }

    auto* object = reinterpret_cast<QObject*>(scan.hits.front());
    const QMetaObject* meta = object->metaObject();
    if (meta == nullptr || meta->className() == nullptr || std::strcmp(meta->className(), kGameClientClass) != 0) {
        return errorJson("GAME_CLIENT_QT_CLASS_MISMATCH");
    }
    if (object->thread() != QThread::currentThread()) {
        return errorJson("GAME_CLIENT_QT_THREAD_MISMATCH");
    }

    const int localMethodCount = meta->methodCount() - meta->methodOffset();
    if (localMethodCount != kGameClientLocalMethodCount || kColdAuthMethodId >= localMethodCount) {
        return errorJson("GAME_CLIENT_QMETA_METHOD_COUNT_MISMATCH");
    }
    const QMetaMethod method = meta->method(meta->methodOffset() + kColdAuthMethodId);
    if (!method.isValid() || method.methodSignature() != QByteArray(kColdAuthSignature) || method.parameterCount() != 2) {
        return errorJson("GAME_CLIENT_QMETA_METHOD_MISMATCH");
    }

    QString email;
    QString password;
    if (!decodeUtf8Exact(emailBytes, email) || !decodeUtf8Exact(passwordBytes, password)) {
        wipeQString(email);
        wipeQString(password);
        return errorJson("CREDENTIAL_UTF8_INVALID");
    }

    const bool invoked = QMetaObject::invokeMethod(
        object,
        "onRequestLoginWithCredentials",
        Qt::DirectConnection,
        Q_ARG(QString, email),
        Q_ARG(QString, password));
    wipeQString(email);
    wipeQString(password);
    if (!invoked) {
        return errorJson("COLD_AUTH_QMETA_INVOKE_FAILED");
    }
    return "{\"ok\":true,\"command\":\"AUTH_WITH_CREDENTIALS\",\"qmeta_method_id\":17,\"invocation_dispatched\":true}";
}

std::string authWithCredentials(const int credentialsFd)
{
    QByteArray emailBytes;
    QByteArray passwordBytes;
    const std::string frameError = readCredentialMemfd(credentialsFd, emailBytes, passwordBytes);
    if (!frameError.empty()) {
        wipeByteArray(emailBytes);
        wipeByteArray(passwordBytes);
        return errorJson(frameError);
    }

    auto* app = QCoreApplication::instance();
    if (app == nullptr) {
        wipeByteArray(emailBytes);
        wipeByteArray(passwordBytes);
        return errorJson("QCOREAPPLICATION_UNAVAILABLE");
    }

    std::string result;
    const bool scheduled = QMetaObject::invokeMethod(app, [&]() {
        result = authOnQtThread(emailBytes, passwordBytes);
    }, Qt::BlockingQueuedConnection);
    wipeByteArray(emailBytes);
    wipeByteArray(passwordBytes);
    return scheduled ? result : errorJson("QT_AUTH_SCHEDULING_FAILED");
}

IpcRequest receiveRequest(const int client)
{
    char commandBuffer[128]{};
    char controlBuffer[CMSG_SPACE(sizeof(int) * 4)]{};
    iovec io{};
    io.iov_base = commandBuffer;
    io.iov_len = sizeof(commandBuffer) - 1;
    msghdr message{};
    message.msg_iov = &io;
    message.msg_iovlen = 1;
    message.msg_control = controlBuffer;
    message.msg_controllen = sizeof(controlBuffer);

    ssize_t count = -1;
    do {
        count = ::recvmsg(client, &message, MSG_CMSG_CLOEXEC);
    } while (count < 0 && errno == EINTR);
    if (count <= 0) {
        return {false, {}, {}, "IPC_REQUEST_READ_FAILED"};
    }

    IpcRequest request{true, std::string(commandBuffer, static_cast<std::size_t>(count)), {}, {}};
    for (cmsghdr* header = CMSG_FIRSTHDR(&message); header != nullptr; header = CMSG_NXTHDR(&message, header)) {
        if (header->cmsg_level != SOL_SOCKET || header->cmsg_type != SCM_RIGHTS || header->cmsg_len < CMSG_LEN(sizeof(int))) {
            if (request.error.empty()) {
                request.error = "IPC_ANCILLARY_DATA_INVALID";
            }
            request.ok = false;
            continue;
        }
        const std::size_t payloadBytes = header->cmsg_len - CMSG_LEN(0);
        if (payloadBytes % sizeof(int) != 0) {
            if (request.error.empty()) {
                request.error = "IPC_ANCILLARY_DATA_INVALID";
            }
            request.ok = false;
            continue;
        }
        const std::size_t descriptorCount = payloadBytes / sizeof(int);
        const auto* descriptors = reinterpret_cast<const int*>(CMSG_DATA(header));
        request.fileDescriptors.insert(request.fileDescriptors.end(), descriptors, descriptors + descriptorCount);
    }

    if ((message.msg_flags & (MSG_CTRUNC | MSG_TRUNC)) != 0) {
        if (request.error.empty()) {
            request.error = "IPC_REQUEST_TRUNCATED";
        }
        request.ok = false;
    }

    while (!request.command.empty() && (request.command.back() == '\n' || request.command.back() == '\r')) {
        request.command.pop_back();
    }
    if (request.command.empty() || request.command.find('\n') != std::string::npos || request.command.find('\r') != std::string::npos) {
        if (request.error.empty()) {
            request.error = "IPC_COMMAND_INVALID";
        }
        request.ok = false;
    }
    return request;
}

bool sameUserPeer(const int client)
{
    ucred credentials{};
    socklen_t length = sizeof(credentials);
    return ::getsockopt(client, SOL_SOCKET, SO_PEERCRED, &credentials, &length) == 0 &&
        length == sizeof(credentials) && credentials.uid == ::geteuid();
}

void writeResponse(const int client, std::string response)
{
    response.push_back('\n');
    const char* data = response.data();
    std::size_t remaining = response.size();
    while (remaining != 0) {
        ssize_t written = -1;
        do {
            written = ::write(client, data, remaining);
        } while (written < 0 && errno == EINTR);
        if (written <= 0) {
            break;
        }
        data += written;
        remaining -= static_cast<std::size_t>(written);
    }
}

void authServer()
{
    for (int attempt = 0; attempt < 400 && QCoreApplication::instance() == nullptr; ++attempt) {
        std::this_thread::sleep_for(std::chrono::milliseconds(25));
    }
    if (QCoreApplication::instance() == nullptr || !verifyExactExecutable()) {
        return;
    }
    dl_iterate_phdr(phdrCallback, nullptr);
    if (g_mainBase.load() == 0) {
        return;
    }

    const char* socketEnv = std::getenv("OTCLIENT_TIBIA_RE_AUTH_SOCKET");
    if (socketEnv == nullptr || socketEnv[0] != '/') {
        return;
    }
    g_authSocketPath = socketEnv;
    sockaddr_un address{};
    if (g_authSocketPath.size() >= sizeof(address.sun_path)) {
        return;
    }
    struct stat existing {};
    errno = 0;
    if (::lstat(g_authSocketPath.c_str(), &existing) == 0 || errno != ENOENT) {
        return;
    }

    const int server = ::socket(AF_UNIX, SOCK_STREAM | SOCK_CLOEXEC, 0);
    if (server < 0) {
        return;
    }
    ::umask(0077);
    address.sun_family = AF_UNIX;
    std::strncpy(address.sun_path, g_authSocketPath.c_str(), sizeof(address.sun_path) - 1);
    if (::bind(server, reinterpret_cast<sockaddr*>(&address), sizeof(address)) != 0 ||
        ::chmod(g_authSocketPath.c_str(), 0600) != 0 || ::listen(server, 1) != 0) {
        ::close(server);
        ::unlink(g_authSocketPath.c_str());
        return;
    }

    const int client = ::accept4(server, nullptr, nullptr, SOCK_CLOEXEC);
    if (client >= 0) {
        timeval timeout{};
        timeout.tv_sec = 3;
        ::setsockopt(client, SOL_SOCKET, SO_RCVTIMEO, &timeout, sizeof(timeout));

        IpcRequest request = receiveRequest(client);
        std::string response;
        if (!sameUserPeer(client)) {
            response = errorJson("IPC_PEER_UID_MISMATCH");
        } else if (!request.ok) {
            response = errorJson(request.error);
        } else if (request.command != "AUTH_WITH_CREDENTIALS") {
            response = errorJson("UNKNOWN_COMMAND");
        } else if (request.fileDescriptors.size() != 1) {
            response = errorJson("CREDENTIAL_FD_COUNT_INVALID");
        } else {
            response = authWithCredentials(request.fileDescriptors.front());
        }
        for (const int fd : request.fileDescriptors) {
            if (fd >= 0) {
                ::close(fd);
            }
        }
        writeResponse(client, std::move(response));
        ::close(client);
    }

    ::close(server);
    ::unlink(g_authSocketPath.c_str());
}

__attribute__((constructor)) void initializeExperimentalAuth()
{
    std::thread(authServer).detach();
}

} // namespace
