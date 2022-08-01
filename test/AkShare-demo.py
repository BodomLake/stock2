import akshare as ak
import pandas as pd
import numpy as np
import json
import pymongo as pmg

myclient = pmg.MongoClient("mongodb://localhost:27017/")
stock = myclient['stock']
stockList = stock['list-hk']

def prtEachLine(rawData):
    doc = json.loads(rawData.T.to_json()).values()
    for d in doc:
        print(d)

# 上海股票全貌 限量: 单次返回最近交易日的股票数据总貌数据(当前交易日的数据需要交易所收盘后统计)
# stock_sse_summary_df = ak.stock_sse_summary()

# 截止某年某月某日 深圳证券交易所-市场总貌 限量: 单次返回最近交易日的市场总貌数据(当前交易日的数据需要交易所收盘后统计)
# stock_szse_summary_df = ak.stock_szse_summary(date="20200930")

# 全股实时行情数据11
# stock_zh_a_spot_df = ak.stock_zh_a_spot()

# 单次返回具体某个 A 上市公司的所有历史行情数据
# 默认返回不复权的数据; qfq: 返回前复权后的数据; hfq: 返回后复权后的数据; hfq-factor: 返回后复权因子; hfq-factor: 返回前复权因子
# stock_zh_a_daily_hfq_df = ak.stock_zh_a_daily(symbol="sh688021")

# stock_financial_abstract_df = ak.stock_financial_abstract(stock="300724")

# current_data_df = ak.stock_hk_spot()

# symbol="创月新高"; choice of {"创月新高", "半年新高", "一年新高", "历史新高"}
# stock_rank_cxg_ths_df = ak.stock_rank_cxg_ths(symbol="半年新高")
# prtEachLine(stock_rank_cxg_ths_df)

# 连续上涨
# stock_rank_lxsz_ths_df = ak.stock_rank_lxsz_ths()

# 接口示例-历史行情数据-前复权-东方财富
# stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol="000001", period="daily", start_date="20170301", end_date='20210907', adjust="qfq")
# prtEachLine(stock_zh_a_hist_df)

# 接口示例-历史行情数据-前复权-新浪财经
# stock_zh_a_daily_qfq_df = ak.stock_zh_a_daily(symbol="sz000002", start_date="20101103", end_date="20201116", adjust="qfq")
# prtEachLine(stock_zh_a_daily_qfq_df)

# 历史行情数据-网易
# stock_zh_a_hist_163_df = ak.stock_zh_a_hist_163(symbol="sh601318", start_date="20210101", end_date="20220101")
# prtEachLine(stock_zh_a_hist_163_df)

# （举例：美达股份） 分时数据-东财
# stock_zh_a_hist_min_em_df = ak.stock_zh_a_hist_min_em(symbol="000782", start_date="2022-07-20 09:30:00", end_date="2022-07-22 15:00:00", period='1', adjust='qfq')
# stock_zh_a_hist_min_em_df = ak.stock_zh_a_hist_min_em(symbol="000782", period='5', adjust='qfq')
# print(stock_zh_a_hist_min_em_df)

'''
    接口: stock_zh_a_hist_pre_min_em
    目标地址: http://quote.eastmoney.com/concept/sz000782.html?from=classic
    描述: 东方财富 - 股票行情 - 盘前数据
    限量: 单次返回指定当前交易日的股票分钟数据, 包含盘前分钟数据
'''
# stock_zh_a_hist_pre_min_em_df = ak.stock_zh_a_hist_pre_min_em(symbol="000782")
# print(stock_zh_a_hist_pre_min_em_df)
'''
接口: stock_zh_a_cdr_daily

目标地址: https://finance.sina.com.cn/realstock/company/sh689009/nc.shtml

描述: 上海证券交易所-科创板-CDR

限量: 单次返回指定 CDR 的日频率数据, 分钟历史行情数据可以通过 stock_zh_a_minute 获取
'''
# stock_zh_a_cdr_daily_df = ak.stock_zh_a_cdr_daily(symbol='sh689009', start_date='20201103', end_date='20201116')
# print(stock_zh_a_cdr_daily_df)

'''接口: stock_zh_b_daily

目标地址: https://finance.sina.com.cn/realstock/company/sh900901/nc.shtml(示例)

描述: B 股数据是从新浪财经获取的数据, 历史数据按日频率更新

限量: 单次返回指定 B 股上市公司指定日期间的历史行情日频率数据
'''
stock_zh_b_daily_qfq_df = ak.stock_zh_b_daily(symbol="sh900901", start_date="20101103", end_date="20201116", adjust="qfq")
prtEachLine(stock_zh_b_daily_qfq_df)