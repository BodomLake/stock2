import time

import pymongo as pmg
import numpy as np

myclient = pmg.MongoClient("mongodb://localhost:27017/")
# 获取数据库列表
dblist = myclient.list_database_names()
db_stock = myclient['stock']
org_list = db_stock['list']
org_list_china = db_stock['list-china']

arr1 = []
doc1 = org_list.find({'marketType': {'$in': [0, 1, 6]}})

for x in doc1:
    arr1.append(x['code']);

arr2 = []
arr2_full = []
doc2 = org_list_china.find({})

for y in doc2:
    arr2.append(y['code']);
    arr2_full.append(y)

across = [val for val in arr1 if val in arr2]
# print(across)
print(len(across))
# arr1中有,而arr2中没有的
diff1 = list(set(arr1).difference(set(arr2)))
# 反之
diff2 = list(set(arr2).difference(set(arr1)))
print(diff1)
print(diff2)
print('长度:',len(diff2))

# 拼接 json数组 {code:'',name:''}
doc3 = org_list_china.find({})
attachStockArray = []
for d in diff2:
    for z in arr2_full:
        if d == z['code']:
            attachStockArray.append({'code': z['code'], 'name': z['name']})
            break;

print('长度:',len(attachStockArray),'//',attachStockArray)
# print(arr1)
# print(arr2)
