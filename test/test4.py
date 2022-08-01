import time
import pymongo as pmg
myclient = pmg.MongoClient("mongodb://localhost:27017/")
# 获取数据库列表
dblist = myclient.list_database_names()
print('数据库：', dblist)

stock = myclient['isp']
# 集合finance
financeReport = stock['finance']
# 集合list
stockList = stock['list']
# 财报信息
financeReportArr = []
# 是否归档
# stockList.update_many({}, { '$set': {'archived': False }})
# 是否在爬取数据的时候遭遇了程序异常
# stockList.update_many({}, { '$set': {'exception': None }})

startTime = time.time();
# 无条件找出所有的数据
for fr in financeReport.find({}):
    # 条件更新：只要有财务报表数据，就更新为True，意思是 已被归档
    stockList.update_many({ 'code': fr['code']},{ '$set': {'archived': True }})
    financeReportArr.append(fr)
print('结束耗时:', time.time() - startTime, 's' )
# doc3 = stockList.find({'marketType': 0}, {'code': 1, 'name': 1}).skip(621).limit(10)
