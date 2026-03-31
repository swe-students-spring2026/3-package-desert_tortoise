from desert_tortoise import Bunny, Cat, Dog, Parrot, Tortoise, shelter



def demo_pet(pet, food: str, amount: int, toy: str, sleep_time: int) -> None:
    def print_status(pet_obj):
        status = pet_obj.status()
        print("\nStatus:")
        for k, v in status.items():
            if k != "ascii_art":
                print(f"  {k}: {v}")
        print("\nPet:")
        print(status["ascii_art"])
        return status

    print("=" * 60)
    print(f"Adopted {pet.species}: {pet.name}")

    status = print_status(pet)

    print(f"\nFeeding {pet.name} with {food} x{amount}...")
    pet.feed(food, amount)
    status = print_status(pet)

    print(f"\nPlaying with {pet.name} using {toy}...")
    pet.play(toy)
    status = print_status(pet)

    print(f"\nPutting {pet.name} to sleep for {sleep_time}...")
    pet.sleep(sleep_time)
    status = print_status(pet)


def main() -> None:
    print("Welcome to the Digital Pet Package Example!\n")

    print("Initial shelter snapshot:")
    print(shelter.snapshot())
    print()

    print("Shelter availability:")
    for species in ["parrot", "bunny", "tortoise", "cat", "dog"]:
        print(f"{species}: {shelter.has_available(species)}")
    print()

    # all pets adoptation
    parrot = Parrot.adopt("Sunny")
    bunny = Bunny.adopt("Clover")
    tortoise = Tortoise.adopt("Ruby")
    cat = Cat.adopt("Mochi")
    dog = Dog.adopt("Bella")

    # all pets demo on eating, playing, and sleeping
    demo_pet(parrot, "seeds", 2, "mirror", 2)
    demo_pet(bunny, "carrots", 2, "tunnel", 2)
    demo_pet(tortoise, "greens", 2, "foraging puzzle", 2)
    demo_pet(cat, "fish", 2, "feather", 2)
    demo_pet(dog, "meat", 2, "ball", 2)

    print("\n" + "=" * 60)
    print("Demonstrating edge-case behavior:")

    # Reuse the already adopted pets so the example does not fail when shelter inventory is empty.
    stress_dog = dog
    stress_dog.hunger = 90
    stress_dog.exhaustion = 90
    stress_dog.health = 50

    print("\nBefore stressful play:")
    status = stress_dog.status()
    print("\nStatus:")
    for k, v in status.items():
        if k != "ascii_art":
            print(f"  {k}: {v}")
    print("\nPet:")
    print(status["ascii_art"])

    print("\nPlaying with Bella using ball...")
    stress_dog.play("ball")
    print("After stressful play (health may decrease):")
    status = stress_dog.status()
    print("\nStatus:")
    for k, v in status.items():
        if k != "ascii_art":
            print(f"  {k}: {v}")
    print("\nPet:")
    print(status["ascii_art"])

    shelter_tortoise = tortoise
    shelter_tortoise.hunger = 100
    shelter_tortoise._check_runaway()

    print("\nAfter forcing Ruby to critical hunger:")
    status = shelter_tortoise.status()
    print("\nStatus:")
    for k, v in status.items():
        if k != "ascii_art":
            print(f"  {k}: {v}")
    print("\nPet:")
    print(status["ascii_art"])

    print("\nUpdated shelter snapshot after return:")
    print(shelter.snapshot())

    print("\nFinal shelter snapshot:")
    print(shelter.snapshot())


if __name__ == "__main__":
    main()