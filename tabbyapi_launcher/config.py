import os
from pathlib import Path
from typing import Any
import json

from . import CONFIG_PATH
from .utils import make_path_link

DEFAULT_STATE: dict[str, Any] = {
    "schema_version": 1,
    "repo_dir": None,
}

def load_state() -> dict[str, Any]:
    if not CONFIG_PATH.exists():
        return DEFAULT_STATE

    try:
        with CONFIG_PATH.open("r", encoding="utf-8") as file:
            state = json.load(file)
    except (OSError, json.JSONDecodeError) as error:
        raise RuntimeError(
            f"Error reading config file: {make_path_link(CONFIG_PATH)}"
        ) from error

    if not isinstance(state, dict):
        raise RuntimeError(f"Invalid config state: {make_path_link(CONFIG_PATH)}")

    return DEFAULT_STATE | state


def save_state(state: dict[str, Any]) -> None:
    TEMP_CONFIG_PATH = CONFIG_PATH.with_suffix(CONFIG_PATH.suffix + ".tmp")

    try:
        with TEMP_CONFIG_PATH.open("w", encoding="utf-8") as file:
            json.dump(
                state,
                file,
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
            )
            file.write("\n")
            file.flush()
            os.fsync(file.fileno())

        TEMP_CONFIG_PATH.replace(CONFIG_PATH)

    except (OSError, TypeError, ValueError) as error:
        TEMP_CONFIG_PATH.unlink(missing_ok=True)
        raise RuntimeError(
            f"Configuration could not be saved: {make_path_link(CONFIG_PATH)}"
        ) from error


def update_state(**changes: Any) -> dict[str, Any]:
    state = load_state()
    state.update(changes)
    save_state(state)
    return state
