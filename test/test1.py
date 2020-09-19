import re
import urllib.request as req

arr = ['123', 'as', 'aa']
arr2 = [1, 2, 3]
newArr = map(lambda x: x + ':map', arr)
print(newArr)
sq = map(lambda x: x ** 2, arr2)
print(list(sq))

print(map(lambda x: x % 2, range(7)))


def extractNumber(string):
    return re.subn(r"\d+\.?\d*", "", string)


s = '-13.50%'
print(list(s))
ss = list(s)[0:-1]
print(s[0:-1])
print(float(-13.13))
print(ss[-1] == '万' or ss[-1] == '亿' or ss[-1] == '%')

str0 = '4.08万亿'
print(str0[0:-2])
print(len(str0))
print(str0[len(str0) - 2:len(str0)])

stocks = [{'code': '300724', 'name': '捷佳伟创'}, {'code': '300725', 'name': '药石科技'}]
for stock in stocks:
    stockCode = stock['code']
    stockName = stock['name']
    print(stockCode, stockName)
