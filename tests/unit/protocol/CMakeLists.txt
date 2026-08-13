otclient_add_gtest(otclient_protocol_contract_tests
    SOURCES
        game_login_version_string_test.cpp
        protocol_game_lifecycle_test.cpp
        resource_contract_test.cpp
    LABELS
        unit
        protocol
)

target_compile_definitions(otclient_protocol_contract_tests PRIVATE
    OTCLIENT_SOURCE_DIR="${CMAKE_SOURCE_DIR}"
)
