import os
import re

tagRe = re.compile(r'<[^>]+>')

def ensureOutputDirectories(outputDir):
    for i in range(1, 4):
        os.makedirs(f'{outputDir}/{i}', exist_ok=True)

def readFile(filePath):
    with open(filePath, 'r', encoding='utf-8') as f:
        return f.read()

def writeFile(filePath, content):
    with open(filePath, 'w', encoding='utf-8') as f:
        f.write(content)

def processHtmlContent(content):
    content = content.replace('节假日与风俗', '节假日和习俗')
    content = content.replace('大事记', '大事迹')
    content = content.replace('大事纪', '大事迹')

    lines = content.splitlines()

    sections = {'section1': [], 'section2': [], 'section3': []}
    currentSection = None

    for line in lines:
        cleanLine = tagRe.sub('', line)

        if 'h2 id="大事迹"' in line:
            currentSection = sections['section1']
        elif 'h2 id="出生"' in line:
            currentSection = sections['section2']
        elif 'h2 id="逝世"' in line:
            currentSection = sections['section3']
        elif 'h2 id="节假日和习俗"' in line:
            currentSection = None

        if currentSection is not None and currentSection != sections['section3']:
            currentSection.append(cleanLine)

        if currentSection == sections['section3'] and 'h2 id="节假日和习俗"' not in line:
            sections['section3'].append(cleanLine)

    return sections

def saveSections(outputDir, fileNameNoExt, sections):
    for i, section in enumerate(['section1', 'section2', 'section3'], start=1):
        if sections[section]:
            writeFile(f'{outputDir}/{i}/{fileNameNoExt}.txt', '\n'.join(sections[section]))

def cleanTextFile(txtFile):
    if not os.path.exists(txtFile):
        return

    with open(txtFile, 'r', encoding='utf-8') as f:
        txtLines = f.readlines()

    centuryPattern = re.compile(r'^\d+世纪')
    for idx, txtLine in enumerate(txtLines):
        if centuryPattern.search(txtLine):
            txtLines = txtLines[idx:]
            break

    txtLines = [line for line in txtLines if '[编辑]' not in line]

    writeFile(txtFile, ''.join(txtLines))

def processHtmlFiles(directory, outputDir):
    ensureOutputDirectories(outputDir)

    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".html"):
                filePath = os.path.join(root, file)
                fileNameNoExt = os.path.splitext(file)[0]

                content = readFile(filePath)

                sections = processHtmlContent(content)
                saveSections(outputDir, fileNameNoExt, sections)

                for i in range(1, 4):
                    txtFile = f'{outputDir}/{i}/{fileNameNoExt}.txt'
                    cleanTextFile(txtFile)

                print(f"处理 {file}")

directory = "WikiHTML"
outputDir = "WikiTXT"

processHtmlFiles(directory, outputDir)