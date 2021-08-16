import time

import pymongo as pmg

myclient = pmg.MongoClient("mongodb://localhost:27017/")
# 获取数据库列表
dblist = myclient.list_database_names()
print(dblist)

stock = myclient['stock']
finance = stock['finance']
stockList = stock['list']

# 传入JSON形式的空对象，会删除该集合中所有的数据
# list.delete_many({})

# 锁定一个字段，需要在该字段下的一个类型为数组的元素 进行筛选，用$elemMatch 匹配需要遍历的每个元素
startTime = time.time()
doc2 = finance.find({"tables.data": {
    "$elemMatch": {"text": '2.49亿', "period": "2020-06-30", "indicator": "净利润(元)"}
}}, {"code": 1, "name": "1"})

arr1 = []
for x in doc2:
    print(x)
    arr1.append(x)
print('查询结果总数为：', len(arr1))
print('耗时', time.time() - startTime, 's')
arr2 = []
stockList = stock['list']
# doc3 = stockList.find({'marketType': 0}, {'code': 1, 'name': 1}).skip(621).limit(10)
doc3 = stockList.find({'marketType': 0}, {'code': 1, 'name': 1})
for x in doc3:
    # print(x['code'])
    arr2.append(x)
print(len(arr2), '个')

# 1604 + 2343 = 3947 (同花顺有55没有找到)
# 3892 + 55 = 3947
# for arr2_item in arr2:
#     print(arr2_item['code'], ':', arr2_item['name'])
