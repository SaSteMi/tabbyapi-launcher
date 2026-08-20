from pathlib import Path

def make_hyperlink(text: str, url: str) -> str:
    return f"\033]8;;{url}\033\\{text}\033]8;;\033\\"


def make_path_link(path: Path) -> str:
    return make_hyperlink(str(path), path.resolve().as_uri())
