from __future__ import annotations

from .pet import Pet
from .shelter import adopt_one, return_one

import random

class Cat(Pet):
    ASCII_ART = (
        "            (\\(\\\n"
        "            / ..(\n"
        "         .-' ,_Y/\n"
        "       .'     (\n"
        "      /   \\/  |\n"
        "     _|  _/| // \n"
        "   .',_\\__)\\_)) \n"
        "   '----,)\n"
    )
    ALLOWED_TOYS = {"cardboard", "feather", "mouse"}

    def __init__(self, name: str) -> None:
        super().__init__(name=name, species="cat")
    
    @classmethod
    def adopt(cls, name: str) -> "Cat":
        adopt_one("cat")
        return cls(name=name)
    
    def feed(self, food_type: str, amount: int = 1) -> dict[str, object]:
        """Feed this pet by an amount of food."""
        if self.in_shelter:
            raise RuntimeError("This cat has returned to the shelter")
        if not isinstance(food_type, str):
            raise TypeError("food type must be string")
        if not isinstance(amount, int):
            raise TypeError("amount must be an int")
        if amount <= 0:
            raise ValueError("amount must be greater than 0")
        
        if("fish" in food_type or "meat" in food_type):
            self.hunger -= 10*amount
            self.health += 7*amount
        elif("treat" in food_type):
            self.hunger -= 6*amount
            self.health += 3*amount
        else:
            self.boredom += 10

        self._clamp_all()
        self._check_runaway()
        return self.status()


    def play(self, type_of_toy: str) -> dict[str, object]:
        """Play with this pet using a toy type."""
        if self.in_shelter:
            raise RuntimeError("This cat has returned to the shelter")
        if not isinstance(type_of_toy, str):
            raise TypeError("toy type must be string")
        if type_of_toy.strip().lower() not in self.ALLOWED_TOYS:
            raise ValueError("toy must be one of: cardboard, feather, mouse")
        
        interest = random.randint(1, 3)
        self.boredom -= interest*10
        self.exhaustion += interest*5
        self.hunger += interest*3

        if self.hunger >= 100 or self.exhaustion >= 100:
            self.health -= 20
        elif self.hunger > 85 or self.exhaustion > 85:
            self.health -= 10

        self._clamp_all()
        self._check_runaway()
        return self.status()

    def sleep(self, time: int = 5) -> dict[str, object]:
        """Put this pet to sleep for some amount of time."""
        if self.in_shelter:
            raise RuntimeError("This cat has returned to the shelter")
        if not isinstance(time, int):
            raise TypeError("time must be an int")
        if time <= 0:
            raise ValueError("time must be greater than 0")

        
        self.exhaustion -= time * 2
        self.hunger += time

        if self.hunger >= 100 or self.exhaustion >= 100:
            self.health -= 20
        elif self.hunger > 85 or self.exhaustion > 85:
            self.health -= 10

        self._clamp_all()
        self._check_runaway()
        return self.status()

    def _extra_status(self) -> dict[str, object]:
        return {"ascii_art": self.ASCII_ART}

    def _check_runaway(self) -> None:
        """Return pet to shelter when critical stats reach zero."""
        if self.health == 0 or self.boredom == 0 or self.exhaustion == 0:
            if not self.in_shelter:
                self.in_shelter = True
                return_one("cat", self.name)