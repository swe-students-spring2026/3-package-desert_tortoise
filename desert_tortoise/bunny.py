"""Concrete bunny pet implementation."""

from __future__ import annotations

from .pet import Pet
from .shelter import adopt_one, return_one


class Bunny(Pet):
    """A concrete digital pet implementation for bunnies."""

    ASCII_ART = ("""
                 ,
            /|      __
           / |   ,-~ /
          Y :|  //  /
          | jj /( .^
          >-"~"-v"
         /       Y
        jo  o    |
       ( ~T~     j
        >._-' _./
       /   "~"  |
      Y     _,  |
     /| ;-"~ _  l
    / l/ ,-"~    \
    \//\/      .- \
     Y        /    Y    
     l       I     !
     ]\      _\    /"\
    (" ~----( ~   Y.  )
~~~~~~~~~~~~~~~~~~~~~~~~~
    """)

    ALLOWED_FOODS = {"hay", "carrots", "lettuce"}
    ALLOWED_TOYS = {"tunnel", "ball", "cardboard"}

    def __init__(self, name: str) -> None:
        super().__init__(name=name, species="bunny")

    @classmethod
    def adopt(cls, name: str) -> "Bunny":
        adopt_one("bunny")
        return cls(name=name)

    def feed(self, food_type: str, amount: int = 1) -> dict[str, object]:
        if self.in_shelter:
            raise RuntimeError("This bunny has returned to the shelter")
        if not isinstance(food_type, str):
            raise TypeError("food_type must be a string")
        if not isinstance(amount, int):
            raise TypeError("amount must be an int")
        if amount <= 0:
            raise ValueError("amount must be greater than 0")

        food = food_type.strip().lower()
        if food not in self.ALLOWED_FOODS:
            raise ValueError("food_type must be one of: hay, carrots, lettuce")

        self.hunger -= amount
        self.health += amount // 4
        self.exhaustion += amount // 10
        self._clamp_all()
        self._check_runaway()
        return self.status()

    def play(self, type_of_toy: str) -> dict[str, object]:
        if self.in_shelter:
            raise RuntimeError("This bunny has returned to the shelter")
        if not isinstance(type_of_toy, str):
            raise TypeError("type_of_toy must be a string")

        toy = type_of_toy.strip().lower()
        if not toy:
            raise ValueError("type_of_toy must be non-empty")

        toy_fun = {
            "tunnel": 22,
            "ball": 16,
            "cardboard": 14,
        }
        if toy not in self.ALLOWED_TOYS:
            raise ValueError(
                "type_of_toy must be one of: tunnel, ball, cardboard"
            )
        fun_boost = toy_fun[toy]

        self.boredom -= fun_boost
        self.hunger += max(3, fun_boost // 4)
        self.exhaustion += max(4, fun_boost // 3)
        if self.hunger > 85 or self.exhaustion > 85:
            self.health -= 6

        self._clamp_all()
        self._check_runaway()
        return self.status()

    def sleep(self, time: int = 5) -> dict[str, object]:
        if self.in_shelter:
            raise RuntimeError("This bunny has returned to the shelter")
        if not isinstance(time, int):
            raise TypeError("time must be an int")
        if time <= 0:
            raise ValueError("time must be greater than 0")

        self.exhaustion -= 10 * time
        self.hunger += 4 * time
        self.boredom += 3 * time
        if self.hunger > 90:
            self.health -= 8

        self._clamp_all()
        self._check_runaway()
        return self.status()

    def _check_runaway(self) -> None:
        if self.health == 0 or self.boredom == 0 or self.exhaustion == 0:
            if not self.in_shelter:
                self.in_shelter = True
                return_one("bunny", self.name)

    def status(self) -> dict[str, object]:
        return {
            "name": self.name,
            "species": self.species,
            "health": self.health,
            "exhaustion": self.exhaustion,
            "boredom": self.boredom,
            "hunger": self.hunger,
            "mood": self._mood(),
            "ascii_art": self.ASCII_ART,
            "in_shelter": self.in_shelter,
        }
