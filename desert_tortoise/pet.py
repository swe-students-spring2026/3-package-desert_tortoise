"""Digital pet abstract base class."""

from __future__ import annotations

from abc import ABC, abstractmethod


class Pet(ABC):
    """Abstract base class for all digital pets."""

    def __init__(
        self,
        name: str,
        species: str,
        health: int = 100,
        exhaustion: int = 20,
        boredom: int = 30,
        hunger: int = 40,
    ) -> None:
        self.name = name.strip()
        self.species = species.strip().lower()
        if not self.name:
            raise ValueError("name must be a non-empty string")
        if not self.species:
            raise ValueError("species must be a non-empty string")

        self.health = health
        self.exhaustion = exhaustion
        self.boredom = boredom
        self.hunger = hunger
        self.in_shelter = False
        self._clamp_all()

    @classmethod
    @abstractmethod
    def adopt(cls, name: str) -> "Pet":
        """Create and return a pet of this type."""

    @abstractmethod
    def feed(self, food_type: str, amount: int = 1) -> dict[str, object]:
        """Feed this pet by an amount of food."""

    @abstractmethod
    def play(self, type_of_toy: str) -> dict[str, object]:
        """Play with this pet using a toy type."""

    @abstractmethod
    def sleep(self, time: int = 5) -> dict[str, object]:
        """Put this pet to sleep for some amount of time."""

    @abstractmethod
    def status(self) -> dict[str, object]:
        """Return this pet's current state."""

    @abstractmethod
    def _check_runaway(self) -> None:
        """Return pet to shelter when critical stats reach zero."""

    def _mood(self) -> str:
        if self.health <= 25:
            return "sick"
        if self.hunger >= 70:
            return "hungry"
        if self.exhaustion >= 70:
            return "sleepy"
        if self.boredom >= 70:
            return "bored"
        return "happy"

    def _clamp_all(self) -> None:
        self.health = max(0, min(100, self.health))
        self.exhaustion = max(0, min(100, self.exhaustion))
        self.boredom = max(0, min(100, self.boredom))
        self.hunger = max(0, min(100, self.hunger))
