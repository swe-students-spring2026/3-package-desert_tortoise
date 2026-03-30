import pytest

from desert_tortoise import shelter
from desert_tortoise.parrot import Parrot


@pytest.fixture(autouse=True)
def reset_shelter_inventory():
    shelter.SHELTER_INVENTORY.clear()
    shelter.SHELTER_INVENTORY.update(
        {
            "parrot": [{"species": "parrot", "default_name": "Sunny"}],
            "bunny": [{"species": "bunny", "default_name": "Clover"}],
            "tortoise": [{"species": "tortoise", "default_name": "Ruby"}],
            "cat": [{"species": "cat", "default_name": "Kitty"}],
        }
    )


def test_adopt_parrot_returns_parrot_instance():
    pet = Parrot.adopt("Kiwi")

    assert isinstance(pet, Parrot)
    assert pet.name == "Kiwi"
    assert pet.species == "parrot"
    assert pet.in_shelter is False


def test_adopt_parrot_reduces_inventory():
    before = len(shelter.SHELTER_INVENTORY["parrot"])
    pet = Parrot.adopt("Kiwi")
    after = len(shelter.SHELTER_INVENTORY["parrot"])

    assert pet.name == "Kiwi"
    assert before == 1
    assert after == 0


def test_adopt_parrot_when_unavailable_raises_error():
    Parrot.adopt("First")

    with pytest.raises(RuntimeError):
        Parrot.adopt("Second")


def test_feed_allowed_food_changes_stats():
    pet = Parrot.adopt("Kiwi")
    pet.hunger = 40
    pet.health = 80
    pet.exhaustion = 10

    result = pet.feed("seeds", 5)

    assert result["name"] == "Kiwi"
    assert pet.hunger == 35
    assert pet.health == 81
    assert pet.exhaustion == 10


def test_feed_invalid_food_raises_value_error():
    pet = Parrot.adopt("Kiwi")

    with pytest.raises(ValueError):
        pet.feed("pizza", 1)


def test_feed_invalid_types_raise_errors():
    pet = Parrot.adopt("Kiwi")

    with pytest.raises(TypeError):
        pet.feed(123, 1)  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        pet.feed("seeds", "2")  # type: ignore[arg-type]


def test_feed_nonpositive_amount_raises_value_error():
    pet = Parrot.adopt("Kiwi")

    with pytest.raises(ValueError):
        pet.feed("seeds", 0)
    with pytest.raises(ValueError):
        pet.feed("seeds", -1)


def test_play_mirror_changes_stats():
    pet = Parrot.adopt("Kiwi")
    pet.boredom = 40
    pet.hunger = 20
    pet.exhaustion = 10

    result = pet.play("mirror")

    assert result["species"] == "parrot"
    assert pet.boredom == 16
    assert pet.hunger == 28
    assert pet.exhaustion == 22


def test_play_applies_health_penalty_when_threshold_crossed():
    pet = Parrot.adopt("Kiwi")
    pet.health = 100
    pet.hunger = 84
    pet.exhaustion = 80

    pet.play("ladder")

    assert pet.hunger == 89
    assert pet.exhaustion == 88
    assert pet.health == 92


def test_play_invalid_toy_raises_value_error():
    pet = Parrot.adopt("Kiwi")

    with pytest.raises(ValueError):
        pet.play("string")
    with pytest.raises(ValueError):
        pet.play("   ")


def test_play_invalid_toy_type_raises_type_error():
    pet = Parrot.adopt("Kiwi")

    with pytest.raises(TypeError):
        pet.play(123)  # type: ignore[arg-type]


def test_sleep_changes_stats():
    pet = Parrot.adopt("Kiwi")
    pet.exhaustion = 50
    pet.hunger = 20
    pet.boredom = 10

    result = pet.sleep(2)

    assert result["name"] == "Kiwi"
    assert pet.exhaustion == 34
    assert pet.hunger == 30
    assert pet.boredom == 14


def test_sleep_applies_health_penalty_when_hunger_exceeds_90():
    pet = Parrot.adopt("Kiwi")
    pet.health = 90
    pet.hunger = 89

    pet.sleep(1)

    assert pet.hunger == 94
    assert pet.health == 80


def test_sleep_invalid_time_raises_errors():
    pet = Parrot.adopt("Kiwi")

    with pytest.raises(TypeError):
        pet.sleep("3")  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        pet.sleep(0)
    with pytest.raises(ValueError):
        pet.sleep(-2)


def test_status_returns_expected_keys_and_ascii_art():
    pet = Parrot.adopt("Kiwi")
    status = pet.status()

    assert status["name"] == "Kiwi"
    assert status["species"] == "parrot"
    assert "health" in status
    assert "exhaustion" in status
    assert "boredom" in status
    assert "hunger" in status
    assert "mood" in status
    assert "ascii_art" in status
    assert "m m" in status["ascii_art"]
    assert status["in_shelter"] is False


def test_parrot_returns_to_shelter_when_health_hits_zero():
    pet = Parrot.adopt("Kiwi")
    pet.boredom = 10

    # mirror drops boredom by 24, clamping to 0 and triggering runaway check.
    pet.play("mirror")

    assert pet.in_shelter is True
    assert len(shelter.SHELTER_INVENTORY["parrot"]) == 1
    assert shelter.SHELTER_INVENTORY["parrot"][0]["default_name"] == "Kiwi"


def test_methods_fail_after_returning_to_shelter():
    pet = Parrot.adopt("Kiwi")
    pet.boredom = 10
    pet.play("mirror")

    with pytest.raises(RuntimeError):
        pet.feed("seeds", 1)
    with pytest.raises(RuntimeError):
        pet.play("mirror")
    with pytest.raises(RuntimeError):
        pet.sleep(1)
