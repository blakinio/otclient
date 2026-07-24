otclient_add_gtest(otclient_message_tests
    SOURCES
        inputmessage_test.cpp
        outputmessage_test.cpp
        ${CMAKE_SOURCE_DIR}/tests/support/builders/input_message_builder.cpp
    LABELS
        unit
        protocol
)

target_include_directories(otclient_message_tests PRIVATE ${CMAKE_SOURCE_DIR}/tests)

otclient_add_gtest(otclient_platform_tests
    SOURCES
        platform_open_url_test.cpp
    LABELS
        unit
        platform
)
