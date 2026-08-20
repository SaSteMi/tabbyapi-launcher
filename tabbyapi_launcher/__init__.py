"""Launcher for TabbyAPI."""

import os
import subprocess
import sys
from pathlib import Path
from platformdirs import PlatformDirs
import runpy

from .utils import make_path_link



DIRS = PlatformDirs(
    appname="tabbyapi-launcher",
    appauthor=False,
    roaming=True,
    ensure_exists=True,
)

CONFIG_PATH = DIRS.user_config_path / "config.json"
DIR_PATH = Path(__file__).resolve().parent

from .config import load_state, save_state


def clone_repo(repo_path: Path) -> None:
    """Clone the tabbyAPI repository to the specified directory."""

    print()
    
    try:
        subprocess.run(
            [
                "git",
                "clone",
                "--depth", "1",
                "https://github.com/theroyallab/tabbyAPI.git",
                repo_path,
            ],
            check=True,
        )
        print("\n✓ Repository cloned successfully!\n")
    except subprocess.CalledProcessError as error:
        print(f"\n✗ Failed to clone repository", file=sys.stderr)
        print("Please ensure git is working correctly and you have internet access.", file=sys.stderr)
        raise
    except FileNotFoundError:
        print("\n✗ Git is not installed or not in PATH.", file=sys.stderr)
        print("Please install git and try again.", file=sys.stderr)
        raise





def check_directory(path_string: str) -> Path:
    """Checks whether the specified directory is valid."""
    path_string = path_string.strip()

    if not path_string:
        raise ValueError("Path must not be empty")

    path = Path(path_string).expanduser()

    if not path.is_absolute():
        raise ValueError(
            f"Path must be absolute: {make_path_link(path)}"
        )

    if path == DIRS.user_config_path or path == CONFIG_PATH:
        raise ValueError(
            f"Path can't be config directory: {make_path_link(path)}"
        )

    if path.exists():

        if not path.is_dir():
            raise NotADirectoryError(
                f"Already exists and is no directory: {make_path_link(path)}"
            )
        
        if any(path.iterdir()):
            raise FileExistsError(
                f"Directory must be empty: {make_path_link(path)}"
            )

    return path


def main():
    """Main entry point for the tabbyapi launcher."""

    print(f"Loading launcher config from {make_path_link(CONFIG_PATH)}")
    state = load_state()
    repo_dir = state["repo_dir"]

    if repo_dir:
        repo_path = Path(repo_dir)
    else:
        print("\n(install location not yet set)")
        repo_path = DIRS.user_data_path / "tabbyAPI"
        while True:
            user_input = input(f"Choose install location for TabbyAPI GitHub repository [{make_path_link(repo_path)}]: ")

            if not user_input:
                break

            try:
                repo_path = check_directory(user_input)
                break

            except (ValueError, NotADirectoryError, FileExistsError, OSError) as error:
                print(f"Invalid: {error}\n")

        state["repo_dir"] = str(repo_path)
        print(f"✓ Saving {make_path_link(repo_path)} to {make_path_link(CONFIG_PATH)}")
        save_state(state)
    
    # Clone the repository if it doesn't exist
    if not repo_path.exists() or not any(repo_path.iterdir()):
        repo_path.mkdir(parents=True, exist_ok=True)
        clone_repo(repo_path)

    # change directory to TabbyAPI repo
    os.chdir(repo_path)

    # run launcher start script
    try:
        runpy.run_module("tabbyapi_launcher.start", alter_sys=True)
    except FileNotFoundError as error:
        print(f"✗ TabbyAPI could not be started", file=sys.stderr)
        print(f"The repository at {make_path_link(repo_path)} may be corrupted. Try deleting it and running again.\n", file=sys.stderr)
        raise
    except KeyboardInterrupt:
        sys.exit(130)
