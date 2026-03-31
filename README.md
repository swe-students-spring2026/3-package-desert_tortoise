![Python build & test](https://github.com/swe-students-spring2026/3-package-desert_tortoise/actions/workflows/build.yml/badge.svg)

# Desert Tortoise Digital Pet Package

This package was created by following Packaging Python Projects with pipenv for virtual environment and dependency management. It provides a playful ASCII-art digital pet system where users can adopt pets from a shelter, feed them, play with them, put them to sleep, and inspect their status.

## How this package was created

1. Set up project files including LICENSE, README.md, Pipfile, pyproject.toml, source package directory, and tests.
2. Implemented an abstract base class for shared pet behavior and concrete species classes.
3. Added a shared shelter module to manage species inventory and adoption/return flows.
4. Added unit tests using pytest.
5. Added GitHub Actions CI to run tests on pull requests to main for Python 3.11 and 3.12.
6. Configured package metadata in pyproject.toml.

Current high-level structure:

```text
3-package-desert_tortoise/
	|____README.md
	|____LICENSE
	|____Pipfile
	|____pyproject.toml
	|____example.py
	|____tests/
	|____desert_tortoise/
			|______init__.py
			|____pet.py
			|____parrot.py
			|____bunny.py
			|____cat.py
			|____dog.py
			|____tortoise.py
			|____shelter.py
```

## PyPI Website

[Our Package's PyPI Website](https://pypi.org/project/desert-tortoise-virtual-pet-package/)

## How to install and use this package

### Install from PyPI

```bash
pip install desert-tortoise-pet-package
```

### Local development install

```bash
git clone https://github.com/swe-students-spring2026/3-package-desert_tortoise.git
cd 3-package-desert_tortoise
pipenv install --dev
pipenv run pip install -e .
```

### Basic usage

```python
from desert_tortoise import Parrot

pet = Parrot.adopt("Kiwi")
pet.feed("seeds", 2)
pet.play("mirror")
pet.sleep(1)
print(pet.status())
```

### Full example program

The complete example that demonstrates all current pet classes is in example.py.

Run it with:

```bash
pipenv run python example.py
```

## API overview

Each pet class supports the following argument-driven functions:

1. adopt(name: str)
2. feed(food_type: str, amount: int = 1)
3. play(type_of_toy: str)
4. sleep(time: int = 5)
5. status()

Available classes exported by the package:

- Parrot
- Bunny
- Cat
- Dog
- Tortoise

Shared shelter helper module:

- shelter.has_available(species)
- shelter.adopt_one(species)
- shelter.return_one(species, default_name)
- shelter.snapshot()

## How to run unit tests

```bash
pipenv install --dev
pipenv run pytest -q
```

Tests should not fail. Any failing test indicates behavior mismatch or a regression.

## How to build and publish

Install build tools:

```bash
pipenv install --dev build twine
```

Build distributions:

```bash
pipenv run python -m build
```

Verify package files:

```bash
tar --list -f dist/desert_tortoise_pet_package-1.0.0.tar.gz
```

Upload to TestPyPI:

```bash
pipenv run twine upload -r testpypi dist/*
```

Upload to PyPI:

```bash
pipenv run twine upload dist/*
```

When releasing a new version:

1. Delete dist directory.
2. Delete generated egg-info metadata if present.
3. Bump version in pyproject.toml.
4. Rebuild and upload again.

## Continuous integration

This repository uses GitHub Actions to run tests on pull requests into main using Python 3.11 and 3.12.

Workflow file:

- .github/workflows/build.yml

## Contribution workflow

1. Create a feature branch from main.
2. Implement changes and tests.
3. Open a pull request into main.
4. Request teammate review.
5. Merge after review and passing CI.

## Team Member

[Kara](https://github.com/cynikjinchen)
[Grace](https://github.com/grace350)
[Prabhav Jalan](https://github.com/prabhav-jalan)
[Caleb](https://github.com/calebjawharjian)
[Ginny](https://github.com/ginny1536)

## Environment variables and secret files

No environment variables or secret configuration files are required for the current implementation.

If this changes in the future, include an env.example file with dummy values and document setup steps here.

## License

MIT License. See LICENSE for details.
