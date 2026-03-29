"""Concrete dog pet implementation."""

from __future__ import annotations

from .pet import Pet
from .shelter import adopt_one, return_one


class Dog(Pet):
    """A concrete digital pet implementation for dogs."""

    ASCII_ART = (
        "     _=,_\n"
        "  o_/6 /#\\\n"
        "  \\__ |##/\n"
        "   ='|--\\\n"
        "    /   #'-.\n"
        "    \\#|_   _'-. /\n"
        "      |/ \\_( # |'\n" 
        "     C/ ,--___/\n"

    )
    ALLOWED_FOODS = {"meat", "peanut butter", "fruits"}
    ALLOWED_TOYS = {"bone", "stick", "ball"}

    def __init__(self, name: str) -> None:
        super().__init__(name=name, species="dog")

    @classmethod
    def adopt(cls, name: str) -> "Dog":
        adopt_one("dog")
        return cls(name=name)

    def feed(self, food_type: str, amount: int = 1) -> dict[str, object]:
        if self.in_shelter:
            raise RuntimeError("This dog has returned to the shelter")
        if not isinstance(food_type, str):
            raise TypeError("food_type must be a string")
        if not isinstance(amount, int):
            raise TypeError("amount must be an int")
        if amount <= 0:
            raise ValueError("amount must be greater than 0")
        food = food_type.strip().lower()
        if food not in self.ALLOWED_FOODS:
            raise ValueError("food_type must be one of: meat, peanut butter, fruits")

        if food == "meat":
            self.hunger -= 10 * amount
            self.health += 2 * amount
        elif food == "peanut butter":
            self.hunger -= 2 * amount
            self.health += amount
            self.boredom -= amount
        elif food == "fruits":
            self.hunger -= 5 * amount
            self.health += 3 * amount
            

        self._clamp_all()
        self._check_runaway()
        return self.status()

    def play(self, type_of_toy: str) -> dict[str, object]:
        if self.in_shelter:
            raise RuntimeError("This dog has returned to the shelter")
        if not isinstance(type_of_toy, str):
            raise TypeError("type_of_toy must be a string")

        toy = type_of_toy.strip().lower()
        if not toy:
            raise ValueError("type_of_toy must be non-empty")

        if toy not in self.ALLOWED_TOYS:
            raise ValueError(
                "type_of_toy must be one of: bone, stick, ball"
            )

        toy_fun = {
            "bone": {"boredom": -10, "exhaustion": 5, "hunger": 3},
            "stick": {"boredom": -25, "exhaustion": 13, "hunger": 8},
            "ball": {"boredom": -18, "exhaustion": 20, "hunger": 13},
        }
        
        fun_boost = toy_fun[toy]

        self.boredom += fun_boost["boredom"]
        self.exhaustion += max(5, fun_boost["exhaustion"])
        self.hunger += max(4, fun_boost["hunger"])
        if self.hunger > 85 or self.exhaustion > 85:
            self.health -= 8

        self._clamp_all()
        self._check_runaway()
        return self.status()

    def sleep(self, time: int = 5) -> dict[str, object]:
        if self.in_shelter:
            raise RuntimeError("This dog has returned to the shelter")
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
        if self.health == 0 or self.boredom == 0 or self.exhaustion == 0:
            if not self.in_shelter:
                self.in_shelter = True
                return_one("dog", self.name)

    def _extra_status(self) -> dict[str, object]:
        return {"ascii_art": self.ASCII_ART}
