from .game_of_life import GameOfLife
import os
import shutil
import sys


def configs():
    if os.name == "posix":
        if "XDG_CONFIG_HOME" in os.environ:
            CONFIG_PATH = os.path.join(os.environ["XDG_CONFIG_HOME"], "game-of-life")
        else:
            CONFIG_PATH = os.path.join(os.environ["HOME"], ".config/game-of-life")
    elif os.name == "nt":
        if "APPDATA" in os.environ:
            CONFIG_PATH = os.path.join(os.environ["APPDATA"], "game-of-life")
        else:
            print(
                "APPDATA is not set, something must be very wrong.",
                file=sys.stderr,
            )
            sys.exit(1)
    else:
        print("Your OS is not supported", file=sys.stderr)

    os.makedirs(CONFIG_PATH, exist_ok=True)
    SAVE_PATH = os.path.join(CONFIG_PATH, "save.json")
    SETTINGS_PATH = os.path.join(CONFIG_PATH, "settings.json")

    if not os.path.exists(os.path.join(CONFIG_PATH, "save.json")):
        shutil.copyfile(
            os.path.join(os.path.dirname(os.path.realpath(__file__)), "data/save.json"),
            SAVE_PATH,
        )
    if not os.path.exists(os.path.join(CONFIG_PATH, "settings.json")):
        shutil.copyfile(
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)), "data/settings.json"
            ),
            SETTINGS_PATH,
        )
    return SAVE_PATH, SETTINGS_PATH


def main():
    save_path, settings_path = configs()
    GameOfLife.fromjsonfile(settings_path, save_path).run()


if __name__ == "__main__":
    main()
