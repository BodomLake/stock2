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
import logging
import threading
import akshare as ak
import json
import pymongo
import time
from threading import Thread

from utils.utils import get_date, split_group_by_gn

logging.basicConfig(filename='../../log/ppd-2022-07-31.log', filemode='a', level=logging.WARNING,
                    format='%(asctime)s - %(pathname)s - %(levelname)s: %(message)s')


def print_each_line(raw_data):
    for d in json.loads(raw_data.T.to_json()).values():
        print(d)


# 连接mongoDB 数据库
mongoDB = pymongo.MongoClient("mongodb://localhost:27017/")
# 选择数据库
db_stock = mongoDB['isp']
# 股票基本信息集合
stockList = db_stock['list']
# 大陆股票 深市 沪市 科创版
mainland_stock_list = []
# marketType =0是沪市股票 =1是深市股票(30开头的是创业板) =6是科创股票
# 找出未能归档的股票
mainland_stock = stockList.find({'marketType': {'$in': [0, 1, 6]}, 'ppd_archived': {'$in': [None, False]}})
for stock in mainland_stock:
    mainland_stock_list.append(stock)

start_date = "20050101"
# 计算一下今天的日期
end_date = "20220730"
now = get_date()
end_date = now['year'] + now['month'] + now['day']

print(start_date, end_date)
#  默认收集前复权的数据
adjust = 'qfq'

process_start_time = time.time()

ppd = db_stock['ppd']


# 处理每日交易股票交易价格
def process_ppd(stocks):
    # buffer_date_array = []
    for stock in stocks:
        single_process_time = time.time()
        # 查询以股票代码为准，有时候股票的名字会出现XD,ST的前缀
        stockCode = stock['code']
        stockName = stock['name']
        market_type = stock['marketType']
        network_io_start_time = time.time()
        try:
            stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol=stockCode, period="daily", start_date=start_date,
                                                    end_date=end_date,
                                                    adjust=adjust)
            print('network io time cost:', time.time() - network_io_start_time, 's')
            document = json.loads(stock_zh_a_hist_df.T.to_json()).values()
            # 是什么市场的股票 0 1 6
            insertDataArray = []
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
                insertDataArray.append(oneData)
            # print('inserted_data', insertDataArray)
            # price per minute
            ppd.insert_many(insertDataArray)
            print('[股票：', stockName, '股票代码:', stockCode, ']', '的数据已被处理并入库',
                  '对象大小', insertDataArray.__sizeof__(),
                  '耗时：', time.time() - single_process_time, 's')
            stock['ppd_archived'] = True
        except Exception as ex:
            logging.warning(msg=stockCode + ':' + str(ex))
        finally:
            stockList.update_one({'code': stockCode}, {'$set': stock})
    # return buffer_date_array


# 先分配好任务，把目标股票的处理任务分成10份，每份由一个线程执行


def consistence_task(stocks):
    start_time = time.time()
    thread_name = threading.current_thread().name
    print('线程：', thread_name, '已经开始了工作')
    process_ppd(stocks)
    print('[' + thread_name + ' consistence_task 耗时]:', time.time() - start_time)


''' 
    两种线程工作
    network_thread处理网路线程的请求，缓存到内存对象中：分为10个线程，每个线程都会发起请求
    database_thread处理缓存对象：由一个单独的数据库处理线程做对MongoDB的数据插入
'''
group_len = 10
task_num = group_len
stock_split_group = split_group_by_gn(arr=mainland_stock_list, gn=group_len)
# print('stock_split_group:', stock_split_group)
network_threads = []
# 十个线程
for task_index in range(task_num):
    th = Thread(target=consistence_task, args=(stock_split_group[task_index],),
                name=('network_thread-' + str(task_index)))
    network_threads.append(th)
    th.start()

for th in network_threads:
    th.join()

process_end_time = time.time()
print(process_end_time - process_start_time, 's')
