"""Digital pet package."""

from .pet import Pet
from .tortoise import Tortoise
from .parrot import Parrot
from . import shelter
from .bunny import Bunny
from .dog import Dog

__all__ = ["Pet", "Parrot", "Bunny", "shelter", "Tortoise", "Dog"]
