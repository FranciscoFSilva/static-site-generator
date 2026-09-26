# src/main.py

from pathlib import Path
import shutil


def from_static_to_public() -> None:
    static = Path(".").absolute() / Path("static")
    public = Path(".").absolute() / Path("public")
    shutil.rmtree(public)
    shutil.copytree(static, public)


def main() -> None:
    from_static_to_public()


main()
