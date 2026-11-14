"""Read-only Mode-5 tile, window and sprite composition from live VDP memory.

This is a display layer, not a VDP clock or CPU interpreter. A caller supplies
the live buffers from hardware_vdp and must not modify them during a render.
No cartridge image, reference capture, implicit font or placeholder screen is
used. Font writers and image loaders both produce the same 4-bpp VRAM tiles.
"""
from dataclasses import dataclass

from ..graphics_vdp.graphics_assets import cram_colours, tile_pixels
from ..high_level_scene_flows.domain import Boundary
from .hardware_vdp import VdpMemory


RENDER_LIMITATIONS = (
    'No raster timing, horizontal counter, interrupts or status side effects.',
    'No per-scanline sprite/pixel limits or sprite collision status.',
    'No internal SAT cache; direct static table composition does not model sprite-base cache behavior.',
    'No Mode 4, interlace, shadow/highlight or 128-KiB VRAM mode.',
    'Fine horizontal scroll with two-cell vertical scroll needs an explicit hardware edge model.',
    'Visible X-zero sprite masking needs raster sprite evaluation.',
)


@dataclass(frozen=True)
class LayerPixels:
    """An indexed layer; low color nibble zero is transparent, even in palette 3.

    Priorities are one byte per pixel, with values zero or one. Plane A is
    absent where the window replaces it; a transparent window does not reveal A.
    """

    width: int
    height: int
    palette_indices: bytes
    priorities: bytes
    kind: str

    def __post_init__(self):
        size = self.width * self.height
        if self.width not in (256, 320) or self.height not in (224, 240):
            raise ValueError('one supported Mode-5 visible rectangle required')
        if type(self.palette_indices) is not bytes or len(self.palette_indices) != size:
            raise ValueError('one indexed byte per layer pixel required')
        if type(self.priorities) is not bytes or len(self.priorities) != size:
            raise ValueError('one priority byte per layer pixel required')
        if any(value > 63 for value in self.palette_indices):
            raise ValueError('layer palette index must be in 0..63')
        if any(value > 1 for value in self.priorities):
            raise ValueError('layer priority must be zero or one')
        if self.kind not in ('A', 'B', 'window', 'sprites'):
            raise ValueError('an explicit background, window or sprite layer required')


@dataclass(frozen=True)
class RenderedFrame:
    """Opaque host RGBA plus exact indexed pixels; not a CRT color calibration.

    RGB uses the project's existing cram_colours preview profile. Keeping the
    indices separately permits a host to choose a different analog color model.
    """

    width: int
    height: int
    rgba: bytes
    palette_indices: bytes
    colour_profile: str = 'project_cram_colours'
    limitations: tuple[str, ...] = RENDER_LIMITATIONS

    def __post_init__(self):
        size = self.width * self.height
        if type(self.rgba) is not bytes or len(self.rgba) != size * 4:
            raise ValueError('one complete RGBA rectangle required')
        if type(self.palette_indices) is not bytes or len(self.palette_indices) != size:
            raise ValueError('one complete indexed rectangle required')


class _Display:
    """One synchronous render session; tile caches never outlive live memory reads."""

    def __init__(self, memory: VdpMemory):
        if type(memory) is not VdpMemory:
            raise ValueError('the shared VdpMemory instance required')
        for name, size in (('vram', 65536), ('cram', 128),
                           ('vsram', 80), ('registers', 32)):
            backing = getattr(memory, name)
            if type(backing) is not bytearray or len(backing) != size:
                raise ValueError('complete live ' + name + ' backing required')
        self.memory = memory
        self.registers = memory.registers
        if not self.registers[1] & 0x04:
            raise Boundary('Mode-4 display composition is not implemented')
        if self.registers[1] & 0x80:
            raise Boundary('128-KiB VRAM display composition is not implemented')
        if self.registers[12] & 0x06:
            raise Boundary('interlace or reserved interlace display selection is not implemented')
        if self.registers[12] & 0x08:
            raise Boundary('shadow/highlight display composition is not implemented')
        self.width = 320 if self.registers[12] & 1 else 256
        self.height = 240 if self.registers[1] & 8 else 224
        self.enabled = bool(self.registers[1] & 0x40)
        self.size = self.width * self.height
        self.tiles: dict[int, tuple[int, ...]] = {}
        self.hscroll: dict[tuple[int, int], int] = {}
        self.scroll_mode = self.registers[11] & 3
        self.column_scroll = bool(self.registers[11] & 4)
        dimensions = {0: 32, 1: 64, 3: 128}
        horizontal = self.registers[16] & 3
        vertical = (self.registers[16] >> 4) & 3
        if horizontal not in dimensions or vertical not in dimensions:
            raise Boundary('prohibited Mode-5 plane dimension selection')
        self.plane_width = dimensions[horizontal]
        self.plane_height = dimensions[vertical]
        if self.plane_width * self.plane_height > 4096:
            raise Boundary('plane name table exceeds the supported 8192-byte geometry')
        if self.scroll_mode == 1:
            raise Boundary('reserved horizontal scroll mode has no display algorithm')
        self.plane_bases = ((self.registers[2] & 0x38) << 10,
                            (self.registers[4] & 7) << 13)
        self.window_width = 64 if self.width == 320 else 32
        self.window_base = (self.registers[3] & (0x3C if self.width == 320 else 0x3E)) << 10
        self.window_x = (self.registers[17] & 31) * 16
        self.window_y = (self.registers[18] & 31) * 8
        self.window_right = bool(self.registers[17] & 0x80)
        self.window_bottom = bool(self.registers[18] & 0x80)
        for offset in range(0, 128, 2):
            if VdpMemory.word(memory.cram, offset) & ~0x0EEE:
                raise ValueError('live CRAM contains non-color bus bits')
        for offset in range(0, 80, 2):
            if VdpMemory.word(memory.vsram, offset) & ~0x07FF:
                raise ValueError('live VSRAM contains reserved bits')

    def word(self, address: int) -> int:
        vram = self.memory.vram
        return (vram[address & 0xFFFF] << 8) | vram[(address + 1) & 0xFFFF]

    def tile(self, index: int) -> tuple[int, ...]:
        index &= 0x7FF
        if index not in self.tiles:
            # All 2048 complete 32-byte tiles exist in the validated backing.
            # Thus the legacy extractor's missing-tile branch is never entered.
            pixels = tile_pixels(self.memory.vram, index)
            if len(pixels) != 64 or any(value < 0 or value > 15 for value in pixels):
                raise ValueError('the shared codec must decode one complete 4-bpp tile')
            self.tiles[index] = tuple(pixels)
        return self.tiles[index]

    def tile_pixel(self, attributes: int, x: int, y: int) -> tuple[int, int]:
        if attributes & 0x0800:
            x = 7 - x
        if attributes & 0x1000:
            y = 7 - y
        colour = self.tile(attributes & 0x7FF)[y * 8 + x]
        return (((attributes >> 13) & 3) * 16 + colour,
                1 if attributes & 0x8000 else 0)

    def horizontal_scroll(self, plane: int, y: int) -> int:
        key = (plane, y)
        if key not in self.hscroll:
            row = 0 if self.scroll_mode == 0 else (y & ~7 if self.scroll_mode == 2 else y)
            base = (self.registers[13] & 0x3F) << 10
            self.hscroll[key] = self.word(base + row * 4 + plane * 2) & 0x03FF
        return self.hscroll[key]

    def vertical_scroll(self, plane: int, x: int, hscroll: int) -> int:
        if self.column_scroll:
            if hscroll & 15:
                # The partial left column differs between hardware revisions.
                # Do not pick an unprovided MD1/MD2 raster model silently.
                raise Boundary('fine H-scroll with column V-scroll requires an explicit hardware edge model')
            column = x // 16
            offset = column * 4 + plane * 2
        else:
            offset = plane * 2
        return VdpMemory.word(self.memory.vsram, offset) & 0x07FF

    def vertical_window_row(self, y: int) -> bool:
        return y >= self.window_y if self.window_bottom else y < self.window_y

    def window_at(self, x: int, y: int) -> bool:
        horizontal = x >= self.window_x if self.window_right else x < self.window_x
        return horizontal or self.vertical_window_row(y)

    def plane_pixel(self, plane: int, x: int, y: int) -> tuple[int, int]:
        scroll = self.horizontal_scroll(plane, y)
        source_x = x - scroll
        if (plane == 0 and not self.window_right and 0 < self.window_x < self.width
                and not self.vertical_window_row(y) and scroll & 15
                and self.window_x <= x < self.window_x + (scroll & 15)):
            # Preserve the VDP's partial column fetch at a left-window boundary;
            # it fetches the current pair, not the preceding pair used elsewhere.
            source_x += 16
        source_x %= self.plane_width * 8
        source_y = (y + self.vertical_scroll(plane, x, scroll)) % (self.plane_height * 8)
        cell = (source_y // 8) * self.plane_width + source_x // 8
        return self.tile_pixel(self.word(self.plane_bases[plane] + cell * 2),
                               source_x & 7, source_y & 7)

    def window_pixel(self, x: int, y: int) -> tuple[int, int]:
        cell = (y // 8) * self.window_width + x // 8
        return self.tile_pixel(self.word(self.window_base + cell * 2), x & 7, y & 7)

    def background_layers(self) -> dict[str, LayerPixels]:
        colours = {kind: bytearray(self.size) for kind in ('A', 'B', 'window')}
        priorities = {kind: bytearray(self.size) for kind in colours}
        if self.enabled:
            for y in range(self.height):
                for x in range(self.width):
                    offset = y * self.width + x
                    colour, priority = self.plane_pixel(1, x, y)
                    colours['B'][offset] = colour
                    priorities['B'][offset] = priority
                    kind = 'window' if self.window_at(x, y) else 'A'
                    colour, priority = (self.window_pixel(x, y) if kind == 'window'
                                        else self.plane_pixel(0, x, y))
                    colours[kind][offset] = colour
                    priorities[kind][offset] = priority
        return {kind: LayerPixels(self.width, self.height, bytes(colours[kind]),
                                   bytes(priorities[kind]), kind) for kind in colours}

    def sprite_layer(self) -> LayerPixels:
        colours = bytearray(self.size)
        priorities = bytearray(self.size)
        if not self.enabled:
            return LayerPixels(self.width, self.height, bytes(colours), bytes(priorities), 'sprites')
        capacity = 80 if self.width == 320 else 64
        base = (self.registers[5] & (0x7E if self.width == 320 else 0x7F)) << 9
        visited: set[int] = set()
        index = 0
        while True:
            if index >= capacity:
                raise Boundary('sprite link is outside the active Mode-5 sprite table')
            if index in visited:
                raise Boundary('cyclic sprite links require raster evaluation')
            visited.add(index)
            address = base + index * 8
            y = (self.word(address) & 0x01FF) - 128
            size_link = self.word(address + 2)
            attributes = self.word(address + 4)
            raw_x = self.word(address + 6) & 0x01FF
            x = raw_x - 128
            width_cells = ((size_link >> 10) & 3) + 1
            height_cells = ((size_link >> 8) & 3) + 1
            width, height = width_cells * 8, height_cells * 8
            if raw_x == 0 and y < self.height and y + height > 0:
                raise Boundary('visible X-zero sprite masking requires raster sprite evaluation')
            left, right = max(0, x), min(self.width, x + width)
            top, bottom = max(0, y), min(self.height, y + height)
            palette = ((attributes >> 13) & 3) * 16
            priority = 1 if attributes & 0x8000 else 0
            pattern = attributes & 0x07FF
            for screen_y in range(top, bottom):
                local_y = screen_y - y
                if attributes & 0x1000:
                    local_y = height - 1 - local_y
                for screen_x in range(left, right):
                    offset = screen_y * self.width + screen_x
                    if colours[offset] & 15:
                        continue
                    local_x = screen_x - x
                    if attributes & 0x0800:
                        local_x = width - 1 - local_x
                    # Sprite tiles run down each column before the next column.
                    tile_index = pattern + (local_x // 8) * height_cells + local_y // 8
                    colour = self.tile(tile_index)[(local_y & 7) * 8 + (local_x & 7)]
                    if colour:
                        colours[offset] = palette + colour
                        priorities[offset] = priority
            index = size_link & 0x7F
            if index == 0:
                break
        return LayerPixels(self.width, self.height, bytes(colours), bytes(priorities), 'sprites')

    def layers(self) -> dict[str, LayerPixels]:
        layers = self.background_layers()
        layers['sprites'] = self.sprite_layer()
        return layers

    def compose(self, layers: dict[str, LayerPixels]) -> RenderedFrame:
        if type(layers) is not dict or set(layers) != {'A', 'B', 'window', 'sprites'}:
            raise ValueError('the complete A/B/window/sprite layer set required')
        for kind, layer in layers.items():
            if (type(layer) is not LayerPixels or layer.kind != kind
                    or layer.width != self.width or layer.height != self.height):
                raise ValueError('layers must share one visible Mode-5 rectangle')
        backdrop = self.registers[7] & 63
        pixels = bytearray([backdrop]) * self.size
        if self.enabled:
            ranks = bytearray(self.size)
            for kind, low_rank, high_rank in (('B', 1, 4), ('A', 2, 5),
                                              ('window', 2, 5), ('sprites', 3, 6)):
                layer = layers[kind]
                for offset, colour in enumerate(layer.palette_indices):
                    if colour & 15:
                        rank = high_rank if layer.priorities[offset] else low_rank
                        if rank > ranks[offset]:
                            pixels[offset] = colour
                            ranks[offset] = rank
            if self.registers[0] & 0x20:
                for y in range(self.height):
                    start = y * self.width
                    pixels[start:start + 8] = bytes([backdrop]) * 8
        palette = cram_colours(bytes(self.memory.cram))
        rgba = bytearray(self.size * 4)
        for offset, colour in enumerate(pixels):
            red, green, blue = palette[colour]
            start = offset * 4
            rgba[start:start + 4] = bytes((red, green, blue, 255))
        return RenderedFrame(self.width, self.height, bytes(rgba), bytes(pixels))


def render_layers(memory: VdpMemory) -> dict[str, LayerPixels]:
    """Decode live memory into separate complete layers without hardware writes."""
    return _Display(memory).layers()


def compose_frame(memory: VdpMemory, layers: dict[str, LayerPixels]) -> RenderedFrame:
    """Combine supplied layers using current display registers and CRAM colors.

    The caller is responsible for keeping those layers and live memories from
    the same paused display state. This function does not claim a raster capture.
    """
    return _Display(memory).compose(layers)


def render_frame(memory: VdpMemory) -> RenderedFrame:
    """Decode and combine one caller-controlled, static live Mode-5 display state."""
    display = _Display(memory)
    return display.compose(display.layers())
