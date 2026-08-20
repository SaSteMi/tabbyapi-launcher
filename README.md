# TabbyAPI Launcher

A minimal launcher that wrapps [TabbyAPI](https://github.com/theroyallab/tabbyAPI) into a python tool.

## Installation

Install using `[uv](https://docs.astral.sh/uv/getting-started/installation/) tool`/`pipx`:

```bash
uv tool install tabbyapi-launcher
```

## Usage

After installation, simply run:

```bash
tabbyapi
```

This will:

1. Shallow-clone the [TabbyAPI repository](https://github.com/theroyallab/tabbyAPI)
2. Prepare the venv
3. Run it

All arguments are passed through directly to the TabbyAPI startup script.

## How It Works

- Saves repository location to config file
- Executes the TabbyAPI start script [start.py](https://github.com/theroyallab/tabbyAPI/blob/main/start.py) with your arguments
- The [TabbyAPI repository](https://github.com/theroyallab/tabbyAPI) stays fully persistent and self-reliant

## Uninstall

```bash
uv tool uninstall tabbyapi
```

You may also wish to remove the cloned repository or config directory (both paths are printed out at startup).
