import argparse
import os
import re

from bs4 import BeautifulSoup

SECTION_ALIASES = {
    "大事记": "1",
    "大事迹": "1",
    "大事纪": "1",
    "出生": "2",
    "逝世": "3",
}


def collect_li_text(li):
    parts = []
    for child in li.children:
        name = getattr(child, "name", None)
        if name in ("sup", "ul", "ol"):
            continue
        if isinstance(child, str):
            parts.append(child)
        else:
            parts.append(child.get_text(" ", strip=True))
    return re.sub(r"\s+", " ", "".join(parts)).strip()


def extract_section(heading):
    container = heading.parent if heading.parent.name == "div" else heading
    items = []
    for sibling in container.find_next_siblings():
        if sibling.find("h2"):
            break
        for li in sibling.find_all("li"):
            text = collect_li_text(li)
            if text:
                items.append(text)
    return items


def parse_html(html):
    soup = BeautifulSoup(html, "html.parser")
    sections = {}
    for h2 in soup.find_all("h2"):
        folder = SECTION_ALIASES.get(h2.get_text(strip=True))
        if folder and folder not in sections:
            sections[folder] = extract_section(h2)
    return sections


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parser = argparse.ArgumentParser(description="将维基百科 HTML 转换为分节 TXT")
    parser.add_argument("--input-dir", default=os.path.join(script_dir, "WikiHTML"),
                        help="HTML 目录（默认: 脚本同级 WikiHTML）")
    parser.add_argument("--output-dir", default=os.path.join(script_dir, "WikiTXT"),
                        help="TXT 输出目录（默认: 脚本同级 WikiTXT）")
    args = parser.parse_args()

    if not os.path.isdir(args.input_dir):
        raise SystemExit(f"输入目录不存在: {args.input_dir}，请先运行 saveWikiHTML.py")

    processed = 0
    for file_name in sorted(os.listdir(args.input_dir)):
        if not file_name.endswith(".html"):
            continue
        with open(os.path.join(args.input_dir, file_name), "r", encoding="utf-8") as file:
            html = file.read()
        sections = parse_html(html)
        file_stem = os.path.splitext(file_name)[0]
        for folder, items in sections.items():
            section_dir = os.path.join(args.output_dir, folder)
            os.makedirs(section_dir, exist_ok=True)
            with open(os.path.join(section_dir, f"{file_stem}.txt"), "w", encoding="utf-8") as out:
                out.write("\n".join(items) + "\n")
        processed += 1
        print(f"已处理 {file_name} ({processed})")

    print(f"完成: 共处理 {processed} 个 HTML 文件")


if __name__ == "__main__":
    main()
