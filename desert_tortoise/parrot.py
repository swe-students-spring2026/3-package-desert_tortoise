from __future__ import annotations

from .pet import Pet
from .shelter import adopt_one, return_one


class Parrot(Pet):
    """A concrete digital pet implementation for parrots."""

    ASCII_ART = (
        "  __\n"
        "             /'{>\n"
        "         ____) (____\n"
        "       //';--   ;--'\\\\\n"
        "      ///////\\_/\\\\\\\\\\\n"
        "             m m"
    )
    ALLOWED_FOODS = {"seeds", "nuts", "fruits"}
    ALLOWED_TOYS = {"mirror", "bell", "ladder"}

    def __init__(self, name: str) -> None:
        super().__init__(name=name, species="parrot")

    @classmethod
    def adopt(cls, name: str) -> "Parrot":
        adopt_one("parrot")
        return cls(name=name)

    def feed(self, food_type: str, amount: int = 1) -> dict[str, object]:
        if self.in_shelter:
            raise RuntimeError("This parrot has returned to the shelter")
        if not isinstance(food_type, str):
            raise TypeError("food_type must be a string")
        if not isinstance(amount, int):
            raise TypeError("amount must be an int")
        if amount <= 0:
            raise ValueError("amount must be greater than 0")
        food = food_type.strip().lower()
        if food not in self.ALLOWED_FOODS:
            raise ValueError("food_type must be one of: seeds, nuts, fruits")

        self.hunger -= amount
        self.health += amount // 5
        self.exhaustion += amount // 12
        self._clamp_all()
        self._check_runaway()
        return self.status()

    def play(self, type_of_toy: str) -> dict[str, object]:
        if self.in_shelter:
            raise RuntimeError("This parrot has returned to the shelter")
        if not isinstance(type_of_toy, str):
            raise TypeError("type_of_toy must be a string")

        toy = type_of_toy.strip().lower()
        if not toy:
            raise ValueError("type_of_toy must be non-empty")

        toy_fun = {
            "mirror": 24,
            "bell": 18,
            "ladder": 16,
        }

        if toy not in self.ALLOWED_TOYS:
            raise ValueError(
                "type_of_toy must be one of: mirror, bell, ladder"
            )
        
        fun_boost = toy_fun[toy]

        self.boredom -= fun_boost
        self.hunger += max(4, fun_boost // 3)
        self.exhaustion += max(5, fun_boost // 2)
        if self.hunger > 85 or self.exhaustion > 85:
            self.health -= 8

        self._clamp_all()
        self._check_runaway()
        return self.status()

    def sleep(self, time: int = 5) -> dict[str, object]:
        if self.in_shelter:
            raise RuntimeError("This parrot has returned to the shelter")
        if not isinstance(time, int):
            raise TypeError("time must be an int")
        if time <= 0:
            raise ValueError("time must be greater than 0")

        self.exhaustion -= 8 * time
        self.hunger += 5 * time
        self.boredom += 2 * time
        if self.hunger > 90:
            self.health -= 10

        self._clamp_all()
        self._check_runaway()
        return self.status()

    def _check_runaway(self) -> None:
        if self.health == 0 or self.hunger == 100 or self.exhaustion == 100:
            if not self.in_shelter:
                self.in_shelter = True
                return_one("parrot", self.name)

    def _extra_status(self) -> dict[str, object]:
        return {"ascii_art": self.ASCII_ART}
