otclient_add_gtest(otclient_test_support_tests
    SOURCES
        test_support_test.cpp
        ${CMAKE_SOURCE_DIR}/tests/support/test_environment/test_environment.cpp
    LABELS
        unit
)

target_include_directories(otclient_test_support_tests PRIVATE ${CMAKE_SOURCE_DIR}/tests)
