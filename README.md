# ⌛ TodayInHistory | 历史上的今天

数据来源：[Wikipedia](https://zh.wikipedia.org/)

## 📖 前言

在 GitHub 上看到了 [PrintNow/TodayInHistory](https://github.com/PrintNow/TodayInHistory) 项目，但该仓库的数据收集于 2020 年，且没有进一步更新。受此启发，我决定进行自己的数据收集

本仓库正是在这个想法下诞生的

## 🛠️ 过程

*所有数据处理均使用 Python 完成*

- 将 `https://zh.wikipedia.org/wiki/{month}月{day}日` 页面以 HTML 格式保存到本地
  - 保存下来的页面是繁体中文，我使用了 `OpenCC` 将其转换为简体中文
- 对 HTML 进行处理，将其转换为 TXT 文件
  - 过程中发现一些词汇的表述不统一，例如“**大事迹**”在不同页面可能出现“**大事纪**”或“**大事记**”(~~气人😠~~)
- 将 TXT 文件转换为 JSON

## 🚀 使用

本仓库的数据收集于 *2024 年 9 月 21 日*

- **方法一**：依次运行 `saveWikiHTML.py`、`genWikiTXT.py` 和 `genWikiJSON.py`，便可生成 `WikiJSON`
- **方法二**：直接使用本仓库 `WikiJSON` 文件夹下的现成数据

## ✍️ 后语

- 目前数据处理还不够完善，已知某些 TXT 文件中会有 CSS 代码混入，后续若有时间会进行优化
- 其他内容待补充 😑