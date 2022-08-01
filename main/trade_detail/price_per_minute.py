"""
收集数据：
    补完之前20个交易日的信息
    每日定时任务:检查交易数据是否更新，如果没有补全需要的信息
    当前用 AKShare 获取数据，精确到分钟
    先约定一些数据结构，存储在mongodb中
    精确到分时图
分析数据：
    在确认数据收集完毕的情况下，才能进行数据分析
    统计打板的可能股票，找出对应的连板数（3板，4板这种），
    每一天下午5点，执行 统计任务和分析任务
    打板成功率，
"""
import akshare as ak
import json
import pymongo
from datetime import datetime


# 600651 飞乐音响 新中国第一支上市股票
from utils.utils import get_date


def print_each_line(raw_data):
    for d in json.loads(raw_data.T.to_json()).values():
        print(d)


now = datetime.now()
print(now.year, now.month, now.day, now.hour, now.minute, now.second)
# 连接mongoDB 数据库
mongoDB = pymongo.MongoClient("mongodb://localhost:27017/")
# 选择数据库
db_stock = mongoDB['isp']

start_date = "20000701"
end_date = "20220730"
now = get_date()
end_date = now['year'] + now['month'] + now['day']

# 查询以股票代码为准，有时候股票的名字会出现XD,ST的前缀
stockCode = '200992'
stockName = '四方达'
adjust = 'qfq'
market_type = 1
# 四方达
stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol=stockCode, period="daily", start_date=start_date, end_date=end_date,
                                        adjust=adjust)
# {'日期': '2022-07-01', '开盘': 14.77, '收盘': 14.69, '最高': 14.84, '最低': 14.61,
# '成交量': 779243, '成交额': 1164030784.0, '振幅': 1.56, '涨跌幅': -0.41, '涨跌额': -0.06, '换手率': 0.4}
document = json.loads(stock_zh_a_hist_df.T.to_json()).values()
# 是什么市场的股票 0 1 6
insertDatas = []
# 每天的数据，更新给具体的那一只股票
for doc in document:
    date = doc['日期']
    Open = doc['开盘']
    close = doc['收盘']
    high = doc['最高']
    low = doc['最低']
    trading_volume = doc['成交量']
    transaction_amount = doc['成交额']
    # 价格剧烈震动的时候，振幅偏高
    amplitude = doc['振幅']
    # 百分率数据（不会小于涨跌幅）
    # 对于普通股票，大于9.9%算作涨停
    # 当前，对于科创版，创业板平时的交易日，约等于20%才能算作涨停
    fluctuation = doc['涨跌幅']
    # 百分比数据
    price_change = doc['涨跌额']
    turnover_rate = doc['换手率']
    oneData = {
        'code': stockCode, 'market_type': market_type, 'adjust': adjust,
        'date': date,
        'open': Open,
        'close': close,
        'high': high, 'low': low,
        'transaction_amount': transaction_amount,
        'trading_volume': trading_volume,
        'amplitude': amplitude,
        'fluctuation': fluctuation,
        'price_change': price_change,
        'turnover_rate': turnover_rate,
    }
    # insertData = {'code': stockCode, 'market_type': 0, 'adjust': 'qfq', 'ppd': oneData}
    insertDatas.append(oneData)
# price per minute
ppd = db_stock['ppd']
ppd.insert_many(insertDatas)

print(document)
