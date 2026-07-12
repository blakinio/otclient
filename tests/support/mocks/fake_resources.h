#pragma once

#include <stdexcept>
#include <string>
#include <string_view>
#include <unordered_map>

namespace otclient::test {

class FakeResources
{
public:
    void add(std::string path, std::string contents) { m_files.emplace(std::move(path), std::move(contents)); }
    [[nodiscard]] std::string_view read(const std::string& path) const
    {
        const auto it = m_files.find(path);
        if (it == m_files.end())
            throw std::out_of_range("missing fake resource: " + path);
        return it->second;
    }
    void reset() { m_files.clear(); }

private:
    std::unordered_map<std::string, std::string> m_files;
};

} // namespace otclient::test
