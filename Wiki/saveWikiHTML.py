import argparse
import os
import time

import requests

BASE_URL = "https://zh.wikipedia.org/zh-cn/{}月{}日"
HEADERS = {
    "User-Agent": "TodayInHistory-DataCollector/1.0 (open-source data update script)"
}


def get_days_in_month(month):
    if month == 2:
        return 29
    if month in (4, 6, 9, 11):
        return 30
    return 31


def fetch_page(session, url, retries=3):
    last_error = None
    for attempt in range(retries):
        try:
            response = session.get(url, headers=HEADERS, timeout=30)
            response.raise_for_status()
            return response.text
        except requests.RequestException as exc:
            last_error = exc
            if attempt < retries - 1:
                time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"{url} -> {last_error}")


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parser = argparse.ArgumentParser(description="抓取维基百科『历史上的今天』页面（zh-cn 简体）")
    parser.add_argument("--output-dir", default=os.path.join(script_dir, "WikiHTML"),
                        help="HTML 保存目录（默认: 脚本同级 WikiHTML）")
    parser.add_argument("--month", type=int, choices=range(1, 13), help="只抓取指定月份")
    parser.add_argument("--day", type=int, help="只抓取指定日期（需与 --month 同时使用）")
    parser.add_argument("--delay", type=float, default=0.3, help="相邻请求间隔秒数")
    args = parser.parse_args()

    if args.day and not args.month:
        parser.error("--day 需要与 --month 同时使用")
    if args.day and args.day > get_days_in_month(args.month):
        parser.error(f"{args.month}月没有{args.day}日")

    os.makedirs(args.output_dir, exist_ok=True)
    months = [args.month] if args.month else list(range(1, 13))
    failed = []
    saved = 0

    with requests.Session() as session:
        for month in months:
            day_start = args.day if (args.day and args.month) else 1
            day_end = args.day if (args.day and args.month) else get_days_in_month(month)
            for day in range(day_start, day_end + 1):
                url = BASE_URL.format(month, day)
                file_path = os.path.join(args.output_dir, f"{month}月{day}日.html")
                try:
                    html = fetch_page(session, url)
                except RuntimeError as exc:
                    print(f"失败 {exc}")
                    failed.append(url)
                    continue
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(html)
                saved += 1
                print(f"[{saved}] 已保存 {file_path}")
                time.sleep(args.delay)

    print(f"完成: 成功 {saved} 页, 失败 {len(failed)} 页")
    if failed:
        for url in failed:
            print(f"失败页面: {url}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
