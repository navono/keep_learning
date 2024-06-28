#* Variables
SHELL := /usr/bin/env bash
PYTHON := python
OS := $(shell python -c 'import sys; print(sys.platform)')

ifeq ($(OS),win32)
	PYTHONPATH := $(shell python -c "import os; print(os.getcwd())")
    TEST_COMMAND := set PYTHONPATH=$(PYTHONPATH) && poetry run pytest -c pyproject.toml --cov-report=html --cov=p3g_demo tests/
else
	PYTHONPATH := `pwd`
    TEST_COMMAND := PYTHONPATH=$(PYTHONPATH) poetry run pytest -c pyproject.toml --cov-report=html --cov=p3g_demo tests/
endif

#* Docker variables
IMAGE_BACKEND := fastapi_template_backend
IMAGE_BACKEND_VERSION := latest

#* All commands for backend
.PHONY: lock back-install pre-commit-install polish-codestyle formatting test check-codestyle lint docker-build docker-remove cleanup dev help

export POETRY_PYPROJECT=./backend/pyproject.toml

lock:
	cd backend && poetry lock -n && poetry export --without-hashes > requirements.txt

install:
	cd backend && poetry lock -n && poetry export --without-hashes > ./backend/requirements.txt
	cd backend && poetry install -n

pre-commit-install:
	cd backend && poetry run pre-commit install

polish-codestyle:
	cd backend && poetry run ruff format --config pyproject.toml .
	cd backend && poetry run ruff check --fix --config pyproject.toml .

formatting: polish-codestyle
format: polish-codestyle

test:
	$(TEST_COMMAND)
	cd backend && poetry run coverage-badge -o assets/images/coverage.svg -f

check-codestyle:
	cd backend && poetry run ruff format --check --config pyproject.toml .
	cd backend && poetry run ruff check --config pyproject.toml .

lint: test check-codestyle

dev:
	poetry run uvicorn backend.app.main:app --host 0.0.0.0 --port 18000 --reload --reload-dir ./backend/app

# Example: make docker-build VERSION=latest
# Example: make docker-build IMAGE=some_name VERSION=0.1.0
docker-build:
	@echo Building docker $(IMAGE_BACKEND):$(VERSION) ...
	docker build \
		-t $(IMAGE_BACKEND):$(VERSION) . \
		-f ./backend/docker/Dockerfile --no-cache

# Example: make docker-remove VERSION=latest
# Example: make docker-remove IMAGE=some_name VERSION=0.1.0
docker-remove:
	@echo Removing docker $(IMAGE_BACKEND):$(VERSION) ...
	docker rmi -f $(IMAGE_BACKEND):$(VERSION)

cleanup:
	find . | grep -E "(__pycache__|\.pyc|\.pyo$$)" | xargs rm -rf
	find . | grep -E ".DS_Store" | xargs rm -rf
	find . | grep -E ".mypy_cache" | xargs rm -rf
	find . | grep -E ".ipynb_checkpoints" | xargs rm -rf
	find . | grep -E ".pytest_cache" | xargs rm -rf
	cd backend && rm -rf build/

help:
	@echo "All commands for [backend] project:"
	@echo "lock                                      Lock the dependencies."
	@echo "install                                   Install the project dependencies."
	@echo "pre-commit-install                        Install the pre-commit hooks."
	@echo "polish-codestyle                          Format the codebase."
	@echo "formatting                                Format the codebase."
	@echo "test                                      Run the tests."
	@echo "check-codestyle                           Check the codebase for style issues."
	@echo "lint                                      Run the tests and check the codebase for style issues."
	@echo "docker-build                              Build the docker image."
	@echo "docker-remove                             Remove the docker image."
	@echo "cleanup                                   Clean the project directory."
	@echo "help                                      Display this help message."
