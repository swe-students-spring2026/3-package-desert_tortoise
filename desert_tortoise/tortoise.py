from __future__ import annotations
from .pet import Pet
from .shelter import adopt_one, return_one


class Tortoise(Pet):
    """A concrete digital pet implementation for tortoises."""

    ASCII_ART = (
        "     ____     \n"
        " ___/ oo \\___ \n"
        "/  _      _  \\\n"
        "\\_/ \\____/ \\_/\n"
        "   /_/  \\_\\   "
    )

    ALLOWED_FOODS = {"greens", "weeds", "flowers"}
    ALLOWED_TOYS = {"foraging puzzle", "climbing obstacle", "neck scratch"}

    def __init__(self, name: str) -> None:
        super().__init__(name=name, species="tortoise")

    @classmethod
    def adopt(cls, name: str) -> "Tortoise":
        adopt_one("tortoise")
        return cls(name=name)

    def feed(self, food_type: str, amount: int = 1) -> dict[str, object]:
        if self.in_shelter:
            raise RuntimeError("This tortoise has returned to the shelter")
        if not isinstance(food_type, str):
            raise TypeError("food_type must be a string")
        if not isinstance(amount, int):
            raise TypeError("amount must be an int")
        if amount <= 0:
            raise ValueError("amount must be greater than 0")

        food = food_type.strip().lower()
        if food not in self.ALLOWED_FOODS:
            raise ValueError("food_type must be one of: greens, weeds, flowers")

        if food == "greens":
            self.hunger -= 8 * amount
            self.health += 2 * amount
        elif food == "weeds":
            self.hunger -= 10 * amount
            self.health += amount
        elif food == "flowers":
            self.hunger -= 6 * amount
            self.health += 3 * amount
            self.boredom -= amount

        self._clamp_all()
        self._check_runaway()
        return self.status()

    def play(self, type_of_toy: str) -> dict[str, object]:
        if self.in_shelter:
            raise RuntimeError("This tortoise has returned to the shelter")
        if not isinstance(type_of_toy, str):
            raise TypeError("type_of_toy must be a string")

        toy = type_of_toy.strip().lower()
        if not toy:
            raise ValueError("type_of_toy must be non-empty")
        if toy not in self.ALLOWED_TOYS:
            raise ValueError(
                "type_of_toy must be one of: foraging puzzle, climbing obstacle, neck scratch"
            )

        if toy == "foraging puzzle":
            self.boredom -= 18
            self.hunger += 4
            self.exhaustion += 3
        elif toy == "climbing obstacle":
            self.boredom -= 14
            self.hunger += 5
            self.exhaustion += 6
            self.health += 3
        elif toy == "neck scratch":
            self.boredom -= 10
            self.hunger += 2
            self.exhaustion += 1

        self._clamp_all()
        self._check_runaway()
        return self.status()

    def sleep(self, time: int = 5) -> dict[str, object]:
        if self.in_shelter:
            raise RuntimeError("This tortoise has returned to the shelter")
        if not isinstance(time, int):
            raise TypeError("time must be an int")
        if time <= 0:
            raise ValueError("time must be greater than 0")

        self.exhaustion -= 6 * time
        self.hunger += 3 * time
        self.boredom += time

        if self.hunger > 90:
            self.health -= 6

        self._clamp_all()
        self._check_runaway()
        return self.status()

    def _check_runaway(self) -> None:
        if self.health == 0 or self.hunger == 100 or self.exhaustion == 100:
            if not self.in_shelter:
                self.in_shelter = True
                return_one("tortoise", self.name)

    def _extra_status(self) -> dict[str, object]:
        return {"ascii_art": self.ASCII_ART}