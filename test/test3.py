import json
# from contextlib import
from contextlib import closing
from urllib.request import urlopen

print(ord('a'))
print(chr(98))


def func(*args):
    print(args, type(args))


func(1)


def func2(x, y, *args):
    print(x, y, args)


func2(1, 2, 3, 4, 5)


def func3(*args, **kwargs):
    print(args, kwargs)


func3(6, 7, a=1, b=2, c=3)

list1 = ['01', '02', '03']
list1 = [ele + '*' for ele in list1]
print(list1)
list2 = [num for num in range(2, 11)]
print(list2)

mcase = {'a': 10, 'b': 34, 'A': 7, 'z': 3}
mcase_frequency = {
    k.lower(): mcase.get(k.lower(), 0) + mcase.get(k.upper(), 0)
    for k in mcase.keys()
    if k.lower() in ['a', 'b', 'z']
}
print(mcase_frequency)

squared = {x ** 2 for x in [1, 1, 2]}
print(squared)

dict1 = {'name': ('Tom', 'Ford'), 'age': {1, 2, 3}}

# json数据转成dict字典
j = '''
    {"id": "007", "name": {"fn":"tom","ln":"福德"},
    "age": 28, "sex": "male", "phone": "13000000000", "email": "123@qq.com"}
    '''
dict2 = json.loads(j)
print(dict2['name']['ln'])
print(dict2)

# with open('dict2.json', 'a') as f1, open('dict3.json', 'w') as f2:
#     f1.write('\r\n')
# json.dump(dict2, f1)
# json.dump(dict2, f2)

# with closing(urlopen('http://www.baidu.com')) as page:
#     for line in page:
#         print(line)

with open('dict2.json', 'r') as fr:
    print(fr.readlines())
# 字符串 API测试
print('字符串 API测试')
# split从左开始 rsplit从右开始
S = "this is string example....啊wow!!!"
print(S.split())
print(S.rsplit())
print(S.split('i', 2))
print(S.rsplit('i', 2))
print(S.rsplit('w'))
# strip从头并且从尾  rstrip只从尾巴 lstrip只从头计算
# 神奇的删除 a 挡住了 1 2 3 b 四个规则,删除 a右边的b字母
str2 = "123abcrunoob3221"
print(str2.strip('32b1'))
print(str2.lstrip('123b'))
print(str2.rstrip('32b1'))
