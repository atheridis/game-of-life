from setuptools import setup, find_packages

setup(
    name="game_of_life",
    version="0.0.1",
    author="Georgios Atheridis",
    author_email="atheridis@tutamail.com",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "gameoflife=game_of_life.main:main",
        ],
    },
    package_data={
        "game_of_life": ["data/*.json"],
    },
    install_requires=[
        "pygame",
    ],
)
