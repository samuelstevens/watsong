all: types format lint test

types: FORCE
	mypy --strict -p watsong

format: FORCE
	isort watsong
	black watsong

lint: FORCE
	flake8 watsong

test: FORCE
	python -m unittest
	pytest

coverage: FORCE
	coverage run --include "watsong/*" -m pytest
	coverage html
	open htmlcov/index.html

FORCE: