import argparse
import json
import os
import time

import requests

BASE_URL = "https://baike.baidu.com/cms/home/eventsOnHistory/{}.json"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}


def fetch_json(session, url, retries=3):
    last_error = None
    for attempt in range(retries):
        try:
            response = session.get(url, headers=HEADERS, timeout=30)
            response.raise_for_status()
            return response.json()
        except (requests.RequestException, ValueError) as exc:
            last_error = exc
            if attempt < retries - 1:
                time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"{url} -> {last_error}")


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parser = argparse.ArgumentParser(description="抓取百度百科『历史上的今天』JSON")
    parser.add_argument("--output-dir", default=os.path.join(script_dir, "BaiduJson"),
                        help="JSON 保存目录（默认: 脚本同级 BaiduJson）")
    parser.add_argument("--month", type=int, choices=range(1, 13), help="只抓取指定月份")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    months = [args.month] if args.month else list(range(1, 13))
    failed = []

    with requests.Session() as session:
        for month in months:
            url = BASE_URL.format(f"{month:02d}")
            file_path = os.path.join(args.output_dir, f"{month}月.json")
            try:
                data = fetch_json(session, url)
            except RuntimeError as exc:
                print(f"失败 {exc}")
                failed.append(month)
                continue
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            print(f"已保存 {file_path}")
            time.sleep(0.5)

    print(f"完成: 成功 {len(months) - len(failed)} 个月, 失败 {len(failed)} 个")
    if failed:
        print(f"失败月份: {failed}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
