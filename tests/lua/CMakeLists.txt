find_program(OTCLIENT_LUA_EXECUTABLE
    NAMES luajit luajit-2.1 lua51 lua
    HINTS
        "${VCPKG_INSTALLED_DIR}/${VCPKG_TARGET_TRIPLET}/tools/luajit"
        "${VCPKG_INSTALLED_DIR}/${VCPKG_TARGET_TRIPLET}/tools"
    REQUIRED
)

set(OTCLIENT_LUA_RUNNER ${CMAKE_CURRENT_SOURCE_DIR}/helpers/runner.lua)

add_test(
    NAME otclient_lua_unit_tests
    COMMAND ${CMAKE_COMMAND} -E env
        "OTCLIENT_SOURCE_DIR=${CMAKE_SOURCE_DIR}"
        ${OTCLIENT_LUA_EXECUTABLE}
        ${OTCLIENT_LUA_RUNNER}
        ${CMAKE_CURRENT_SOURCE_DIR}/unit/gamelib_util_test.lua
)
set_tests_properties(otclient_lua_unit_tests PROPERTIES
    LABELS "lua;unit"
    TIMEOUT 15
)

add_test(
    NAME otclient_lua_contract_tests
    COMMAND ${CMAKE_COMMAND} -E env
        "OTCLIENT_SOURCE_DIR=${CMAKE_SOURCE_DIR}"
        ${OTCLIENT_LUA_EXECUTABLE}
        ${OTCLIENT_LUA_RUNNER}
        ${CMAKE_CURRENT_SOURCE_DIR}/contracts/resource_types_test.lua
)
set_tests_properties(otclient_lua_contract_tests PROPERTIES
    LABELS "lua;unit;protocol"
    TIMEOUT 15
)

add_test(
    NAME otclient_lua_runner_failure_contract
    COMMAND ${CMAKE_COMMAND}
        -DLUA_EXECUTABLE=${OTCLIENT_LUA_EXECUTABLE}
        -DLUA_RUNNER=${OTCLIENT_LUA_RUNNER}
        -DFAILURE_FIXTURE=${CMAKE_CURRENT_SOURCE_DIR}/fixtures/intentional_failure.lua
        -P ${CMAKE_CURRENT_SOURCE_DIR}/helpers/verify_runner_failure.cmake
)
set_tests_properties(otclient_lua_runner_failure_contract PROPERTIES
    LABELS "lua;unit"
    TIMEOUT 15
)
