import os
import requests
import json

def createSaveDirectory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def fetchAndSavePage(url, filePath):
    try:
        response = requests.get(url)
        response.raise_for_status()
        json_data = response.json()
        with open(filePath, 'w', encoding='utf-8') as file:
            json.dump(json_data, file, ensure_ascii=False, indent=4)
        print(f"保存 {filePath}")
        return True
    except requests.RequestException as e:
        print(f"错误 {url}: {e}")
        return False
    except json.JSONDecodeError:
        print(f"解析JSON失败 {url}")
        return False

def main():
    saveDir = "BaiduJson"
    createSaveDirectory(saveDir)
    failedUrls = []
    urlTemplate = "https://baike.baidu.com/cms/home/eventsOnHistory/{month:02d}.json"
    for month in range(1, 13):
        filePath = os.path.join(saveDir, f"{month}月.json")
        if not fetchAndSavePage(urlTemplate.format(month=month), filePath):
            failedUrls.append(month)
    if failedUrls:
        print("请求失败页面")
        for month in failedUrls:
            filePath = os.path.join(saveDir, f"{month}月.json")
            fetchAndSavePage(urlTemplate.format(month=month), filePath)

if __name__ == "__main__":
    main()