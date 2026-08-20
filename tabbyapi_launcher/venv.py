import os
import sys
from pathlib import Path


def activate_venv(environ: dict[str, str], venv_path: Path) -> Path:
    venv_path = venv_path.resolve()


    if sys.platform == "win32":
        venv_bin = venv_path / "Scripts"
        venv_python = venv_bin / "python.exe"
    else:
        venv_bin = venv_path / "bin"
        venv_python = venv_bin / "python"

    # prepare envs
    environ["VIRTUAL_ENV"] = str(venv_path)
    environ["PATH"] = f"{venv_bin}{os.pathsep}{environ.get('PATH', '')}"
    environ.pop("PYTHONHOME", None)

    return venv_python
