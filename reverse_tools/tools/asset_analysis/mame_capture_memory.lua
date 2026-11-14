-- Capture read-only VRAM and Z80 address-space snapshots for asset correlation.
--
-- Use a fresh relative ASCII prefix in an existing output directory.
local prefix = assert(os.getenv("ASSET_CAPTURE_PREFIX"), "set ASSET_CAPTURE_PREFIX")
prefix = prefix:gsub("\\", "/")
local wait_seconds = tonumber(os.getenv("ASSET_CAPTURE_WAIT")) or 6.0

assert(prefix:match("^[%w._/%-]+$") and prefix:sub(1, 1) ~= "/" and prefix:sub(-1) ~= "/",
    "ASSET_CAPTURE_PREFIX must be a relative ASCII file prefix")
for component in prefix:gmatch("[^/]+") do
    assert(component ~= "..", "ASSET_CAPTURE_PREFIX must stay inside the working directory")
end
for _, suffix in ipairs({"_vram.bin", "_z80.bin", "_screen.png"}) do
    local existing = io.open(prefix .. suffix, "rb")
    if existing then
        existing:close()
        error("output already exists: " .. prefix .. suffix)
    end
end
assert(emu.wait(wait_seconds), "emulation stopped before memory capture")

local machine = manager.machine
local vdp = assert(machine.devices[":gen_vdp"], "missing :gen_vdp")
local vram = assert(vdp.spaces["videoram"], "missing VDP videoram space")
local z80 = assert(machine.devices[":genesis_snd_z80"], "missing Z80")
local z80_program = assert(z80.spaces["program"], "missing Z80 program space")

local function dump_space(space, start_address, length, path)
    local handle = assert(io.open(path, "wb"))
    local chunk = {}
    for offset = 0, length - 1 do
        chunk[#chunk + 1] = string.char(space:read_u8(start_address + offset))
        if #chunk == 4096 then
            handle:write(table.concat(chunk))
            chunk = {}
        end
    end
    if #chunk > 0 then
        handle:write(table.concat(chunk))
    end
    handle:close()
    print(string.format("CAPTURE path=%s start=%X length=%X", path, start_address, length))
end

dump_space(vram, 0, 0x10000, prefix .. "_vram.bin")
dump_space(z80_program, 0, 0x1E00, prefix .. "_z80.bin")

local screen = assert(machine.screens[":megadriv"], "missing screen")
local error_text = screen:snapshot(prefix .. "_screen.png")
assert(not error_text, "snapshot failed: " .. tostring(error_text))
print(string.format("CAPTURE path=%s frame=%d", prefix .. "_screen.png", screen:frame_number()))

machine:exit()
