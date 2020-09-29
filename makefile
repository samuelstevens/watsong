all: types format lint

types: FORCE
	mypy --strict -p watsong

format: FORCE
	isort watsong
	black watsong

lint: FORCE
	flake8 watsong

FORCE: