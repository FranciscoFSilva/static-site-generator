# src/main.py

import shutil
from pathlib import Path

import sys
from md_parser import extract_title
from md_to_html import markdown_to_html_node


def from_static_to_public() -> None:
    static = Path(".").absolute() / Path("static")
    public = Path(".").absolute() / Path("docs")
    Path.mkdir(public, exist_ok=True)
    shutil.rmtree(public)
    shutil.copytree(static, public)


def generate_page(
    from_path: Path, template_path: Path, dest_path: Path, base_path: str
):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r", encoding="utf-8") as file:
        markdown = file.read()

    with open(template_path, "r", encoding="utf-8") as file:
        html_template = file.read()

    nodes = markdown_to_html_node(markdown)
    html = nodes.to_html()

    title = extract_title(markdown)

    html_template = html_template.replace("{{ Title }}", title).replace(
        "{{ Content }}", html
    )

    html_template = html_template.replace('href="/', f'href="{base_path}').replace(
        'src="/', f'src="{base_path}'
    )

    Path.mkdir(dest_path.parent, parents=True, exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as file:
        file.write(html_template)


def main() -> None:
    basepath = "/" if len(sys.argv) < 2 else sys.argv[1]
    from_static_to_public()
    from_path = Path(".").absolute() / Path("content")
    template_path = Path(".").absolute() / Path("template.html")
    print(template_path)
    print()
    for dirpath, _, filenames in from_path.walk():
        for filename in filenames:
            filepath = dirpath / filename
            if filepath.suffix == ".md":
                common_path = filepath.relative_to(from_path)
                dest_path = (
                    Path(".").absolute()
                    / Path("docs")
                    / common_path.with_suffix(".html")
                )
                generate_page(filepath, template_path, dest_path, basepath)


main()
