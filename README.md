[Orcarouter 推荐注册链接](https://www.orcarouter.ai/register?ref=ref_b23c0b803926cafdcf9e)

# ⌛ TodayInHistory | 历史上的今天

数据来源：
- [Wikipedia](https://zh.wikipedia.org/)
- [Baidu](https://baike.baidu.com/calendar)

# 📖 前言

在 GitHub 上看到了一个关于 **历史上的今天** 的项目，但该仓库的数据收集于 2020 年，且没有进一步更新。受此启发，我决定进行自己的数据收集

本仓库正是在这个想法下诞生的

## Wiki

### 🛠️ 过程

*所有数据处理均使用 Python 完成*

- 将 `https://zh.wikipedia.org/zh-cn/{month}月{day}日` 页面以 HTML 格式保存到本地
  - 使用维基 `zh-cn` 语言变体接口，直接获取简体中文页面（官方字词转换，无需 OpenCC）
- 使用 `BeautifulSoup` 提取 **大事记 / 出生 / 逝世** 三个章节，转换为 TXT 文件
- 将 TXT 文件转换为 JSON

### 🚀 使用

先安装依赖：

```bash
pip install -r requirements.txt
```

依次运行以下脚本：

```bash
# 抓取全年 366 个页面（约 10-20 分钟）
python saveWikiHTML.py

# HTML 转分节 TXT
python genWikiTXT.py

# TXT 合并为每日 JSON
python genWikiJSON.py
```

- 每个脚本支持 `--help` 查看参数，例如 `--month 1 --day 1` 可只处理单日，便于增量更新
- 或者直接使用本仓库 `Wiki/WikiJson` 文件夹下的现成数据

### JSON 格式

`Wiki/WikiJson/{m}-{d}.json` 为数组，每个元素：

```json
{
    "year": "-45",
    "content": "罗马共和国独裁官尤利乌斯·凯撒规定开始使用儒略历，取代旧有的罗马历。",
    "type": "event"
}
```

- `year`：年份，公元前的年份以负数表示
- `type`：`event`（大事记）/ `birth`（出生）/ `death`（逝世）

## Baidu

### 🛠️ 过程

*所有数据处理均使用 Python 完成*

- 将 `https://baike.baidu.com/calendar` 页面以 HTML 格式保存到本地
  - 可是并无任何数据
- 经过一番寻找在 `https://baike.baidu.com/cms/home/eventsOnHistory/{month:02d}.json` 中找到了源 JSON

### 🚀 使用

```bash
# 抓取全部 12 个月
python saveBaiduJSON.py
```

- 支持 `--month` 参数只抓取单月
- 或者直接使用本仓库 `Baidu/BaiduJson` 文件夹下的现成数据

# ✍️ 后语

- 本仓库数据收集于 *2026 年 10 月 4 日*
- 数据有更新需求时，重新运行上述脚本即可
