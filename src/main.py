# src/main.py

from md_parser import extract_title
from md_to_html import markdown_to_html_node
from pathlib import Path
import shutil


def from_static_to_public() -> None:
    static = Path(".").absolute() / Path("static")
    public = Path(".").absolute() / Path("public")
    shutil.rmtree(public)
    shutil.copytree(static, public)

def generate_page(from_path: Path, template_path: Path, dest_path: Path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r", encoding='utf-8') as file:
        markdown = file.read()

    with open(template_path, "r", encoding='utf-8') as file:
        html_template = file.read()

    nodes = markdown_to_html_node(markdown)
    html = nodes.to_html()

    title = extract_title(markdown)

    html_template = html_template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    with open(dest_path, "w", encoding='utf-8') as file:
        file.write(html_template)

def main() -> None:
    from_static_to_public()
    from_path = Path('.').absolute() / Path('content') / Path('index.md')
    template_path = Path('.').absolute() / Path('template.html')
    dest_path = Path('.').absolute() / Path('public') / Path('index.html')
    generate_page(from_path, template_path, dest_path)


main()
