import tushare as ts
import pandas as pd
import numpy as np
import json
import pymongo as pmg

myclient = pmg.MongoClient("mongodb://localhost:27017/")
stock = myclient['stock']
stockList = stock['ipo']

token = '97b8ee1058b9f62942e6537a8b42178296a484894d3086e94452317d'
ts.set_token(token)

pro = ts.pro_api()
# 查询当前所有正常上市交易的股票列表
# df = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
# df = pro.stock_company(exchange='SZSE', fields='ts_code,chairman,manager,secretary,reg_capital,setup_date,province')
# df = pro.stk_managers(ts_code='000001.SZ')
df = pro.new_share(start_date='20200923', end_date='20200930')
# print(json.loads(df.T.to_json()).values())

# stockList.insert_many(json.loads(df.T.to_json()).values())
doc = json.loads(df.T.to_json()).values()
for d in doc:
    print(d['name'] + ' ' +d['ts_code'])
# df.to_csv('20201001.xls', encoding='utf-8-sig')
