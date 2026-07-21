/*
 * Copyright (c) 2010-2026 OTClient <https://github.com/edubart/otclient>
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */
#ifndef __EMSCRIPTEN__

#include "connection.h"
#include "server.h"

#include <istream>
#include <limits>
#include <memory>
#include <sstream>
#include <string>

extern asio::io_service g_ioService;

namespace {
constexpr std::size_t MAX_LOOPBACK_HTTP_HEADERS = 8192;

std::string makeLoopbackHttpResponse(const bool ok)
{
    const std::string body = ok
        ? "<!doctype html><html><body>Authentication response received. You can return to OTClient.</body></html>"
        : "<!doctype html><html><body>Invalid authentication response. You can return to OTClient.</body></html>";
    std::ostringstream response;
    response << (ok ? "HTTP/1.1 200 OK\r\n" : "HTTP/1.1 400 Bad Request\r\n")
             << "Content-Type: text/html; charset=utf-8\r\n"
             << "Cache-Control: no-store\r\n"
             << "Pragma: no-cache\r\n"
             << "Connection: close\r\n"
             << "Content-Length: " << body.size() << "\r\n\r\n"
             << body;
    return response.str();
}
}

Server::Server(const int port, const bool loopbackHttp)
    : m_loopbackHttp(loopbackHttp)
    , m_acceptor(g_ioService,
                 asio::ip::tcp::endpoint(loopbackHttp ? asio::ip::address_v4::loopback() : asio::ip::address_v4::any(),
                                         static_cast<unsigned short>(port)))
{
}

ServerPtr Server::create(const int port)
{
    try {
        const bool loopbackHttp = port < 0;
        const long long requestedPort = loopbackHttp ? -static_cast<long long>(port) : static_cast<long long>(port);
        if (requestedPort < 0 || requestedPort > std::numeric_limits<unsigned short>::max()) {
            g_logger.error("Failed to initialize server: invalid port");
            return nullptr;
        }
        return std::make_shared<Server>(static_cast<int>(requestedPort), loopbackHttp);
    } catch (const std::exception& e) {
        g_logger.error("Failed to initialize server: {}", e.what());
        return nullptr;
    }
}

void Server::close()
{
    if (!m_isOpen)
        return;

    m_isOpen = false;
    m_acceptPending = false;
    std::error_code ignored;
    m_acceptor.cancel(ignored);
    m_acceptor.close(ignored);
}

void Server::acceptNext()
{
    if (!m_isOpen || m_acceptPending)
        return;

    m_acceptPending = true;

    if (!m_loopbackHttp) {
        const auto& connection = std::make_shared<Connection>();
        connection->m_connecting = true;

        const auto self = static_self_cast<Server>();
        m_acceptor.async_accept(connection->m_socket, [self, connection](const std::error_code& error) {
            self->m_acceptPending = false;
            if (!error) {
                connection->m_connected = true;
                connection->m_connecting = false;
            }
            self->callLuaField("onAccept", connection, error.message(), error.value());
        });
        return;
    }

    const auto socket = std::make_shared<asio::ip::tcp::socket>(g_ioService);
    const auto self = static_self_cast<Server>();
    m_acceptor.async_accept(*socket, [self, socket](const std::error_code& acceptError) {
        if (acceptError) {
            self->m_acceptPending = false;
            if (self->m_isOpen)
                self->callLuaField("onHttpRequest", std::string(), acceptError.message(), acceptError.value());
            return;
        }

        std::error_code endpointError;
        const auto remote = socket->remote_endpoint(endpointError);
        if (endpointError || !remote.address().is_loopback()) {
            self->m_acceptPending = false;
            self->callLuaField("onHttpRequest", std::string(), std::string("non_loopback_peer"), 403);
            return;
        }

        const auto buffer = std::make_shared<asio::streambuf>(MAX_LOOPBACK_HTTP_HEADERS);
        asio::async_read_until(*socket, *buffer, "\r\n\r\n",
            [self, socket, buffer](const std::error_code& readError, std::size_t) {
                std::string target;
                std::string callbackError;
                int callbackCode = 0;

                if (readError) {
                    callbackError = readError == asio::error::not_found ? "request_headers_too_large" : readError.message();
                    callbackCode = readError.value();
                } else {
                    std::istream request(buffer.get());
                    std::string requestLine;
                    std::getline(request, requestLine);
                    if (!requestLine.empty() && requestLine.back() == '\r')
                        requestLine.pop_back();

                    std::istringstream parser(requestLine);
                    std::string method;
                    std::string version;
                    parser >> method >> target >> version;
                    if (method != "GET" || target.empty() || target.front() != '/' ||
                        version.rfind("HTTP/", 0) != 0 || target.find('#') != std::string::npos) {
                        target.clear();
                        callbackError = "invalid_request";
                        callbackCode = 400;
                    }
                }

                const auto response = std::make_shared<std::string>(makeLoopbackHttpResponse(callbackError.empty()));
                asio::async_write(*socket, asio::buffer(*response),
                    [self, socket, response, target, callbackError, callbackCode](const std::error_code&, std::size_t) {
                        std::error_code ignored;
                        socket->shutdown(asio::ip::tcp::socket::shutdown_both, ignored);
                        socket->close(ignored);
                        self->m_acceptPending = false;
                        if (self->m_isOpen)
                            self->callLuaField("onHttpRequest", target, callbackError, callbackCode);
                    });
            });
    });
}

#endif
