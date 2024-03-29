from __future__ import annotations

from typing import Tuple

import numpy as np  # type: ignore
import color

# Tile graphics structured type compatible with Console.tiles_rgb.
graphic_dt = np.dtype(
    [
        ('ch', np.int32),  # Unicode codepoint.
        ('fg', '3B'),  # 3 unsigned bytes, for RGB colors.
        ('bg', '3B'),
    ]
)

# Tile struct used for statically defined tile data.
tile_dt = np.dtype(
    [
        ('weight', int),
        ('walkable', np.bool_),  # True if this tile can be walked over.
        ('transparent', np.bool_),   # True if this tile doesn't block FOV.
        ('dark', graphic_dt),   # Graphics for when this tile is not in FOV.
        ('light', graphic_dt),   # Graphics for when this tile is in FOV.
    ]
)

def new_tile(
    *,  # Enforce the use of keywords, so that parameter order doesn't matter.
    weight: int,
    walkable: int,
    transparent: int,
    dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
    light: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
) -> np.ndarray:
    '''Helper function for defining individual tile types '''
    return np.array((weight, walkable, transparent, dark, light), dtype = tile_dt)

# unexplored, unseen tiles
SHROUD = np.array((ord(' '), (color.white), (color.black)), dtype = graphic_dt)

placeholder = new_tile(
    weight = -100,
    walkable = True,
    transparent = True,
    dark = (ord(' '), (color.white), (color.white)),
    light = (ord(' '), (color.white), (color.white)),
)
placeholder1 = new_tile(
    weight = -100,
    walkable = True,
    transparent = True,
    dark = (ord(' '), (color.anb_red), (color.anb_red)),
    light = (ord(' '), (color.anb_red), (color.anb_red)),
)

floor = new_tile(
    weight = 1,
    walkable = True,
    transparent = True,
    dark = (ord(' '), (color.light_grey), (color.dark_grey)),
    light = (ord(' '), (color.white), (color.grey)),
)
wall = new_tile(
    weight = 0,
    walkable = False,
    transparent = False,
    dark = (ord('#'), (color.light_grey), (color.dark_grey)),
    light = (ord('#'), (color.white), (color.grey)),
)
down_stairs = new_tile(
    weight = 2,
    walkable = True,
    transparent = True,
    dark = (ord('>'), (color.light_grey), (color.dark_grey)),
    light = (ord('>'), (color.white), (color.grey))
)
up_stairs = new_tile(
    weight = 2,
    walkable = True,
    transparent = True,
    dark = (ord('<'), (color.light_grey), (color.dark_grey)),
    light = (ord('<'), (color.white), (color.grey))
)

loose_grass = new_tile(
    weight = 1,
    walkable = True,
    transparent = True,
    dark = (ord('░'), (color.light_grey), (color.dark_grey)),
    light = (ord('░'), (color.anb_light_green), (color.grey))
)
grass = new_tile(
    weight = 2,
    walkable = True,
    transparent = True,
    dark = (ord('▒'), (color.light_grey), (color.dark_grey)),
    light = (ord('▒'), (color.anb_green), (color.grey))
)
dense_grass = new_tile(
    weight = 3,
    walkable = True,
    transparent = True,
    dark = (ord('▓'), (color.light_grey), (color.dark_grey)),
    light = (ord('▓'), (color.anb_green), (color.grey))
)

loose_rubble = new_tile(
    weight = 1,
    walkable = True,
    transparent = True,
    dark = (ord('░'), (color.light_grey), (color.dark_grey)),
    light = (ord('░'), (color.light_grey), (color.grey))
)
rubble = new_tile(
    weight = 2,
    walkable = True,
    transparent = True,
    dark = (ord('▒'), (color.light_grey), (color.dark_grey)),
    light = (ord('▒'), (color.grey), (color.grey))
)

stalagmite = new_tile(
    weight = 0,
    walkable = False,
    transparent = False,
    dark = (ord('▼'), (color.light_grey), (color.dark_grey)),
    light = (ord('▼'), (color.light_grey), (color.grey))
)
stalactite = new_tile(
    weight = 0,
    walkable = False,
    transparent = False,
    dark = (ord('▲'), (color.light_grey), (color.dark_grey)),
    light = (ord('▲'), (color.light_grey), (color.grey))
)

shallow_water = new_tile(
    weight = 0,
    walkable = True,
    transparent = True,
    dark = (ord('~'), (color.light_grey), (color.dark_grey)),
    light = (ord('~'), (color.anb_blue), (color.grey))
)
deep_water = new_tile(
    weight = 5,
    walkable = True,
    transparent = True,
    dark = (ord('~'), (color.light_grey), (color.dark_grey)),
    light = (ord('~'), (color.anb_deep_blue), (color.grey))
)