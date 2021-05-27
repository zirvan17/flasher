import typing as t
import dataclasses


@dataclasses.dataclass
class CartItem:
    add_on_deal_id: int
    group_id: t.Union[int, str]  # if value is 0 then it's int, else it's a string
    itemid: int
    modelid: int
    price: int
    shopid: int
