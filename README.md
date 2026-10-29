# EOS-EXIF-Join

Application to join EOS and EXIF data files for image processing

UI made with PyQt6
exe generated using Pyinstaller

## Installation

Install the [uv](https://docs.astral.sh/uv/) package manager then:

```sh
uv sync
```

## Running

Use join_data.exe or

```sh
uv run python -m gui
```

## Development

Git hooks are managed with [prek](https://prek.j178.dev). Install them with:

```sh
uv run prek install
```

## Building

Builds are done automatically with GitHub Actions when pushing a tag with a semantic
version formats like `vN.N.N` or `vN.N.N-rcN`
