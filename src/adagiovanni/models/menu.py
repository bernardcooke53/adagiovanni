from enum import Enum


class Sandwich(str, Enum):
    def __format__(self, __format_spec: str) -> str:
        return str.__format__(self, __format_spec)

    HamAndCheese = "Ham and Cheese"
    BLT = "BLT"
    ChickenAndBacon = "Chicken and Bacon"
    Clubhouse = "Clubhouse"
    EggMayonnaise = "Egg Mayonnaise"


# class Sandwich(IdModelMixin, BaseModel):
#     name: str
#     friendly_name: str
#     description: Optional[str] = None
#
#
# class Menu(BaseModel):
#     sandwiches: List[Sandwich]
