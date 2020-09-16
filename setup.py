from distutils.core import setup

setup(
    name="watsong",
    version="1.0.0",
    packages=["watsong"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "flask",
        "spotipy",
    ],
)
