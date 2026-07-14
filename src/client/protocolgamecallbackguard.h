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

#pragma once

#include <utility>

namespace otclient::detail {

template<typename ProtocolPtr>
[[nodiscard]] bool isCurrentProtocolGame(const ProtocolPtr& sourceProtocol, const ProtocolPtr& currentProtocol)
{
    return sourceProtocol && sourceProtocol == currentProtocol;
}

template<typename ProtocolPtr, typename Callback>
[[nodiscard]] bool runIfCurrentProtocolGame(const ProtocolPtr& sourceProtocol, const ProtocolPtr& currentProtocol, Callback&& callback)
{
    if (!isCurrentProtocolGame(sourceProtocol, currentProtocol))
        return false;

    std::forward<Callback>(callback)();
    return true;
}

template<typename ProtocolPtr, typename CurrentProtocolProvider, typename Callback>
[[nodiscard]] bool runWhileCurrentProtocolGame(const ProtocolPtr& sourceProtocol, CurrentProtocolProvider&& currentProtocolProvider, Callback&& callback)
{
    if (!isCurrentProtocolGame(sourceProtocol, currentProtocolProvider()))
        return false;

    std::forward<Callback>(callback)();
    return isCurrentProtocolGame(sourceProtocol, currentProtocolProvider());
}

} // namespace otclient::detail
