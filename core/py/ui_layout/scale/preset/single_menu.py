from dataclasses import dataclass

from py.hmi.single_menu.variable import SingleMenuVar
from py.variable import Size


@dataclass
class ScaleSingleMenu:
    block_size: Size = Size(128, 128)
    main_size: Size = Size(
        block_size.width * (SingleMenuVar.WIDTH_BLOCK * 2 - 1),
        block_size.height * (SingleMenuVar.HEIGHT_BLOCK * 2 - 1)
    )
    number_size: Size = Size(60, 60)
    gap: int = block_size.width * 2
