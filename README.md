# Virtual environment

## Create the vitual environment

```bash
make venv

ln -s .venv/bin/activate ./activate #mac and linux
```

## Activate the virtual environment

```bash
source ./activate #mac and linux
```

## Deactivate the virtual environment

```bash
deactivate
```

# Package installation

```bash
make install
```

## After package installation

If you install any package needed for your features don't forget to add it to requierements.txt.

```bash
pip install package
pip freeze > requirements.txt
```

# Pre-commit

## Install pre-commit

```bash
pre-commit install
```

## Run pre-commit

```bash
pre-commit run -a
```
