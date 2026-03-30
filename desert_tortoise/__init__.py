"""Digital pet package."""

from .pet import Pet
from .tortoise import Tortoise
from .parrot import Parrot
from .cat import Cat
from . import shelter
from .bunny import Bunny

__all__ = ["Pet", "Parrot", "Bunny", "shelter", "Tortoise", "Cat"]