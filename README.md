# To deploy the application

To deploy the application, you can use the script deploy.sh.

**Before running the script, you need to have Docker installed on your machine.**

```bash
source deploy.sh
```

This script will build the Docker image and run the container.

A tenant can be created by the administrator. To do this, the administrator must run the following python file:

```bash
python3 add_tenant_user.py
# or depending on your python version
python add_tenant_user.py
```

This user have informations:

- email: admin@adm.adm
- password: admin
- city: Paris, 75000

# To develop on this project

## Virtual environment

To develop on this project you need to create a virtual environment. This will allow you to install packages only for this project and not for your whole system.

### Create the vitual environment

```bash
python3 -m venv venv
```

### Activate the virtual environment

```bash
source venv/bin/activate
```

### Deactivate the virtual environment

```bash
deactivate
```

### Install project packages

```bash
pip install -r requirements.txt
```

### Add a package to the project

After installing a package, you need to add it to the requirements.txt file to keep track of the project dependencies.

```bash
pip install your_package
pip freeze > requirements.txt
```

## Pre-commit

The pre-commit package is used to run some checks before committing your code. It will run the black formatter and the flake8 linter.

### Install pre-commit

```bash
pre-commit install
```
