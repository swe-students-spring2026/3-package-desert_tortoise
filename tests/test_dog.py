import pytest

from desert_tortoise.dog import Dog
from desert_tortoise import shelter


@pytest.fixture(autouse=True)
def reset_shelter():
    shelter.SHELTER_INVENTORY.clear()
    shelter.SHELTER_INVENTORY.update(
        {
            "parrot": [{"species": "parrot", "default_name": "Sunny"}],
            "tortoise": [{"species": "tortoise", "default_name": "Ruby"}],
            "cat": [{"species": "cat", "default_name": "Kitty"}],
            "dog": [{"species": "dog", "default_name": "Bella"}],
        }
    )


#adopt
def test_adopt_dog_returns_dog_instance():
    dog = Dog.adopt("Luna")
    assert isinstance(dog, Dog)


def test_adopt_sets_name():
    dog = Dog.adopt("Luna")
    assert dog.name == "Luna"


def test_adopt_sets_species():
    dog = Dog.adopt("Luna")
    assert dog.species == "dog"

def test_adopt_sets_remove_from_shelter():
    dog = Dog.adopt("Luna")
    assert dog.in_shelter is False


def test_adopt_dog_reduces_inventory():
    before = len(shelter.SHELTER_INVENTORY["dog"])
    Dog.adopt("Luna")
    after = len(shelter.SHELTER_INVENTORY["dog"])
    assert before == 1
    assert after == 0


def test_adopt_dog_when_available_raises_eror():
    Dog.adopt("Luna")
    with pytest.raises(RuntimeError):
        Dog.adopt("Max")


#feed
def test_feed_meat_changes_stats():
    dog = Dog.adopt("Luna")
    dog.hunger = 50
    dog.health = 50
    dog.feed("meat", 1)
    assert dog.hunger < 50
    assert dog.health > 50


def test_feed_peanut_butter_reduces_boredom():
    dog = Dog.adopt("Luna")
    expected_boredom = max(0, min(100, dog.boredom - 1))
    dog.feed("peanut butter", 1)
    assert dog.boredom == expected_boredom


def test_feed_fruits_changes_stats():
    dog = Dog.adopt("Luna")
    dog.hunger = 50
    dog.health = 50
    dog.feed("fruits", 4)
    assert dog.hunger < 50
    assert dog.health > 50


def test_feed_not_allowed_food():
    dog = Dog.adopt("Luna")
    with pytest.raises(ValueError):
        dog.feed("chocolate", 1)


def test_feed_non_string_food():
    dog = Dog.adopt("Luna")
    with pytest.raises(TypeError):
        dog.feed(1, 1)


def test_feed_invalid_amount_type():
    dog = Dog.adopt("Luna")
    with pytest.raises(TypeError):
        dog.feed("meat", "one")


def test_feed_non_int_amount():
    dog = Dog.adopt("Luna")
    with pytest.raises(TypeError):
        dog.feed("meat", 1.5)


def test_feed_nonpositive_amount():
    dog = Dog.adopt("Luna")
    with pytest.raises(ValueError):
        dog.feed("meat", 0)
    with pytest.raises(ValueError):
        dog.feed("meat", -2)


def test_feed_dog_in_shelter_raises_runtime_error():
    dog = Dog.adopt("Luna")
    dog.in_shelter = True
    with pytest.raises(RuntimeError):
        dog.feed("meat", 1)


#play

def test_play_bone_changes_stats():
    dog = Dog.adopt("Luna")
    dog.boredom = 50
    dog.exhaustion = 50
    dog.hunger = 50
    dog.play("bone")
    assert dog.boredom < 50
    assert dog.exhaustion > 50
    assert dog.hunger > 50


def test_play_stick_changes_stats():
    dog = Dog.adopt("Luna")
    dog.boredom = 50
    dog.exhaustion = 50
    dog.hunger = 50
    dog.play("stick")
    assert  dog.boredom < 50
    assert dog.exhaustion > 50
    assert dog.hunger > 50


def test_play_ball_changes_stats():
    dog = Dog.adopt("Luna")
    dog.boredom = 50
    dog.exhaustion = 50
    dog.hunger = 50
    dog.play("ball")
    assert  dog.boredom < 50
    assert dog.exhaustion > 50
    assert dog.hunger > 50

def test_play_invalid_toy():
    dog = Dog.adopt("Luna")
    with pytest.raises(ValueError):
        dog.play("laser")


def test_play_empty_string():
    dog = Dog.adopt("Luna")
    with pytest.raises(ValueError):
        dog.play(" ")


def test_play_non_string_toy():
    dog = Dog.adopt("Luna")
    with pytest.raises(TypeError):
        dog.play(1)


def test_play_high_hunger_reduce_health():
    dog = Dog.adopt("Luna")
    dog.hunger = 90
    dog.health = 50
    dog.play("ball")
    assert dog.health < 50


def test_play_high_exhaustion_reduce_health():
    dog = Dog.adopt("Luna")
    dog.exhaustion = 90
    dog.health = 50
    dog.play("stick")
    assert dog.health < 50


def test_play_dog_in_shelter_raises_runtime_error():
    dog = Dog.adopt("Luna")
    dog.in_shelter = True
    with pytest.raises(RuntimeError):
        dog.play("feather")


#sleep
def test_sleep_reduces_exhaustion():
    dog = Dog.adopt("Luna")
    dog.exhaustion = 50
    dog.sleep(2)
    assert dog.exhaustion < 50


def test_sleep_increases_hunger():
    dog = Dog.adopt("Luna")
    dog.hunger = 50
    dog.sleep(2)
    assert dog.hunger > 50


def test_sleep_increases_boredom():
    dog = Dog.adopt("Luna")
    dog.boredom = 50
    dog.sleep(2)
    assert dog.boredom > 50


def test_sleep_high_hunger_reduce_health():
    dog = Dog.adopt("Luna")
    dog.hunger = 88
    dog.health = 50
    dog.sleep(2)
    assert dog.health < 50


def test_sleep_non_int_time():
    dog = Dog.adopt("Luna")
    with pytest.raises(TypeError):
        dog.sleep("two")


def test_sleep_zero_time():
    dog = Dog.adopt("Luna")
    with pytest.raises(ValueError):
        dog.sleep(0)


def test_sleep_negative_time():
    dog = Dog.adopt("Luna")
    with pytest.raises(ValueError):
        dog.sleep(-3)


def test_sleep_shelter_dog_raises():
    dog = Dog.adopt("Luna")
    dog.in_shelter = True
    with pytest.raises(RuntimeError):
        dog.sleep(3)


#status

def test_status_returns_dict():
    dog = Dog.adopt("Luna")
    result = dog.status()
    assert isinstance(result, dict)


def test_status_contains_name():
    dog = Dog.adopt("Luna")
    dog_status = dog.status()
    assert dog_status["name"] == "Luna"


def test_status_contains_species():
    dog = Dog.adopt("Luna")
    dog_status = dog.status()
    assert dog_status["species"] == "dog"


def test_status_contains_all_keys():
    dog = Dog.adopt("Luna")
    dog_status = dog.status()
    expected_keys = {"name", "species", "health", "exhaustion", "boredom", "hunger", "mood", "in_shelter"}
    assert expected_keys.issubset(dog_status.keys())


#runaway
def test_runaway_when_health_hits_zero():
    dog = Dog.adopt("Luna")
    dog.health = 0
    dog._check_runaway()
    assert dog.in_shelter is True
    assert len(shelter.SHELTER_INVENTORY["dog"]) == 1
    assert shelter.SHELTER_INVENTORY["dog"][0]["default_name"] == "Luna"


def test_runaway_when_hunger_hits_100():
    dog = Dog.adopt("Luna")
    dog.hunger = 100
    dog._check_runaway()
    assert dog.in_shelter is True
    assert len(shelter.SHELTER_INVENTORY["dog"]) == 1
    assert shelter.SHELTER_INVENTORY["dog"][0]["default_name"] == "Luna"


def test_runaway_when_exhaustion_hits_100():
    dog = Dog.adopt("Luna")
    dog.exhaustion = 100
    dog._check_runaway()
    assert dog.in_shelter is True
    assert len(shelter.SHELTER_INVENTORY["dog"]) == 1
    assert shelter.SHELTER_INVENTORY["dog"][0]["default_name"] == "Luna"


def test_no_runaway_healthy_dog():
    dog = Dog.adopt("Luna")
    dog._check_runaway()
    assert dog.in_shelter is False