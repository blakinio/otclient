find_package(GTest CONFIG REQUIRED)

include(GoogleTest)

function(otclient_add_gtest TARGET_NAME)
    cmake_parse_arguments(OTCLIENT_TEST "" "" "SOURCES;LABELS" ${ARGN})

    if(OTCLIENT_TEST_SOURCES)
        set(TEST_SOURCES ${OTCLIENT_TEST_SOURCES})
    else()
        # Backwards compatibility for the existing positional call sites.
        set(TEST_SOURCES ${OTCLIENT_TEST_UNPARSED_ARGUMENTS})
    endif()

    if(NOT OTCLIENT_TEST_LABELS)
        set(OTCLIENT_TEST_LABELS unit)
    endif()

    add_executable(${TARGET_NAME} ${TEST_SOURCES})

    set_target_properties(${TARGET_NAME} PROPERTIES
        CXX_STANDARD 20
        CXX_STANDARD_REQUIRED ON
    )

    if(TOGGLE_PRE_COMPILED_HEADER)
        target_precompile_headers(${TARGET_NAME} PRIVATE ${CMAKE_SOURCE_DIR}/src/framework/pch.h)
    endif()

    target_link_libraries(${TARGET_NAME}
        PRIVATE
            otclient_core
            GTest::gtest
            GTest::gtest_main
    )

    if(ANDROID)
        target_link_libraries(${TARGET_NAME}
            PRIVATE
                log
                c
        )
    endif()

    target_compile_definitions(${TARGET_NAME}
        PRIVATE
            CLIENT
            FRAMEWORK_GRAPHICS
            FRAMEWORK_NET
            FRAMEWORK_SOUND
            FRAMEWORK_XML
    )

    if(ASAN_ENABLED)
        if(MSVC)
            target_compile_options(${TARGET_NAME} PRIVATE /fsanitize=address)
            target_link_options(${TARGET_NAME} PRIVATE /fsanitize=address)
        else()
            target_compile_options(${TARGET_NAME} PRIVATE -fsanitize=address)
            target_link_options(${TARGET_NAME} PRIVATE -fsanitize=address)
        endif()
    endif()

    if(MSVC)
        target_compile_options(${TARGET_NAME} PRIVATE /utf-8)
        if(BUILD_STATIC_LIBRARY)
            set_property(TARGET ${TARGET_NAME} PROPERTY MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>")
        else()
            set_property(TARGET ${TARGET_NAME} PROPERTY MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>DLL")
        endif()
    endif()

    gtest_discover_tests(${TARGET_NAME}
        PROPERTIES
            LABELS "${OTCLIENT_TEST_LABELS}"
            TIMEOUT 20
    )
endfunction()

add_subdirectory(map)
add_subdirectory(stdext)
add_subdirectory(otml)
add_subdirectory(unit)
add_subdirectory(integration)
add_subdirectory(lua)
