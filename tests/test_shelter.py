import pytest

from desert_tortoise import shelter


@pytest.fixture(autouse=True)
def reset_shelter_inventory():
    shelter.SHELTER_INVENTORY.clear()
    shelter.SHELTER_INVENTORY.update(
        {
            "parrot": [{"species": "parrot", "default_name": "Sunny"}],
            "tortoise": [{"species": "tortoise", "default_name": "Ruby"}],
            "bunny": [{"species": "bunny", "default_name": "Clover"}],
            "dog": [{"species": "dog", "default_name": "Bella"}],
            "cat": [{"species": "cat", "default_name": "Kitty"}],
        }
    )
    
def test_has_available_returns_true_for_existing_species():
    assert shelter.has_available("parrot") is True
    assert shelter.has_available("tortoise") is True
    assert shelter.has_available("PARROT") is True


def test_has_available_returns_false_for_unknown_species():
    assert shelter.has_available("dragon") is False
    assert shelter.has_available("unicorn") is False


def test_adopt_one_removes_pet_from_inventory():
    shelter.adopt_one("cat")
    assert shelter.SHELTER_INVENTORY["cat"] == []

def test_adopt_one_is_case_insensitive():
    pet = shelter.adopt_one("DOG")
    assert pet == {"species": "dog", "default_name": "Bella"}
    assert len(shelter.SHELTER_INVENTORY["dog"]) == 0


def test_adopt_one_raises_when_species_empty():
    with pytest.raises(RuntimeError):
        shelter.adopt_one("dragon")


def test_adopt_one_and_another_raises():
    shelter.adopt_one("bunny")
    with pytest.raises(RuntimeError):
        shelter.adopt_one("bunny")


def test_return_one_adds_pet_back_to_inventory():
    shelter.adopt_one("parrot")
    assert shelter.has_available("parrot") is False
    shelter.return_one("parrot", "Kiwi")
    assert shelter.has_available("parrot") is True


def test_return_one_creates_species_bucket_if_missing():
    shelter.return_one("hamster", "Nibbles")

    assert "hamster" in shelter.SHELTER_INVENTORY
    assert len(shelter.SHELTER_INVENTORY["hamster"]) == 1
    assert shelter.SHELTER_INVENTORY["hamster"][0]["default_name"] == "Nibbles"


def test_snapshot_returns_copy_not_original():
    snap = shelter.snapshot()
    snap["parrot"].append({"species": "parrot", "default_name": "Fake"})

    assert len(snap["parrot"]) == 2
    assert len(shelter.SHELTER_INVENTORY["parrot"]) == 1
    assert shelter.SHELTER_INVENTORY["parrot"][0]["default_name"] == "Sunny"