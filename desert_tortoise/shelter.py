"""Shared shelter inventory for all pet species."""

from __future__ import annotations

# Species inventory can scale as new pets are added.
SHELTER_INVENTORY: dict[str, list[dict[str, str]]] = {
    "parrot": [{"species": "parrot", "default_name": "Sunny"}],
    "bunny": [{"species": "bunny", "default_name": "Clover"}],
    "tortoise": [{"species": "tortoise", "default_name": "Ruby"}],
    "dog": [{"species": "dog", "default_name": "Bella"}],
    "cat": [{"species": "cat", "default_name": "Kitty"}],
}


def has_available(species: str) -> bool:
    """Return True when at least one pet of this species is available."""
    key = species.strip().lower()
    return bool(SHELTER_INVENTORY.get(key, []))


def adopt_one(species: str) -> dict[str, str]:
    """Remove and return one pet record of the requested species."""
    key = species.strip().lower()
    inventory = SHELTER_INVENTORY.get(key, [])
    if not inventory:
        raise RuntimeError(f"No {key}s available in shelter right now")
    return inventory.pop(0)


def return_one(species: str, default_name: str) -> None:
    """Return a pet back to shelter inventory."""
    key = species.strip().lower()
    SHELTER_INVENTORY.setdefault(key, []).append(
        {"species": key, "default_name": default_name}
    )


def snapshot() -> dict[str, list[dict[str, str]]]:
    """Read-only copy of shelter inventory for debugging or status views."""
    return {species: pets.copy() for species, pets in SHELTER_INVENTORY.items()}