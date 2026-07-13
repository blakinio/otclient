execute_process(
    COMMAND "${LUA_EXECUTABLE}" "${LUA_RUNNER}" "${FAILURE_FIXTURE}"
    RESULT_VARIABLE runner_result
    OUTPUT_VARIABLE runner_output
    ERROR_VARIABLE runner_error
)

if(runner_result EQUAL 0)
    message(FATAL_ERROR "Lua runner returned success for an intentional assertion failure:\n${runner_output}\n${runner_error}")
endif()

if(NOT runner_error MATCHES "intentional runner self-test")
    message(FATAL_ERROR "Lua runner failed without reporting the expected test name:\n${runner_output}\n${runner_error}")
endif()
