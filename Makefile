venv:
	- python -m venv .venv

install:
	- pip install -r requirements.txt

run:
	- python main.py

pre-run:
	- pre-commit run --all-files

docs:
	- pdoc src -o docs

pre-install:
	- pip install pre-commit
	- pre-commit install
