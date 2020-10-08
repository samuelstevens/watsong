# Watsong

## Dev Instructions

0. Create your virtual environment (optional)

```sh
python3 -m venv virtualenv
```

0. Activate your virutal environment (optional)

### macOS

```sh
. ./virtualenv/bin/activate
```

### Windows

```sh
.\virtualenv\scripts\activate
```

1. Install requirements

```sh
pip install -r requirements.txt
```

2. Activate dev environment

### macOS

```sh
. ./envs/dev-unix.sh
```

### Windows

1. Set up environment variables

```sh
.\envs\dev-windows.bat
```

3. Run application

```sh
flask run
```

4. Open application in browser

[https://localhost:5000/](https://localhost:5000/)

## Running Individual Files as Scripts

Because of the way Flask and `mypy` and all these tools work, to run a file as a script you'll need to do:

```sh
python -m watsong.spotify # or whatever
```

## Running the unit tests

## Contributing
Make sure your commits are linted with black by running
```bash
black .
```
in the top level directory.

Also run
```bash
mypy --strict -p watsong
```
to detect any issues thrown by numpy.

Finally, make sure the unit tests pass.
```bash
pytest
```
