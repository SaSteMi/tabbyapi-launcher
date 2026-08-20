import os
from shutil import which
import subprocess
import sys
from pathlib import Path
from .venv import activate_venv
from .utils import make_path_link

VENV_PATH = Path("venv")
START_SCRIPT_PATH = Path("start.py")

# Creates a venv if it doesn't exist and runs the start script for requirements upgrades
# This is intended for users who want to start the API and have everything upgraded and installed

has_uv = which("uv") is not None

environ = os.environ.copy()

# Don't create a venv if a conda environment is active

if os.getenv("CONDA_PREFIX"):
    print("It looks like you're in a conda environment. Skipping venv check.")
    python_executable = Path(sys.executable)

else:
    if not VENV_PATH.exists():
        print("Venv doesn't exist! Creating one for you.")

        if has_uv:
            print("It looks like you're using uv. Running appropriate commands.")
            subprocess.run(
                ["uv", "venv", VENV_PATH, "-p", "3.12"],
                check=True,
            )
        else:
            subprocess.run(
                [sys.executable, "-m", "venv", VENV_PATH],
                check=True,
            )

        start_options = Path("start_options.json")

        if start_options.exists():
            print("Removing old {start_options}")
            start_options.unlink()

        print()

    python_executable = activate_venv(environ, VENV_PATH)

print(f"Launching TabbyAPI repo at {make_path_link(Path.cwd())}: Executing {make_path_link(START_SCRIPT_PATH)} with {make_path_link(python_executable.relative_to(Path.cwd()))}\n")

# Check critical files

for file in (python_executable, START_SCRIPT_PATH):
    if not file.is_file():
        raise FileNotFoundError(
            f"{make_path_link(file.resolve())} could not be found"
        )

# Call the TabbyAPI start script and pass args

sys.exit(
    subprocess.run(
        [python_executable, START_SCRIPT_PATH] + sys.argv[1:],
        env=environ,
        check=True,
    ).returncode
)
