# coding=utf-8
import math
import re
import urllib.request as req
from datetime import datetime
import numpy as np


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


def get_date():
    now = datetime.now()
    print(now.year, now.month, now.day, now.hour, now.minute, now.second)
    year = now.year
    month = now.month
    day = now.day
    if now.month < 10:
        month = '0' + str(month)
    if now.day < 10:
        day = '0' + str(day)

    return {
        'year': str(year),
        'month': str(month),
        'day': str(day),
    }


# length: 每组的长度
def split_group(arr, length):
    return [arr[idx:idx + length] for idx in range(0, len(arr), length)]


# 分割数组，按照数组的个数
def split_group_by_gn(arr, gn):
    # 数组最大长度
    max_length = math.floor(len(arr) / gn)
    return split_group(arr, max_length)


if __name__ == '__main__':
    for i in range(0, 3):
        print(i)
    array = ['START', 'a', 12378912,
             'ASD', 'sds', 'zxc',
             'qwe', '---', '))',
             "/\\/<", "saa", "JKL",
             "<<", ">>", "JKL",
             "\\<", 213, "END"]
    print('最后三个：', array[-3:])
    print('按照组长分组', split_group(arr=array, length=5))
    print('按照组数分组', split_group_by_gn(arr=array, gn=2))
    print(range(0, 22, 5))
    date = get_date()
    print(date['year'], date['month'], date['day'])
