from selenium.webdriver import Chrome
from selenium import webdriver
import time
from utils.Page import Page
from utils.Part import Part



def getCurrent(chrome_browser: webdriver):
    return chrome_browser.execute_script("return document.getElementsByClassName(\"bpx-player-ctrl-time-current\")[0].textContent")


def convertT(a):
    temp = a.split(":")
    ret = 0
    for i in range(len(temp)):
        ret = ret * 60 + int(temp[i])
    return ret


def processTxt(path):
    file = open(path, 'r', encoding='UTF-8')
    datas = file.readlines()
    rt = dict()
    for i in range(int(len(datas)/2)):
        tm = convertT(datas[2*i])
        rt[tm] = datas[2*i+1][:-1]
    return rt


def findText(current, times):
    index = 0
    for i in range(len(times)):
        if current > times[i]:
            continue
        else:
            index = i
            break
    return times[index]


def contactSentence(line, lines):
    i = 0
    ch = line[0]
    while i < len(line):
        ch = line[i]
        if ch == ' ':
            i = i + 1
        else:
            break
    if 'a' <= ch <= 'z':
        before = ""
        if len(lines) != 0:
            before = lines[-1]
            if "[click]" in before:
                return line
            lines.remove(lines[-1])
        else:
            before = ""
        line = before.replace("\n", " ") + line
        return line
    else:
        return line


def separateSentence(line, lines):
    i = 0
    j = 0
    flag = False
    while i < len(line):
        ch = line[i]
        if ch == '.' or ch == '?':
            j = i
            while i < len(line) - 1:
                i = i + 1
                ch = line[i]
                if ch == ' ':
                    continue
                else:
                    break
            if 'A' <= ch <= 'Z':
                flag = True
                break
        i = i + 1
    if not flag:
        return line
    else:
        line1 = line[0:j+1]
        line2 = line[i:-1]
        lines.append(line1+"\n")
        return line2


def write(pages):
    file = open('data/new.txt', 'w', encoding='UTF-8')
    lines = []
    tmp = []
    for page in pages:
        tmp.append(("第"+str(page.getNo())+"页").center(80, "=")+"\n")
        parts = page.getContent()
        for part in parts:
            for text in part.getContent():
                tmp.append(text)
            if part != parts[-1]:
                tmp.append("[click]")

    for line in tmp:
        if line == "":
            continue
        line = contactSentence(line, lines)
        line = separateSentence(line, lines)
        line = line + "\n"
        lines.append(line)
    for line in lines:
        file.write(line)
    file.close()


data = processTxt('data/file.txt')
print("字幕文件处理成功".center(80, "="))
print("点击：c")
print("翻页：s")
print("结束：q")
chrome = Chrome()
chrome.get("https://www.bilibili.com/video/BV1rZ4y1o7aS/?p=6&vd_source=085b289c1b65a07afc7d78543630d105")
time.sleep(3)
begin = 0
end = 0
pages = []
page = Page(1)
pages.append(page)
while True:
    times = list(data.keys())
    cmd = input()

    if cmd == "c" or cmd == "s" or cmd == "q":
        part = Part()
        current = convertT(getCurrent(chrome))
        if cmd != "q":
            end = findText(current, times)
        else:
            end = times[-1]+1
        print(str(begin) + "s--" + str(end)+"s")
        for time in data.keys():
            if begin <= time < end:
                part.add(data[time])
        begin = end
        page.add(part)
    if cmd == "q":
        break
    if cmd == "s":
        print("generate new Page")
        page = Page(page.getNo() + 1)
        pages.append(page)

write(pages)
chrome.close()


