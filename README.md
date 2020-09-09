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

> I'm not completely sure how to activate environment variables in Windows. At a minimum, you can copy-paste the script contents into a shell. Does anyone know?

```sh
# somehow run ./envs/dev-windows.bat
```

3. Run application

```sh
flask run
```

4. Open application in browser

[https://localhost:5000/jukebox](https://localhost:5000/jukebox)
