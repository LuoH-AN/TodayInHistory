import argparse
import json
import os

TYPE_MAPPING = {"1": "event", "2": "birth", "3": "death"}


def format_year(year):
    return year.replace("前", "-").replace("年", "").strip()


def parse_txt(file_path, entry_type):
    entries = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line or "：" not in line:
                continue
            year, content = line.split("：", 1)
            entries.append({
                "year": format_year(year),
                "content": content.strip(),
                "type": entry_type,
            })
    return entries


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parser = argparse.ArgumentParser(description="将分节 TXT 合并为每日 JSON")
    parser.add_argument("--input-dir", default=os.path.join(script_dir, "WikiTXT"),
                        help="TXT 目录（默认: 脚本同级 WikiTXT）")
    parser.add_argument("--output-dir", default=os.path.join(script_dir, "WikiJson"),
                        help="JSON 输出目录（默认: 脚本同级 WikiJson）")
    args = parser.parse_args()

    events_dir = os.path.join(args.input_dir, "1")
    if not os.path.isdir(events_dir):
        raise SystemExit(f"输入目录不存在: {events_dir}，请先运行 genWikiTXT.py")

    os.makedirs(args.output_dir, exist_ok=True)
    for file_name in sorted(os.listdir(events_dir)):
        if not file_name.endswith(".txt"):
            continue
        entries = []
        for folder, entry_type in TYPE_MAPPING.items():
            txt_path = os.path.join(args.input_dir, folder, file_name)
            if os.path.exists(txt_path):
                entries.extend(parse_txt(txt_path, entry_type))
        base_name = file_name.replace("月", "-").replace("日.txt", "")
        out_path = os.path.join(args.output_dir, f"{base_name}.json")
        with open(out_path, "w", encoding="utf-8") as json_file:
            json.dump(entries, json_file, ensure_ascii=False, indent=4)
        print(f"完成 {out_path} ({len(entries)} 条)")

    print(f"完成: 输出目录 {args.output_dir}")


if __name__ == "__main__":
    main()
