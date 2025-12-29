# Variables
PYTHON := poetry run
POETRY := poetry
PRE_COMMIT := poetry run pre-commit
PROJECT_NAME := src
PYTHON_FILES := $(PROJECT_NAME) features/steps

# Colors for terminal output
BLUE := \033[1;34m
GREEN := \033[1;32m
RED := \033[1;31m
YELLOW := \033[1;33m
NC := \033[0m # No Color

.PHONY: help
help: ## Show this help message
	@echo 'Usage:'
	@echo "${BLUE}make${NC} ${GREEN}<target>${NC}"
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z\-_0-9]+:.*?## / {printf "  ${BLUE}%-20s${NC} %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: setup
setup: ## Setup project pre-requisites
	@echo "${BLUE}Setup project pre-requisites...${NC}"
	@echo "${GREEN}Installing poetry...${NC}"
	pip install poetry

.PHONY: install
install: ## Install project dependencies
	@echo "${BLUE}Installing project dependencies...${NC}"
	$(POETRY) install
	$(PRE_COMMIT) install

.PHONY: install-dev
install-dev: ## Install project dependencies with dev extras
	@echo "${BLUE}Installing project dependencies...${NC}"
	$(POETRY) install --with dev
	$(PRE_COMMIT) install

.PHONY: update
update: ## Update dependencies to their latest versions
	@echo "${BLUE}Updating dependencies...${NC}"
	$(POETRY) update

.PHONY: clean
clean: ## Remove build artifacts and cache directories
	@echo "${BLUE}Cleaning project...${NC}"
	rm -rf dist/
	rm -rf build/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .mypy_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

.PHONY: format
format: ## Format code using black
	@echo "${BLUE}Formatting code...${NC}"
	$(PYTHON) black --config pyproject.toml $(PYTHON_FILES)

.PHONY: lint
lint: ## Run all linters
	@echo "${BLUE}Running linters...${NC}"
	$(PYTHON) ruff check --config pyproject.toml $(PYTHON_FILES)

.PHONY: behave
behave: ## Run BDD tests with behave
	@echo "${BLUE}Running BDD tests...${NC}"
	$(PYTHON) behave

.PHONY: test
test: ## Run unit tests with pytest
	@echo "${BLUE}Running unit tests...${NC}"
	$(PYTHON) pytest src/tests/ -v

.PHONY: test-cov
test-cov: ## Run tests with coverage
	@echo "${BLUE}Running tests with coverage...${NC}"
	$(PYTHON) pytest src/tests/ -v --cov=src --cov-report=html

.PHONY: run
run: ## Run the application
	@echo "${BLUE}Starting application...${NC}"
	$(PYTHON) python manage.py

.PHONY: migrate
migrate: ## Run database migrations
	@echo "${BLUE}Running migrations...${NC}"
	$(PYTHON) alembic upgrade head

.PHONY: migrate-new
migrate-new: ## Create a new migration
	@echo "${BLUE}Creating new migration...${NC}"
	$(PYTHON) alembic revision --autogenerate -m "$(message)"

.PHONY: pre-commit
pre-commit: ## Run pre-commit hooks
	@echo "${BLUE}Running pre-commit hooks...${NC}"
	$(PRE_COMMIT) run --all-files

.PHONY: check
check: lint test ## Run all checks (linting and tests)

.PHONY: docker-up
docker-up: ## Start Docker containers
	@echo "${BLUE}Starting Docker containers...${NC}"
	docker-compose up -d

.PHONY: docker-down
docker-down: ## Stop Docker containers
	@echo "${BLUE}Stopping Docker containers...${NC}"
	docker-compose down

.PHONY: docs
docs: ## Generate PlantUML diagrams
	@echo "${BLUE}Generating documentation diagrams...${NC}"
	plantuml -tsvg docs/*.puml || echo "PlantUML not installed. Install with: apt install plantuml"

.DEFAULT_GOAL := help
