run:
	- python ./src/main.py

venv:
	- python -m venv .venv

install:
	- pip install -r requirements.txt

pre-run:
	- pre-commit run --all-files

pre-install:
	- pip install pre-commit
	- pre-commit install
