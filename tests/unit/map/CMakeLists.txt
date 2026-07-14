otclient_add_gtest(otclient_tile_order_tests
    SOURCES
        tile_order_test.cpp
        ${CMAKE_SOURCE_DIR}/tests/support/builders/thing_builders.cpp
        ${CMAKE_SOURCE_DIR}/tests/support/test_environment/test_environment.cpp
    LABELS
        unit
)

target_include_directories(otclient_tile_order_tests PRIVATE ${CMAKE_SOURCE_DIR}/tests)
set_target_properties(otclient_tile_order_tests PROPERTIES DISABLE_PRECOMPILE_HEADERS ON)
