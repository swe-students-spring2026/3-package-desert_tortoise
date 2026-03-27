"""Digital pet package."""

from .parrot import Parrot
from .pet import Pet
from . import shelter
from .bunny import Bunny

__all__ = ["Pet", "Parrot", "Bunny", "shelter"]
