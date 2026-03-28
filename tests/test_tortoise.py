import pytest

from desert_tortoise.tortoise import Tortoise
from desert_tortoise import shelter


@pytest.fixture(autouse=True)
def reset_shelter_inventory():
    shelter.SHELTER_INVENTORY.clear()
    shelter.SHELTER_INVENTORY.update(
        {
            "parrot": [{"species": "parrot", "default_name": "Sunny"}],
            "tortoise": [{"species": "tortoise", "default_name": "Ruby"}],
        }
    )


def test_adopt_tortoise_returns_tortoise_instance():
    pet = Tortoise.adopt("Mochi")
    assert isinstance(pet, Tortoise)
    assert pet.name == "Mochi"
    assert pet.species == "tortoise"
    assert pet.in_shelter is False


def test_adopt_tortoise_reduces_inventory():
    before = len(shelter.SHELTER_INVENTORY["tortoise"])
    pet = Tortoise.adopt("Shelly")
    after = len(shelter.SHELTER_INVENTORY["tortoise"])
    assert pet.name == "Shelly"
    assert before == 1
    assert after == 0


def test_adopt_tortoise_when_unavailable_raises_error():
    Tortoise.adopt("First")
    with pytest.raises(RuntimeError):
        Tortoise.adopt("Second")


def test_feed_greens_changes_stats():
    pet = Tortoise.adopt("Mochi")
    pet.hunger = 50
    pet.health = 80

    result = pet.feed("greens", 2)

    assert result["name"] == "Mochi"
    assert pet.hunger == 34
    assert pet.health == 84


def test_feed_weeds_changes_stats():
    pet = Tortoise.adopt("Mochi")
    pet.hunger = 60
    pet.health = 70

    pet.feed("weeds", 2)

    assert pet.hunger == 40
    assert pet.health == 72
    assert pet.species == "tortoise"


def test_feed_flowers_changes_stats_and_boredom():
    pet = Tortoise.adopt("Mochi")
    pet.hunger = 60
    pet.health = 70
    pet.boredom = 20

    pet.feed("flowers", 2)

    assert pet.hunger == 48
    assert pet.health == 76
    assert pet.boredom == 18


def test_feed_invalid_food_raises_value_error():
    pet = Tortoise.adopt("Mochi")
    with pytest.raises(ValueError):
        pet.feed("pizza", 1)


def test_feed_invalid_food_type_raises_type_error():
    pet = Tortoise.adopt("Mochi")
    with pytest.raises(TypeError):
        pet.feed(123, 1)  # type: ignore[arg-type]


def test_feed_invalid_amount_type_raises_type_error():
    pet = Tortoise.adopt("Mochi")
    with pytest.raises(TypeError):
        pet.feed("greens", "2")  # type: ignore[arg-type]


def test_feed_nonpositive_amount_raises_value_error():
    pet = Tortoise.adopt("Mochi")
    with pytest.raises(ValueError):
        pet.feed("greens", 0)

    with pytest.raises(ValueError):
        pet.feed("greens", -1)


def test_play_foraging_puzzle_changes_stats():
    pet = Tortoise.adopt("Mochi")
    pet.boredom = 40
    pet.hunger = 20
    pet.exhaustion = 10

    result = pet.play("foraging puzzle")

    assert result["species"] == "tortoise"
    assert pet.boredom == 22
    assert pet.hunger == 24
    assert pet.exhaustion == 13


def test_play_climbing_obstacle_changes_stats_and_health():
    pet = Tortoise.adopt("Mochi")
    pet.boredom = 50
    pet.hunger = 20
    pet.exhaustion = 10
    pet.health = 80

    pet.play("climbing obstacle")

    assert pet.boredom == 36
    assert pet.hunger == 25
    assert pet.exhaustion == 16
    assert pet.health == 83


def test_play_neck_scratch_changes_stats():
    pet = Tortoise.adopt("Mochi")
    pet.boredom = 25
    pet.hunger = 30
    pet.exhaustion = 15

    pet.play("neck scratch")

    assert pet.boredom == 15
    assert pet.hunger == 32
    assert pet.exhaustion == 16


def test_play_invalid_toy_raises_value_error():
    pet = Tortoise.adopt("Mochi")
    with pytest.raises(ValueError):
        pet.play("ball")


def test_play_empty_toy_raises_value_error():
    pet = Tortoise.adopt("Mochi")
    with pytest.raises(ValueError):
        pet.play("   ")


def test_play_invalid_toy_type_raises_type_error():
    pet = Tortoise.adopt("Mochi")
    with pytest.raises(TypeError):
        pet.play(123)  # type: ignore[arg-type]


def test_sleep_changes_stats():
    pet = Tortoise.adopt("Mochi")
    pet.exhaustion = 50
    pet.hunger = 20
    pet.boredom = 10

    result = pet.sleep(3)

    assert result["name"] == "Mochi"
    assert pet.exhaustion == 32
    assert pet.hunger == 29
    assert pet.boredom == 13


def test_sleep_applies_health_penalty_when_hunger_exceeds_90():
    pet = Tortoise.adopt("Mochi")
    pet.exhaustion = 40
    pet.hunger = 89
    pet.boredom = 10
    pet.health = 100

    pet.sleep(1)

    assert pet.hunger == 92
    assert pet.health == 94
    assert pet.exhaustion == 34


def test_sleep_invalid_time_type_raises_type_error():
    pet = Tortoise.adopt("Mochi")
    with pytest.raises(TypeError):
        pet.sleep("3")  # type: ignore[arg-type]


def test_sleep_nonpositive_time_raises_value_error():
    pet = Tortoise.adopt("Mochi")
    with pytest.raises(ValueError):
        pet.sleep(0)

    with pytest.raises(ValueError):
        pet.sleep(-2)


def test_status_returns_expected_keys():
    pet = Tortoise.adopt("Mochi")
    status = pet.status()

    assert status["name"] == "Mochi"
    assert status["species"] == "tortoise"
    assert "health" in status
    assert "exhaustion" in status
    assert "boredom" in status
    assert "hunger" in status
    assert "mood" in status
    assert "ascii_art" in status
    assert "in_shelter" in status


def test_status_contains_ascii_art():
    pet = Tortoise.adopt("Mochi")
    status = pet.status()

    assert isinstance(status["ascii_art"], str)
    assert "____" in status["ascii_art"]
    assert status["in_shelter"] is False


def test_tortoise_returns_to_shelter_when_health_hits_zero():
    pet = Tortoise.adopt("Mochi")
    pet.health = 0

    pet._check_runaway()

    assert pet.in_shelter is True
    assert len(shelter.SHELTER_INVENTORY["tortoise"]) == 1
    assert shelter.SHELTER_INVENTORY["tortoise"][0]["default_name"] == "Mochi"


def test_tortoise_returns_to_shelter_when_hunger_hits_100():
    pet = Tortoise.adopt("Mochi")
    pet.hunger = 100

    pet._check_runaway()

    assert pet.in_shelter is True
    assert len(shelter.SHELTER_INVENTORY["tortoise"]) == 1
    assert shelter.SHELTER_INVENTORY["tortoise"][0]["default_name"] == "Mochi"


def test_tortoise_methods_fail_after_returning_to_shelter():
    pet = Tortoise.adopt("Mochi")
    pet.health = 0
    pet._check_runaway()

    with pytest.raises(RuntimeError):
        pet.feed("greens", 1)

    with pytest.raises(RuntimeError):
        pet.play("neck scratch")

    with pytest.raises(RuntimeError):
        pet.sleep(1)


def test_values_are_clamped_between_0_and_100():
    pet = Tortoise.adopt("Mochi")
    pet.health = 99
    pet.hunger = 3
    pet.boredom = 1

    pet.feed("flowers", 5)

    assert 0 <= pet.health <= 100
    assert 0 <= pet.hunger <= 100
    assert 0 <= pet.boredom <= 100