local suites = {}
local failures = 0

function assertEqual(expected, actual, message)
  if expected ~= actual then
    error(message or string.format("expected %s, got %s", tostring(expected), tostring(actual)), 2)
  end
end

function assertTrue(value, message)
  if value ~= true then error(message or "expected true", 2) end
end

function assertFalse(value, message)
  if value ~= false then error(message or "expected false", 2) end
end

function assertNil(value, message)
  if value ~= nil then error(message or "expected nil", 2) end
end

function test(name, callback)
  if type(name) ~= "string" or name == "" then error("test name must be non-empty", 2) end
  if type(callback) ~= "function" then error("test callback must be a function", 2) end
  table.insert(suites, { name = name, callback = callback })
end

for index = 1, #arg do
  local ok, errorMessage = pcall(dofile, arg[index])
  if not ok then
    io.stderr:write(string.format("[LOAD FAILED] %s: %s\n", arg[index], errorMessage))
    os.exit(1)
  end
end

for _, suite in ipairs(suites) do
  local ok, errorMessage = xpcall(suite.callback, debug.traceback)
  if ok then
    io.stdout:write(string.format("[PASS] %s\n", suite.name))
  else
    failures = failures + 1
    io.stderr:write(string.format("[FAIL] %s\n%s\n", suite.name, errorMessage))
  end
end

io.stdout:write(string.format("Lua tests: %d total, %d failed\n", #suites, failures))
if failures > 0 then os.exit(1) end
