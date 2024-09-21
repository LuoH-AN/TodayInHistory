import os
import json

typeMapping = {'1': 'event', '2': 'birth', '3': 'death'}

def processLine(line, folderType):
    if '：' in line:
        year, content = line.split('：', 1)
        year = formatYear(year.strip())
        return {
            'year': year,
            'content': content.strip(),
            'type': typeMapping[folderType]
        }
    return None

def formatYear(year):
    return year.replace('前', '-').replace('年', '')

def readFile(filepath, folderType):
    entries = []
    with open(filepath, 'r', encoding='utf-8') as file:
        for line in file:
            entry = processLine(line, folderType)
            if entry:
                entries.append(entry)
    return entries

def generateJson(wikiTxtDir, outputDir):
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)

    for filename in os.listdir(os.path.join(wikiTxtDir, '1')):
        if filename.endswith('.txt'):
            baseName = filename.replace('月', '-').replace('日.txt', '')

            allEntries = []
            for folderType in ['1', '2', '3']:
                filepath = os.path.join(wikiTxtDir, folderType, filename)
                if os.path.exists(filepath):
                    allEntries.extend(readFile(filepath, folderType))

            outputFilepath = os.path.join(outputDir, f"{baseName}.json")
            with open(outputFilepath, 'w', encoding='utf-8') as jsonFile:
                json.dump(allEntries, jsonFile, ensure_ascii=False, indent=4)
                print(f"完成 {outputFilepath}")

wikiTxtDirectory = "WikiTXT"
outputDirectory = "WikiJson"
generateJson(wikiTxtDirectory, outputDirectory)