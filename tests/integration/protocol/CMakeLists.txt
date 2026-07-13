otclient_add_gtest(otclient_protocol_loopback_tests
    SOURCES
        loopback_packet_test.cpp
        ${CMAKE_SOURCE_DIR}/tests/support/builders/input_message_builder.cpp
    LABELS
        integration
        protocol
)

target_include_directories(otclient_protocol_loopback_tests PRIVATE ${CMAKE_SOURCE_DIR}/tests)
