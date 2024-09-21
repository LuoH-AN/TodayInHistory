import os
import requests
import time
from opencc import OpenCC

def createSaveDirectory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def getDaysInMonth(month):
    if month == 2:
        return 29
    elif month in [4, 6, 9, 11]:
        return 30
    else:
        return 31

def fetchAndSavePage(url, filePath):
    cc = OpenCC('t2s')
    try:
        response = requests.get(url)
        response.raise_for_status()
        simplified_text = cc.convert(response.text)
        with open(filePath, 'w', encoding='utf-8') as file:
            file.write(simplified_text)
        print(f"保存 {filePath}")
        return True
    except requests.RequestException as e:
        print(f"错误 {url}: {e}")
        return False

def main():
    saveDir = "WikiHTML"
    createSaveDirectory(saveDir)
    failedUrls = []
    for month in range(1, 13):
        daysInMonth = getDaysInMonth(month)
        for day in range(1, daysInMonth + 1):
            url = f"https://zh.wikipedia.org/wiki/{month}月{day}日"
            fileName = f"{month}月{day}日.html"
            filePath = os.path.join(saveDir, fileName)
            if not fetchAndSavePage(url, filePath):
                failedUrls.append(url)
    if failedUrls:
        print("请求失败页面")
        for url in failedUrls:
            fileName = url.split('/')[-1] + ".html"
            filePath = os.path.join(saveDir, fileName)
            fetchAndSavePage(url, filePath)

if __name__ == "__main__":
    main()