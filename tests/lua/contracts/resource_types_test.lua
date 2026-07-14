local root = assert(os.getenv("OTCLIENT_SOURCE_DIR"), "OTCLIENT_SOURCE_DIR is required")
dofile(root .. "/modules/gamelib/const.lua")

test("ResourceTypes values are unique", function()
  local owners = {}
  for name, value in pairs(ResourceTypes) do
    assertNil(owners[value], string.format("%s and %s both use %d", owners[value] or "", name, value))
    owners[value] = name
  end
end)

test("ResourceTypes bank balance is the only zero identifier", function()
  assertEqual(0, ResourceTypes.BANK_BALANCE)
  for name, value in pairs(ResourceTypes) do
    if name ~= "BANK_BALANCE" then assertFalse(value == 0, name .. " aliases BANK_BALANCE") end
  end
end)

test("ResourceTypes fragment contract uses singular identifiers 84 and 85", function()
  assertEqual(84, ResourceTypes.LESSER_FRAGMENT)
  assertEqual(85, ResourceTypes.GREATER_FRAGMENT)
  assertNil(ResourceTypes.LESSER_FRAGMENTS)
  assertNil(ResourceTypes.GREATER_FRAGMENTS)
end)
