from __future__ import annotations

import typing as t
import dataclasses


@dataclasses.dataclass
class Item:
    add_on_deal_id: int
    brand: str
    flash_sale: bool
    item_id: int
    liked_count: int
    models: t.List[Model]
    name: str
    price: int
    shop_location: str
    shop_id: int
    stock: int
    upcoming_flash_sale: UpcomingFlashSale
    view_count: int

    @dataclasses.dataclass
    class Model:
        item_id: int
        model_id: int
        name: str
        price: int
        stock: int

    @dataclasses.dataclass
    class UpcomingFlashSale:
        end_time: int
        start_time: int
        stock: int
