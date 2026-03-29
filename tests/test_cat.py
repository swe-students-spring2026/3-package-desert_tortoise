import pytest
from desert_tortoise.cat import Cat
from desert_tortoise import shelter

@pytest.fixture(autouse=True)
def reset_shelter_inventory():
    shelter.SHELTER_INVENTORY.clear()
    shelter.SHELTER_INVENTORY.update(
        {
            "parrot": [{"species": "parrot", "default_name": "Sunny"}],
            "tortoise": [{"species": "tortoise", "default_name": "Ruby"}],
            "cat": [{"species": "cat", "default_name": "Kitty"}],
        }
    )
#test init
#test adopt
def test_adopt_cat_returns_cat_instance():
    pet = Cat.adopt("Kitty")
    assert isinstance(pet, Cat)
    assert pet.name == "Kitty"
    assert pet.species == "cat"
    assert pet.in_shelter is False

def test_adopt_cat_reduces_inventory():
    before = len(shelter.SHELTER_INVENTORY["cat"])
    pet = Cat.adopt("Kitty")
    after = len(shelter.SHELTER_INVENTORY["cat"])
    assert pet.name == "Kitty"
    assert before == 1
    assert after == 0


def test_adopt_cat_when_unavailable_raises_error():
    Cat.adopt("First")
    with pytest.raises(RuntimeError):
        Cat.adopt("Second")

#test feed
def test_feed_meat_stats():
    pet = Cat.adopt("Kitty")
    health = pet.health
    hunger = pet.hunger
    expected_health = max(0, min(100,health + 7))
    expected_hunger = max(0, min(100,hunger - 10))
    pet.feed("meat", 1)
    assert pet.health == expected_health
    assert pet.hunger == expected_hunger

    
def test_feed_fish_stats():
    pet = Cat.adopt("Kitty")
    health = pet.health
    hunger = pet.hunger
    expected_health = max(0, min(100,health + 7))
    expected_hunger = max(0, min(100,hunger - 10))
    pet.feed("fish", 1)
    assert pet.health == expected_health
    assert pet.hunger == expected_hunger

def test_feed_treat_stats():
    pet = Cat.adopt("Kitty")
    health = pet.health
    hunger = pet.hunger
    expected_health = max(0, min(100,health + 3))
    expected_hunger = max(0, min(100,hunger - 6))
    pet.feed("treat", 1)
    assert pet.health == expected_health
    assert pet.hunger == expected_hunger

def test_feed_unallowed_stats():
    pet = Cat.adopt("Kitty")
    boredom = pet.boredom
    expected_boredom = max(0, min(100,boredom + 10))
    pet.feed("zzz", 1)
    assert pet.boredom == expected_boredom


def test_feed_invalid_food_type_raises_type_error():
    pet = Cat.adopt("Kitty")
    with pytest.raises(TypeError):
        pet.feed(123, 1)


def test_feed_invalid_amount_type_raises_type_error():
    pet = Cat.adopt("Kitty")
    with pytest.raises(TypeError):
        pet.feed("fish", "2") 


def test_feed_nonpositive_amount_raises_value_error():
    pet = Cat.adopt("Kitty")
    with pytest.raises(ValueError):
        pet.feed("fish", 0)

    with pytest.raises(ValueError):
        pet.feed("fish", -1)

def test_feed_cat_in_shelter_raises_runtime_error():
    pet = Cat.adopt("Kitty")
    pet.in_shelter = True
    with pytest.raises(RuntimeError):
        pet.feed("meat")

#test play
def test_play_cardboard_stats():
    pet = Cat.adopt("Kitty")
    expected_boredom = max(0, min(100,pet.boredom - 10))
    expected_exhaustion = max(0, min(100,pet.exhaustion + 5))
    expected_hunger = max(0, min(100,pet.hunger + 3))
    pet.play("cardboard")
    assert expected_boredom == pet.boredom
    assert expected_exhaustion == pet.exhaustion
    assert expected_hunger == pet.hunger

def test_play_feather_stats():
    pet = Cat.adopt("Kitty")
    expected_boredom = max(0, min(100,pet.boredom - 20))
    expected_exhaustion = max(0, min(100,pet.exhaustion + 10))
    expected_hunger = max(0, min(100,pet.hunger + 6))
    pet.play("feather")
    assert expected_boredom == pet.boredom
    assert expected_exhaustion == pet.exhaustion
    assert expected_hunger == pet.hunger

def test_play_mouse_stats():
    pet = Cat.adopt("Kitty")
    expected_boredom = max(0, min(100,pet.boredom - 30))
    expected_exhaustion = max(0, min(100,pet.exhaustion + 15))
    expected_hunger = max(0, min(100,pet.hunger + 9))
    pet.play("mouse")
    assert expected_boredom == pet.boredom
    assert expected_exhaustion == pet.exhaustion
    assert expected_hunger == pet.hunger

def test_play_health_hit():
    pet = Cat.adopt("Kitty")
    pet.hunger = 90
    pet.exhaustion = 90
    expected_health = max(0, min(100,pet.health - 10))
    pet.play("mouse")
    assert expected_health == pet.health

def test_play_invalid_toy_raises_value_error():
    pet = Cat.adopt("Kitty")
    with pytest.raises(ValueError):
        pet.play("zzz")


def test_play_empty_toy_raises_value_error():
    pet = Cat.adopt("Kitty")
    with pytest.raises(ValueError):
        pet.play("   ")


def test_play_invalid_toy_type_raises_type_error():
    pet = Cat.adopt("Kitty")
    with pytest.raises(TypeError):
        pet.play(123)  # type: ignore[arg-type]

def test_play_cat_in_shelter_raises_runtime_error():
    pet = Cat.adopt("Kitty")
    pet.in_shelter = True
    with pytest.raises(RuntimeError):
        pet.play("feather")

#test sleep
def test_sleep_stats():
    pet = Cat.adopt("Kitty")
    expected_exhaustion = max(0, min(100,pet.exhaustion - 2))
    expected_hunger = max(0, min(100,pet.hunger + 1))
    pet.sleep(1)
    assert expected_exhaustion == pet.exhaustion
    assert expected_hunger == pet.hunger

def test_sleep_health_hit():
    pet = Cat.adopt("Kitty")
    pet.hunger = 90
    pet.exhaustion = 90
    expected_health = max(0, min(100,pet.health - 10))
    pet.sleep(2)
    assert expected_health == pet.health

def test_sleep_invalid_time_type_raises_type_error():
    pet = Cat.adopt("Kitty")
    with pytest.raises(TypeError):
        pet.sleep("3")  # type: ignore[arg-type]


def test_sleep_nonpositive_time_raises_value_error():
    pet = Cat.adopt("Kitty")
    with pytest.raises(ValueError):
        pet.sleep(0)

    with pytest.raises(ValueError):
        pet.sleep(-2)

def test_sleep_cat_in_shelter_raises_runtime_error():
    pet = Cat.adopt("Kitty")
    pet.in_shelter = True
    with pytest.raises(RuntimeError):
        pet.sleep(2)

#test status
def test_status_returns_expected_keys():
    pet = Cat.adopt("Kitty")
    status = pet.status()

    assert status["name"] == "Kitty"
    assert status["species"] == "cat"
    assert "health" in status
    assert "exhaustion" in status
    assert "boredom" in status
    assert "hunger" in status
    assert "mood" in status
    assert "ascii_art" in status
    assert "in_shelter" in status

#test check runaway
def test_cat_returns_to_shelter_when_health_hits_zero():
    pet = Cat.adopt("Kitty")
    pet.health = 0

    pet._check_runaway()

    assert pet.in_shelter is True
    assert len(shelter.SHELTER_INVENTORY["cat"]) == 1
    assert shelter.SHELTER_INVENTORY["cat"][0]["default_name"] == "Kitty"


def test_cat_returns_to_shelter_when_hunger_hits_100():
    pet = Cat.adopt("Kitty")
    pet.hunger = 100

    pet._check_runaway()

    assert pet.in_shelter is True
    assert len(shelter.SHELTER_INVENTORY["cat"]) == 1
    assert shelter.SHELTER_INVENTORY["cat"][0]["default_name"] == "Kitty"