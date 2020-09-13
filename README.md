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
