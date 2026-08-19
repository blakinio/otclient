#ifndef _GNU_SOURCE
#define _GNU_SOURCE
#endif

#include <array>
#include <cerrno>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>
#include <vector>

#include <fcntl.h>
#include <sys/mman.h>
#include <sys/prctl.h>
#include <sys/resource.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/uio.h>
#include <sys/un.h>
#include <unistd.h>

namespace {

constexpr std::size_t kMaxSecretBytes = 1024;
constexpr char kEmailEnv[] = "TIBIA_TEST_EMAIL";
constexpr char kPasswordEnv[] = "TIBIA_TEST_PASSWORD";
constexpr char kCommand[] = "AUTH_WITH_CREDENTIALS\n";

void wipe(void* data, const std::size_t size)
{
    auto* cursor = static_cast<volatile unsigned char*>(data);
    for (std::size_t index = 0; index < size; ++index) {
        cursor[index] = 0;
    }
}

bool loadAndEraseSecret(const char* name, std::vector<unsigned char>& output)
{
    char* value = std::getenv(name);
    if (value == nullptr) {
        return false;
    }
    const std::size_t length = ::strnlen(value, kMaxSecretBytes + 1);
    if (length == 0 || length > kMaxSecretBytes) {
        return false;
    }
    output.assign(reinterpret_cast<unsigned char*>(value), reinterpret_cast<unsigned char*>(value) + length);
    if (::mlock(output.data(), output.size()) != 0) {
        wipe(output.data(), output.size());
        output.clear();
        return false;
    }
    wipe(value, length);
    if (::unsetenv(name) != 0) {
        wipe(output.data(), output.size());
        ::munlock(output.data(), output.size());
        output.clear();
        return false;
    }
    return true;
}

void wipeAndUnlock(std::vector<unsigned char>& value)
{
    if (!value.empty()) {
        wipe(value.data(), value.size());
        ::munlock(value.data(), value.size());
        value.clear();
    }
}

void putLe32(unsigned char* output, const std::uint32_t value)
{
    output[0] = static_cast<unsigned char>(value & 0xffu);
    output[1] = static_cast<unsigned char>((value >> 8u) & 0xffu);
    output[2] = static_cast<unsigned char>((value >> 16u) & 0xffu);
    output[3] = static_cast<unsigned char>((value >> 24u) & 0xffu);
}

bool responseIsSuccess(const std::string& response)
{
    const auto newline = response.find('\n');
    const std::string line = response.substr(0, newline);
    return line.find("\"ok\":true") != std::string::npos &&
        line.find("\"invocation_dispatched\":true") != std::string::npos &&
        line.find("\"qmeta_method_id\":17") != std::string::npos &&
        line.find("\"qmeta_signature\":\"onRequestLoginWithCredentials(QString,QString)\"") != std::string::npos;
}

} // namespace

int main(int argc, char** argv)
{
    if (argc != 3) {
        std::fprintf(stderr, "current secret ingress error: BAD_ARGUMENTS\n");
        return 2;
    }
    char* end = nullptr;
    errno = 0;
    const long expectedPidLong = std::strtol(argv[2], &end, 10);
    if (errno != 0 || end == nullptr || *end != '\0' || expectedPidLong <= 0) {
        std::fprintf(stderr, "current secret ingress error: BAD_EXPECTED_PID\n");
        return 2;
    }
    const pid_t expectedPid = static_cast<pid_t>(expectedPidLong);

    struct rlimit coreLimit {};
    coreLimit.rlim_cur = 0;
    coreLimit.rlim_max = 0;
    if (::setrlimit(RLIMIT_CORE, &coreLimit) != 0 || ::prctl(PR_SET_DUMPABLE, 0, 0, 0, 0) != 0) {
        std::fprintf(stderr, "current secret ingress error: PROCESS_HARDENING_FAILED\n");
        return 2;
    }

    std::vector<unsigned char> email;
    std::vector<unsigned char> password;
    if (!loadAndEraseSecret(kEmailEnv, email)) {
        std::fprintf(stderr, "current secret ingress error: EMAIL_SOURCE_FAILED\n");
        return 2;
    }
    if (!loadAndEraseSecret(kPasswordEnv, password)) {
        wipeAndUnlock(email);
        std::fprintf(stderr, "current secret ingress error: PASSWORD_SOURCE_FAILED\n");
        return 2;
    }

    const int credentialFd = ::memfd_create("otclient-tibia-native-auth", MFD_CLOEXEC | MFD_ALLOW_SEALING);
    if (credentialFd < 0) {
        wipeAndUnlock(email);
        wipeAndUnlock(password);
        std::fprintf(stderr, "current secret ingress error: MEMFD_CREATE_FAILED\n");
        return 2;
    }

    std::array<unsigned char, 8> header{};
    putLe32(header.data(), static_cast<std::uint32_t>(email.size()));
    putLe32(header.data() + 4, static_cast<std::uint32_t>(password.size()));
    std::array<iovec, 3> vectors{};
    vectors[0] = {header.data(), header.size()};
    vectors[1] = {email.data(), email.size()};
    vectors[2] = {password.data(), password.size()};
    const std::size_t expectedSize = header.size() + email.size() + password.size();
    const ssize_t written = ::writev(credentialFd, vectors.data(), static_cast<int>(vectors.size()));
    wipeAndUnlock(email);
    wipeAndUnlock(password);
    wipe(header.data(), header.size());
    if (written != static_cast<ssize_t>(expectedSize)) {
        ::close(credentialFd);
        std::fprintf(stderr, "current secret ingress error: MEMFD_WRITE_FAILED\n");
        return 2;
    }

    const int requiredSeals = F_SEAL_SEAL | F_SEAL_SHRINK | F_SEAL_GROW | F_SEAL_WRITE;
    if (::fcntl(credentialFd, F_ADD_SEALS, requiredSeals) != 0 ||
        (::fcntl(credentialFd, F_GET_SEALS) & requiredSeals) != requiredSeals) {
        ::close(credentialFd);
        std::fprintf(stderr, "current secret ingress error: MEMFD_SEAL_FAILED\n");
        return 2;
    }
    struct stat descriptorStat {};
    if (::fstat(credentialFd, &descriptorStat) != 0 || !S_ISREG(descriptorStat.st_mode) ||
        descriptorStat.st_size != static_cast<off_t>(expectedSize)) {
        ::close(credentialFd);
        std::fprintf(stderr, "current secret ingress error: MEMFD_IDENTITY_FAILED\n");
        return 2;
    }

    const std::string socketPath = argv[1];
    if (socketPath.empty() || socketPath.front() != '/' || socketPath.size() >= sizeof(sockaddr_un::sun_path)) {
        ::close(credentialFd);
        std::fprintf(stderr, "current secret ingress error: BAD_SOCKET_PATH\n");
        return 2;
    }
    const int client = ::socket(AF_UNIX, SOCK_STREAM | SOCK_CLOEXEC, 0);
    if (client < 0) {
        ::close(credentialFd);
        std::fprintf(stderr, "current secret ingress error: SOCKET_CREATE_FAILED\n");
        return 2;
    }
    sockaddr_un address {};
    address.sun_family = AF_UNIX;
    std::strncpy(address.sun_path, socketPath.c_str(), sizeof(address.sun_path) - 1);
    if (::connect(client, reinterpret_cast<sockaddr*>(&address), sizeof(address)) != 0) {
        ::close(client);
        ::close(credentialFd);
        std::fprintf(stderr, "current secret ingress error: SOCKET_CONNECT_FAILED\n");
        return 2;
    }

    struct ucred peer {};
    socklen_t peerLength = sizeof(peer);
    if (::getsockopt(client, SOL_SOCKET, SO_PEERCRED, &peer, &peerLength) != 0 ||
        peerLength != sizeof(peer) || peer.uid != ::geteuid() || peer.pid != expectedPid) {
        ::close(client);
        ::close(credentialFd);
        std::fprintf(stderr, "current secret ingress error: PEER_IDENTITY_MISMATCH\n");
        return 2;
    }

    iovec payload {};
    payload.iov_base = const_cast<char*>(kCommand);
    payload.iov_len = sizeof(kCommand) - 1;
    std::array<unsigned char, CMSG_SPACE(sizeof(int))> control{};
    msghdr message {};
    message.msg_iov = &payload;
    message.msg_iovlen = 1;
    message.msg_control = control.data();
    message.msg_controllen = control.size();
    cmsghdr* cmsg = CMSG_FIRSTHDR(&message);
    cmsg->cmsg_level = SOL_SOCKET;
    cmsg->cmsg_type = SCM_RIGHTS;
    cmsg->cmsg_len = CMSG_LEN(sizeof(int));
    std::memcpy(CMSG_DATA(cmsg), &credentialFd, sizeof(credentialFd));
    if (::sendmsg(client, &message, 0) != static_cast<ssize_t>(sizeof(kCommand) - 1)) {
        ::close(client);
        ::close(credentialFd);
        std::fprintf(stderr, "current secret ingress error: SCM_RIGHTS_SEND_FAILED\n");
        return 2;
    }
    ::close(credentialFd);

    std::string response;
    std::array<char, 4096> buffer{};
    while (response.size() <= 65536) {
        const ssize_t count = ::read(client, buffer.data(), buffer.size());
        if (count < 0 && errno == EINTR) {
            continue;
        }
        if (count <= 0) {
            break;
        }
        response.append(buffer.data(), static_cast<std::size_t>(count));
        if (response.find('\n') != std::string::npos) {
            break;
        }
    }
    ::close(client);
    if (!responseIsSuccess(response)) {
        std::fprintf(stderr, "current secret ingress error: NATIVE_AUTH_RESPONSE_FAILED\n");
        return 2;
    }

    std::puts("NATIVE_AUTH_DISPATCH=PASS");
    std::puts("NATIVE_AUTH_QMETA_METHOD_ID=17");
    std::puts("SECRET_VALUES_LOGGED=false");
    return 0;
}
