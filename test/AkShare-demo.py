import akshare as ak
import pandas as pd
import numpy as np
import json
import pymongo as pmg

myclient = pmg.MongoClient("mongodb://localhost:27017/")
stock = myclient['stock']
stockList = stock['list-hk']

# 上海股票全貌 限量: 单次返回最近交易日的股票数据总貌数据(当前交易日的数据需要交易所收盘后统计)
# stock_sse_summary_df = ak.stock_sse_summary()
# stock_sse_summary_df.reset_index(inplace=True)
# doc = json.loads(stock_sse_summary_df.T.to_json()).values()

# 截止某年某月某日 深圳证券交易所-市场总貌 限量: 单次返回最近交易日的市场总貌数据(当前交易日的数据需要交易所收盘后统计)
# stock_szse_summary_df = ak.stock_szse_summary(date="20200930")
# doc = json.loads(stock_szse_summary_df.T.to_json()).values()

# 全股实时行情数据11
# stock_zh_a_spot_df = ak.stock_zh_a_spot()
# doc = json.loads(stock_zh_a_spot_df.T.to_json()).values()
# stockList.insert_many(doc)


# 单次返回具体某个 A 上市公司的所有历史行情数据
# 默认返回不复权的数据; qfq: 返回前复权后的数据; hfq: 返回后复权后的数据; hfq-factor: 返回后复权因子; hfq-factor: 返回前复权因子
# stock_zh_a_daily_hfq_df = ak.stock_zh_a_daily(symbol="sh688021")
# print(stock_zh_a_daily_hfq_df)
# doc = json.loads(stock_zh_a_daily_hfq_df.T.to_json()).values();
# doc_key = stock_zh_a_daily_hfq_df.T.keys();
# stockList.insert_many(doc)
# for d in doc:
#     print(d)


# stock_financial_abstract_df = ak.stock_financial_abstract(stock="300724")
# doc = json.loads(stock_financial_abstract_df.T.to_json()).values()
# for d in doc:
#     print(d)

current_data_df = ak.stock_hk_spot()
print(current_data_df.T.keys())
doc = json.loads(current_data_df.T.to_json()).values()
# stockList.insert_many(doc)
for d in doc:
    print(d)