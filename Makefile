PYTHON ?= python
PIP ?= $(PYTHON) -m pip
COVERAGE ?= coverage
PYCODESTYLE ?= pycodestyle
FLAKE8 ?= flake8


help: Makefile
	@echo
	@echo " Choose a command run in Warehouse:"
	@echo
	@sed -n 's/^##//p' $< | column -t -s ':' |  sed -e 's/^/ /'
	@echo


## config: Install dependencies.
config:
	$(PIP) install pycodestyle
	$(PIP) install coverage
	$(PIP) install flake8
	$(PIP) install flake8-comprehensions
	$(PIP) install flake8-eradicate
	$(PIP) install flake8-todo
	$(PIP) install -r requirements.txt


## lint-pycodestyle: PyCode Style Lint
lint-pycodestyle:
	@echo "\n>> ============= Pycodestyle Linting ============= <<"
	@find app -type f -name \*.py | while read file; do echo "$$file" && $(PYCODESTYLE) --config=./pycodestyle --first "$$file" || exit 1; done


## lint-flake8: Flake8 Lint.
lint-flake8:
	@echo "\n>> ============= Flake8 Linting ============= <<"
	@find app -type f -name \*.py | while read file; do echo "$$file" && $(FLAKE8) --config=flake8.ini "$$file" || exit 1; done


## lint: Lint The Code.
lint: lint-pycodestyle lint-flake8
	@echo "\n>> ============= All linting cases passed! ============= <<"


## test: Run Test Cases.
test:
	@echo "\n>> ============= Run Test Cases ============= <<"
	$(PYTHON) manage.py test


## migration: Create DB Migration Files.
migration:
	@echo "\n>> ============= Make Migrations ============= <<"
	$(PYTHON) manage.py makemigrations


## migrate: Migrate Database.
migrate:
	@echo "\n>> ============= Migrate ============= <<"
	$(PYTHON) manage.py migrate


## run: Run Server.
run:
	@echo "\n>> ============= Run Server ============= <<"
	$(PYTHON) manage.py runserver


## coverage: Get test coverage.
coverage:
	@echo "\n>> ============= Get test coverage ============= <<"
	$(COVERAGE) run --source='app' manage.py test app
	$(COVERAGE) report -m
	$(COVERAGE) html


## create-env: Create .env file.
create-env:
	@echo "\n>> ============= Create .env file ============= <<"
	cp .env.example .env


## makemessages: Make translation files.
makemessages:
	@echo "\n>> ============= Make translation files ============= <<"
	$(PYTHON) manage.py makemessages


## outdated-pkg: Show outdated python packages
outdated-pkg:
	@echo "\n>> ============= List Outdated Packages ============= <<"
	$(PIP) list --outdated


## ci: Run all CI tests.
ci: test coverage lint outdated-pkg
	@echo "\n>> ============= All quality checks passed ============= <<"


.PHONY: help