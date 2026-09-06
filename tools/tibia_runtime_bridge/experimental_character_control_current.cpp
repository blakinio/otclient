#ifndef _GNU_SOURCE
#define _GNU_SOURCE
#endif

#include <QtCore/QCoreApplication>
#include <QtCore/QCryptographicHash>
#include <QtCore/QFile>
#include <QtCore/QJsonArray>
#include <QtCore/QJsonDocument>
#include <QtCore/QJsonObject>
#include <QtCore/QList>
#include <QtCore/QMetaMethod>
#include <QtCore/QMetaObject>
#include <QtCore/QMetaProperty>
#include <QtCore/QObject>
#include <QtCore/QThread>
#include <QtCore/QVariant>

#include <algorithm>
#include <array>
#include <atomic>
#include <cerrno>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <fstream>
#include <link.h>
#include <string>
#include <thread>
#include <vector>

#include <dlfcn.h>
#include <fcntl.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/un.h>
#include <unistd.h>

namespace {

constexpr std::uint64_t kClientSize = 52105824;
constexpr char kClientSha256[] = "552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1";
constexpr std::uintptr_t kCharacterControllerVptrOffset = 0x30c29a8;
constexpr char kCharacterControllerClass[] = "tibia::gamewindow::TCharacterSelectionController";
constexpr char kConfirmSignature[] = "onCharacterSelectionConfirmed(QList<int>)";

struct Region {
    std::uintptr_t begin{};
    std::uintptr_t end{};
};

std::atomic<std::uintptr_t> gMainBase{0};
std::string gSocketPath;

int phdrCallback(dl_phdr_info* info, std::size_t, void*)
{
    if (info != nullptr && (info->dlpi_name == nullptr || info->dlpi_name[0] == '\0')) {
        gMainBase.store(static_cast<std::uintptr_t>(info->dlpi_addr));
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

std::vector<Region> readWritableRegions()
{
    std::ifstream maps("/proc/self/maps");
    std::vector<Region> regions;
    std::string line;
    while (std::getline(maps, line)) {
        unsigned long long begin = 0;
        unsigned long long end = 0;
        char permissions[5]{};
        if (std::sscanf(line.c_str(), "%llx-%llx %4s", &begin, &end, permissions) != 3) {
            continue;
        }
        if (permissions[0] != 'r' || permissions[1] != 'w' || end <= begin || end - begin > (512ull << 20)) {
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

QObject* findCharacterController()
{
    const auto mainBase = gMainBase.load();
    if (mainBase == 0) {
        return nullptr;
    }
    const auto regions = readWritableRegions();
    if (regions.empty()) {
        return nullptr;
    }
    const int fd = ::open("/proc/self/mem", O_RDONLY | O_CLOEXEC);
    if (fd < 0) {
        return nullptr;
    }
    constexpr std::size_t chunkSize = 1024 * 1024;
    std::vector<unsigned char> buffer(chunkSize);
    std::vector<QObject*> hits;
    const auto expectedVptr = mainBase + kCharacterControllerVptrOffset;
    for (const auto region : regions) {
        std::uintptr_t cursor = region.begin;
        while (cursor < region.end) {
            const auto wanted = std::min<std::size_t>(chunkSize, static_cast<std::size_t>(region.end - cursor));
            const auto count = ::pread(fd, buffer.data(), wanted, static_cast<off_t>(cursor));
            if (count < 0 || static_cast<std::size_t>(count) != wanted) {
                ::close(fd);
                return nullptr;
            }
            for (std::size_t offset = 0; offset + 2 * sizeof(std::uintptr_t) <= wanted; offset += alignof(std::uintptr_t)) {
                std::uintptr_t value = 0;
                std::uintptr_t privateData = 0;
                std::memcpy(&value, buffer.data() + offset, sizeof(value));
                if (value != expectedVptr) {
                    continue;
                }
                std::memcpy(&privateData, buffer.data() + offset + sizeof(value), sizeof(privateData));
                if (privateData == 0 || !inRegion(regions, privateData)) {
                    continue;
                }
                auto* object = reinterpret_cast<QObject*>(cursor + offset);
                const QMetaObject* meta = object->metaObject();
                if (meta != nullptr && meta->className() != nullptr && std::strcmp(meta->className(), kCharacterControllerClass) == 0) {
                    hits.push_back(object);
                }
            }
            cursor += wanted;
        }
    }
    ::close(fd);
    std::sort(hits.begin(), hits.end());
    hits.erase(std::unique(hits.begin(), hits.end()), hits.end());
    return hits.size() == 1 ? hits.front() : nullptr;
}

QList<QObject*> currentCharacters(QObject* controller, bool& ok)
{
    ok = false;
    const QMetaObject* meta = controller->metaObject();
    const int propertyIndex = meta->indexOfProperty("characterList");
    if (propertyIndex < 0) {
        return {};
    }
    const QMetaProperty property = meta->property(propertyIndex);
    const QVariant value = property.read(controller);
    if (!value.isValid() || !value.canConvert<QList<QObject*>>()) {
        return {};
    }
    ok = true;
    return value.value<QList<QObject*>>();
}

QJsonObject stateObject(QObject* controller)
{
    bool listOk = false;
    const QList<QObject*> characters = currentCharacters(controller, listOk);
    if (!listOk) {
        return {{"ok", false}, {"error", "CHARACTER_LIST_PROPERTY_UNAVAILABLE"}};
    }
    QJsonArray names;
    for (QObject* character : characters) {
        QString name;
        if (character != nullptr) {
            for (const char* propertyName : std::array<const char*, 2>{"name", "characterName"}) {
                const QVariant value = character->property(propertyName);
                if (value.isValid()) {
                    name = value.toString();
                    if (!name.isEmpty()) {
                        break;
                    }
                }
            }
        }
        names.append(name);
    }
    const QMetaObject* meta = controller->metaObject();
    const int methodIndex = meta->indexOfMethod(kConfirmSignature);
    return {
        {"ok", true},
        {"character_count", characters.size()},
        {"character_names", names},
        {"confirm_method_present", methodIndex >= 0},
    };
}

QJsonObject dispatchOnQtThread(const std::string& command)
{
    QObject* controller = findCharacterController();
    if (controller == nullptr) {
        return {{"ok", false}, {"error", "CHARACTER_CONTROLLER_NOT_UNIQUE"}};
    }
    if (controller->thread() != QThread::currentThread()) {
        return {{"ok", false}, {"error", "CHARACTER_CONTROLLER_THREAD_MISMATCH"}};
    }
    if (command == "STATE") {
        return stateObject(controller);
    }
    if (command != "CONFIRM_UNIQUE") {
        return {{"ok", false}, {"error", "UNKNOWN_COMMAND"}};
    }

    bool listOk = false;
    const QList<QObject*> characters = currentCharacters(controller, listOk);
    if (!listOk) {
        return {{"ok", false}, {"error", "CHARACTER_LIST_PROPERTY_UNAVAILABLE"}};
    }
    if (characters.size() != 1) {
        return {{"ok", false}, {"error", "CHARACTER_COUNT_NOT_ONE"}, {"character_count", characters.size()}};
    }

    const QMetaObject* meta = controller->metaObject();
    const int methodIndex = meta->indexOfMethod(kConfirmSignature);
    if (methodIndex < 0) {
        return {{"ok", false}, {"error", "CONFIRM_METHOD_MISSING"}};
    }
    const QMetaMethod method = meta->method(methodIndex);
    if (method.parameterCount() != 1 || method.parameterTypes().size() != 1 || method.parameterTypes().front() != QByteArray("QList<int>")) {
        return {{"ok", false}, {"error", "CONFIRM_METHOD_SIGNATURE_MISMATCH"}};
    }
    QList<int> selectedCharacters{0};
    const bool invoked = method.invoke(controller, Qt::DirectConnection, Q_ARG(QList<int>, selectedCharacters));
    if (!invoked) {
        return {{"ok", false}, {"error", "CONFIRM_INVOKE_FAILED"}};
    }
    return {{"ok", true}, {"character_index", 0}, {"confirmation_dispatched", true}};
}

QJsonObject dispatchCommand(const std::string& command)
{
    auto* app = QCoreApplication::instance();
    if (app == nullptr) {
        return {{"ok", false}, {"error", "QCOREAPPLICATION_UNAVAILABLE"}};
    }
    QJsonObject result;
    const bool invoked = QMetaObject::invokeMethod(app, [&]() {
        result = dispatchOnQtThread(command);
    }, Qt::BlockingQueuedConnection);
    return invoked ? result : QJsonObject{{"ok", false}, {"error", "QT_INVOKE_FAILED"}};
}

bool sameUidPeer(const int client)
{
    struct ucred peer {};
    socklen_t length = sizeof(peer);
    return ::getsockopt(client, SOL_SOCKET, SO_PEERCRED, &peer, &length) == 0 &&
        length == sizeof(peer) && peer.uid == ::geteuid();
}

void ipcServer()
{
    for (int attempt = 0; attempt < 400 && QCoreApplication::instance() == nullptr; ++attempt) {
        std::this_thread::sleep_for(std::chrono::milliseconds(25));
    }
    if (QCoreApplication::instance() == nullptr || !verifyExactExecutable()) {
        return;
    }
    dl_iterate_phdr(phdrCallback, nullptr);
    if (gMainBase.load() == 0) {
        return;
    }
    const char* socketEnv = std::getenv("OTCLIENT_TIBIA_RE_CHARACTER_SOCKET");
    if (socketEnv == nullptr || socketEnv[0] != '/') {
        return;
    }
    gSocketPath = socketEnv;
    if (gSocketPath.size() >= sizeof(sockaddr_un::sun_path)) {
        return;
    }

    ::umask(0077);
    ::unlink(gSocketPath.c_str());
    const int server = ::socket(AF_UNIX, SOCK_STREAM | SOCK_CLOEXEC, 0);
    if (server < 0) {
        return;
    }
    sockaddr_un address {};
    address.sun_family = AF_UNIX;
    std::strncpy(address.sun_path, gSocketPath.c_str(), sizeof(address.sun_path) - 1);
    if (::bind(server, reinterpret_cast<sockaddr*>(&address), sizeof(address)) != 0 ||
        ::chmod(gSocketPath.c_str(), 0600) != 0 || ::listen(server, 4) != 0) {
        ::close(server);
        ::unlink(gSocketPath.c_str());
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
        char buffer[64]{};
        const auto count = ::read(client, buffer, sizeof(buffer) - 1);
        std::string command = count > 0 ? std::string(buffer, static_cast<std::size_t>(count)) : std::string{};
        while (!command.empty() && (command.back() == '\n' || command.back() == '\r')) {
            command.pop_back();
        }
        const QJsonObject response = sameUidPeer(client)
            ? dispatchCommand(command)
            : QJsonObject{{"ok", false}, {"error", "IPC_PEER_UID_MISMATCH"}};
        QByteArray encoded = QJsonDocument(response).toJson(QJsonDocument::Compact);
        encoded.append('\n');
        const char* cursor = encoded.constData();
        std::size_t remaining = static_cast<std::size_t>(encoded.size());
        while (remaining != 0) {
            const auto written = ::write(client, cursor, remaining);
            if (written <= 0) {
                break;
            }
            cursor += written;
            remaining -= static_cast<std::size_t>(written);
        }
        ::close(client);
    }
    ::close(server);
    ::unlink(gSocketPath.c_str());
}

__attribute__((constructor)) void initializeCharacterControl()
{
    std::thread(ipcServer).detach();
}

} // namespace
