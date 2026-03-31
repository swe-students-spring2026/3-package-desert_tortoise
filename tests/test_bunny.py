import pytest

from desert_tortoise.bunny import Bunny
from desert_tortoise import shelter

@pytest.fixture(autouse=True)
def reset_shelter_inventory():
    shelter.SHELTER_INVENTORY.clear()
    shelter.SHELTER_INVENTORY.update(
        {
            "parrot": [{"species": "parrot", "default_name": "Sunny"}],
            "bunny": [{"species": "bunny", "default_name": "Clover"}],
            "tortoise": [{"species": "tortoise", "default_name": "Ruby"}],
            "cat": [{"species": "cat", "default_name": "Kitty"}],
            "dog": [{"species": "dog", "default_name": "Bella"}],
        }
    )

# adopt
def test_adopt_bunny_returns_bunny_instance():
    pet = Bunny.adopt("Flopsy")
    assert isinstance(pet, Bunny)
    assert pet.name == "Flopsy"
    assert pet.species == "bunny"
    assert pet.in_shelter is False

def test_adopt_bunny_reduces_inventory():
    before = len(shelter.SHELTER_INVENTORY["bunny"])
    Bunny.adopt("Flopsy")
    after = len(shelter.SHELTER_INVENTORY["bunny"])
    assert before == 1
    assert after == 0

def test_adopt_bunny_when_unavailable_raises_error():
    Bunny.adopt("First")
    with pytest.raises(RuntimeError):
        Bunny.adopt("Second")

#feed
def test_feed_hay_changes_stats():
    pet = Bunny.adopt("Flopsy")
    pet.hunger = 50
    pet.health = 80
    pet.exhaustion = 20

    pet.feed("hay", 8)

    assert pet.hunger == 42
    assert pet.health == 82
    assert pet.exhaustion == 20

def test_feed_carrots_changes_stats():
    pet = Bunny.adopt("Flopsy")
    pet.hunger = 50
    pet.health = 80

    pet.feed("carrots", 4)

    assert pet.hunger == 46
    assert pet.health == 81

def test_feed_lettuce_changes_stats():
    pet = Bunny.adopt("Flopsy")
    pet.hunger = 50
    pet.health = 80

    pet.feed("lettuce", 12)

    assert pet.hunger == 38
    assert pet.health == 83
    assert pet.exhaustion == 21  # default 20 + 1

def test_feed_is_case_insensitive_and_strips_whitespace():
    pet = Bunny.adopt("Flopsy")
    pet.hunger = 50

    pet.feed("  HAY  ", 5)

    assert pet.hunger == 45

def test_feed_invalid_food_raises_value_error():
    pet = Bunny.adopt("Flopsy")
    with pytest.raises(ValueError):
        pet.feed("pizza", 1)

def test_feed_invalid_food_type_raises_type_error():
    pet = Bunny.adopt("Flopsy")
    with pytest.raises(TypeError):
        pet.feed(123, 1)

def test_feed_invalid_amount_type_raises_type_error():
    pet = Bunny.adopt("Flopsy")
    with pytest.raises(TypeError):
        pet.feed("hay", "2")

def test_feed_float_amount_raises_type_error():
    pet = Bunny.adopt("Flopsy")
    with pytest.raises(TypeError):
        pet.feed("hay", 1.5)

def test_feed_nonpositive_amount_raises_value_error():
    pet = Bunny.adopt("Flopsy")
    with pytest.raises(ValueError):
        pet.feed("hay", 0)
    with pytest.raises(ValueError):
        pet.feed("hay", -3)

def test_feed_bunny_in_shelter_raises_runtime_error():
    pet = Bunny.adopt("Flopsy")
    pet.in_shelter = True
    with pytest.raises(RuntimeError):
        pet.feed("hay", 1)

#play
def test_play_tunnel_changes_stats():
    pet = Bunny.adopt("Flopsy")
    pet.boredom = 50
    pet.hunger = 30
    pet.exhaustion = 20

    pet.play("tunnel")

    assert pet.boredom == 28
    assert pet.hunger == 35
    assert pet.exhaustion == 27

def test_play_ball_changes_stats():
    pet = Bunny.adopt("Flopsy")
    pet.boredom = 50
    pet.hunger = 30
    pet.exhaustion = 20

    pet.play("ball")

    assert pet.boredom == 34
    assert pet.hunger == 34
    assert pet.exhaustion == 25

def test_play_cardboard_changes_stats():
    pet = Bunny.adopt("Flopsy")
    pet.boredom = 50
    pet.hunger = 30
    pet.exhaustion = 20

    pet.play("cardboard")

    assert pet.boredom == 36
    assert pet.hunger == 33
    assert pet.exhaustion == 24

def test_play_is_case_insensitive_and_strips_whitespace():
    pet = Bunny.adopt("Flopsy")
    pet.boredom = 50

    pet.play("  TUNNEL  ")

    assert pet.boredom == 28

def test_play_health_penalty_when_hunger_high():
    pet = Bunny.adopt("Flopsy")
    pet.hunger = 90
    pet.health = 80

    pet.play("tunnel")

    assert pet.health == 74  

def test_play_health_penalty_when_exhaustion_high():
    pet = Bunny.adopt("Flopsy")
    pet.exhaustion = 90
    pet.health = 80

    pet.play("tunnel")

    assert pet.health == 74 

def test_play_invalid_toy_raises_value_error():
    pet = Bunny.adopt("Flopsy")
    with pytest.raises(ValueError):
        pet.play("laser")

def test_play_empty_toy_raises_value_error():
    pet = Bunny.adopt("Flopsy")
    with pytest.raises(ValueError):
        pet.play("   ")

def test_play_invalid_toy_type_raises_type_error():
    pet = Bunny.adopt("Flopsy")
    with pytest.raises(TypeError):
        pet.play(123)

def test_play_bunny_in_shelter_raises_runtime_error():
    pet = Bunny.adopt("Flopsy")
    pet.in_shelter = True
    with pytest.raises(RuntimeError):
        pet.play("tunnel")

#sleep 
def test_sleep_changes_stats():
    pet = Bunny.adopt("Flopsy")
    pet.exhaustion = 50
    pet.hunger = 20
    pet.boredom = 10

    pet.sleep(2)

    assert pet.exhaustion == 30
    assert pet.hunger == 28
    assert pet.boredom == 16

def test_sleep_health_penalty_when_hunger_exceeds_90():
    pet = Bunny.adopt("Flopsy")
    pet.hunger = 89
    pet.health = 100

    pet.sleep(1)

    assert pet.hunger == 93
    assert pet.health == 92

def test_sleep_no_health_penalty_when_hunger_at_or_below_90():
    pet = Bunny.adopt("Flopsy")
    pet.hunger = 50
    pet.health = 100

    pet.sleep(1)

    assert pet.health == 100

def test_sleep_invalid_time_type_raises_type_error():
    pet = Bunny.adopt("Flopsy")
    with pytest.raises(TypeError):
        pet.sleep("3")

def test_sleep_nonpositive_time_raises_value_error():
    pet = Bunny.adopt("Flopsy")
    with pytest.raises(ValueError):
        pet.sleep(0)
    with pytest.raises(ValueError):
        pet.sleep(-2)

def test_sleep_bunny_in_shelter_raises_runtime_error():
    pet = Bunny.adopt("Flopsy")
    pet.in_shelter = True
    with pytest.raises(RuntimeError):
        pet.sleep(2)

# status

def test_status_returns_expected_keys():
    pet = Bunny.adopt("Flopsy")
    status = pet.status()

    assert status["name"] == "Flopsy"
    assert status["species"] == "bunny"
    assert "health" in status
    assert "exhaustion" in status
    assert "boredom" in status
    assert "hunger" in status
    assert "mood" in status
    assert "ascii_art" in status
    assert "in_shelter" in status

def test_status_ascii_art_is_bunny():
    pet = Bunny.adopt("Flopsy")
    status = pet.status()

    assert isinstance(status["ascii_art"], str)
    assert len(status["ascii_art"]) > 0

def test_status_in_shelter_false_initially():
    pet = Bunny.adopt("Flopsy")
    status = pet.status()

    assert status["in_shelter"] is False

# runaway checks

def test_bunny_returns_to_shelter_when_health_hits_zero():
    pet = Bunny.adopt("Flopsy")
    pet.health = 0

    pet._check_runaway()

    assert pet.in_shelter is True
    assert len(shelter.SHELTER_INVENTORY["bunny"]) == 1
    assert shelter.SHELTER_INVENTORY["bunny"][0]["default_name"] == "Flopsy"

def test_bunny_returns_to_shelter_when_hunger_hits_100():
    pet = Bunny.adopt("Flopsy")
    pet.hunger = 100

    pet._check_runaway()

    assert pet.in_shelter is True
    assert len(shelter.SHELTER_INVENTORY["bunny"]) == 1
    assert shelter.SHELTER_INVENTORY["bunny"][0]["default_name"] == "Flopsy"

def test_bunny_returns_to_shelter_when_exhaustion_hits_100():
    pet = Bunny.adopt("Flopsy")
    pet.exhaustion = 100

    pet._check_runaway()

    assert pet.in_shelter is True
    assert len(shelter.SHELTER_INVENTORY["bunny"]) == 1
    assert shelter.SHELTER_INVENTORY["bunny"][0]["default_name"] == "Flopsy"

def test_no_runaway_when_stats_are_healthy():
    pet = Bunny.adopt("Flopsy")

    pet._check_runaway()

    assert pet.in_shelter is False

def test_methods_fail_after_returning_to_shelter():
    pet = Bunny.adopt("Flopsy")
    pet.hunger = 100
    pet._check_runaway()

    with pytest.raises(RuntimeError):
        pet.feed("hay", 1)
    with pytest.raises(RuntimeError):
        pet.play("tunnel")
    with pytest.raises(RuntimeError):
        pet.sleep(1)

# value bounds checks
def test_stats_are_clamped_between_0_and_100():
    pet = Bunny.adopt("Flopsy")
    pet.hunger = 5
    pet.health = 98
    pet.boredom = 2

    pet.feed("hay", 20)

    assert 0 <= pet.hunger <= 100
    assert 0 <= pet.health <= 100
    assert 0 <= pet.boredom <= 100
    assert 0 <= pet.exhaustion <= 100

def test_boredom_clamps_to_zero_not_negative():
    pet = Bunny.adopt("Flopsy")
    pet.boredom = 10

    pet.play("tunnel")  

    assert pet.boredom == 0

# mood
def test_mood_happy_by_default():
    pet = Bunny.adopt("Flopsy")
    status = pet.status()

    assert status["mood"] == "happy"

def test_mood_hungry_when_hunger_high():
    pet = Bunny.adopt("Flopsy")
    pet.hunger = 75

    assert pet.status()["mood"] == "hungry"

def test_mood_sick_when_health_low():
    pet = Bunny.adopt("Flopsy")
    pet.health = 20

    assert pet.status()["mood"] == "sick"

def test_mood_sleepy_when_exhaustion_high():
    pet = Bunny.adopt("Flopsy")
    pet.exhaustion = 75

    assert pet.status()["mood"] == "sleepy"

def test_mood_bored_when_boredom_high():
    pet = Bunny.adopt("Flopsy")
    pet.boredom = 75

    assert pet.status()["mood"] == "bored"