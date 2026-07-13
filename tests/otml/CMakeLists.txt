otclient_add_gtest(otml_tests
    otml_alias_test.cpp
    otml_fixture_test.cpp
)

target_compile_definitions(otml_tests PRIVATE OTCLIENT_SOURCE_DIR="${CMAKE_SOURCE_DIR}")
