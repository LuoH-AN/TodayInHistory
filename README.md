# ⌛ TodayInHistory | 历史上的今天

数据来源：
- [Wikipedia](https://zh.wikipedia.org/)
- [Baidu](https://baike.baidu.com/calendar)

# 📖 前言

在 GitHub 上看到了一个关于 **历史上的今天**的项目，但该仓库的数据收集于 2020 年，且没有进一步更新。受此启发，我决定进行自己的数据收集

本仓库正是在这个想法下诞生的

## Wiki

### 🛠️ 过程

*所有数据处理均使用 Python 完成*

- 将 `https://zh.wikipedia.org/wiki/{month}月{day}日` 页面以 HTML 格式保存到本地
  - 保存下来的页面是繁体中文，我使用了 `OpenCC` 将其转换为简体中文
- 对 HTML 进行处理，将其转换为 TXT 文件
  - 过程中发现一些词汇的表述不统一，例如“**大事迹**”在不同页面可能出现“**大事纪**”或“**大事记**”(~~气人😠~~)
- 将 TXT 文件转换为 JSON

### 🚀 使用

本仓库的数据收集于 *2024 年 9 月 21 日*

- **方法一**：依次运行 `Wiki/saveWikiHTML.py`、`Wiki/genWikiTXT.py` 和 `Wiki/genWikiJSON.py`，便可生成 `Wiki/WikiJSON`
- **方法二**：直接使用本仓库 `Wiki/WikiJSON` 文件夹下的现成数据

## Baidu

### 🛠️ 过程

*所有数据处理均使用 Python 完成*

- 将 `https://baike.baidu.com/calendar` 页面以 HTML 格式保存到本地
  - 可是并无任何数据
- 经过一番寻找在 `https://bkssl.bdimg.com/static/wiki-home/eventsOnHistory/eventsOnHistory_2e7e121.js` 中找到了源JSON

### 🚀 使用

- **方法一**：运行 `Biadu/saveBaiduJSON.py`，便可生成 `Baidu/BaiduJSON`
- **方法二**：直接使用本仓库 `Baidu/BaiduJSON` 文件夹下的现成数据

# ✍️ 后语

- 对于JSON的结构正在考虑更改
- 其他内容待补充 😑