all_targets=src/led/ tests/ deploy/

install:
	pip install .
	pip install .[development]
	pip install .[micropython_deploy]
	pip install .[format]
	pip install .[lint]
	pip install .[test]

lint:
	black $(all_targets)
	ruff check $(all_targets)
	mypy $(all_targets)

test:
	pytest tests 

all: lint test

deploy-cleanup-all:
	mpremote run deploy/cleanup.py

partial-deploy-warning:
	@echo ------------------------------------------------
	@echo "WARNING! Deployed only code files; cleanup and" 
	@echo "run full deploy in case of dirty files"
	@echo ------------------------------------------------

deploy-data-dir:
	deploy/safe_putdir.sh data

deploy-python-dummies: 
	mpremote fs cp -r python-dummies/* ":"

deploy-code:
	deploy/safe_rmdir.sh led
	mpremote fs cp -r src/* ":"

deploy-dev: \
	deploy-code
	@make partial-deploy-warning
	mpremote reset

deploy-full: \
	deploy-cleanup-all \
	deploy-python-dummies \
	deploy-code \
	mpremote reset

 