# coding=utf-8
import re
import urllib.request as req


# 过滤字符串中的英文与符号，保留汉字
def extractCharacters(string):
    return re.sub(u"\\(.*?\\)|\\{.*?}|\\[.*?]", "", string)


# 从字符串中提取数字
def extractNumber(string):
    return re.sub("\D", "", string)


# 从字符串中提取字母字符串
def extractLetter(string):
    return ''.join(re.findall(r'[A-Za-z]', string))


def cleanHeadZeroNum(string):
    newStr = ''
    for s in string:
        if s != '0':
            newStr = newStr + s
        else:
            break
    return newStr


def extractStockCode(string):
    codeSplict0 = string.split(")")
    codeSplict1 = codeSplict0[0].split("(")
    return codeSplict1[1]


def extractStockName(string):
    codeSplict0 = string.split(")")
    return codeSplict0[1]


# 爬虫抓取网页的函数
def getHtml(url):
    request = req.Request(url)
    response = req.urlopen(request)
    html = response.read()
    # except request.URLError, e:
    #     if hasattr(e, "code"):
    #         print(e.code)
    #     if hasattr(e, "reason"):
    #         print e.reason
    return html
