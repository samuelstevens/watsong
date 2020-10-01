all: types format lint test

types: FORCE
	mypy --strict -p watsong

format: FORCE
	isort watsong
	black watsong

lint: FORCE
	flake8 watsong

test:
	python -m unittest

FORCE: