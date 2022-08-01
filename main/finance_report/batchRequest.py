import logging
import time
import pymongo as pymg
from utils.launchBrowser import launchChrome
from utils.processStock import processStock

# format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
# 设置输出 log文件位置
logging.basicConfig(filename='../../log/stock-2022-07-23.log', filemode='a', level=logging.WARNING,
                    format='%(asctime)s - %(pathname)s - %(levelname)s: %(message)s')
# 启动浏览器
print('Ready to launch the browser!')
# 打印日志 表示正式启动程序
logging.warning(msg='Starting')
# 目标url前缀
domain = 'http://basic.10jqka.com.cn/'
# 财报url后缀
subject = '/finance'
# 这次要处理的股票代码和股票名称

# 连接mongoDB 数据库
mongoDB = pymg.MongoClient("mongodb://localhost:27017/")
# 选择数据库
db_stock = mongoDB['isp']
# 财报集合
finance = db_stock['finance']
# 股票基本信息集合
stockList = db_stock['list']

stockArray = []
# 深市 沪市 科创版
# marketType =0是沪市股票 =1是深市股票 =6是科创股票
# 找出未能归档的股票
doc1 = stockList.find({'marketType': {'$in': [0, 1, 6]}, 'archived': False})
for z in doc1:
    stockArray.append(z);

# 启动浏览器 准备爬取信息
browser = launchChrome()
# 循环每个股票代表的url
for stock in stockArray:
    stockCode = stock['code']
    stockName = stock['name']
    archived = stock['archived']
    exception = stock['exception']
    # 如果已经归档或者说有错误的，就跳过
    try:
        url = domain + stockCode + subject + '.html'
        browser.get(url=url)
        # 指定的浏览器 资源路径 股票名称 股票代码 要插入的数据库 ；返回处理好的bson数据源
        insertData = processStock(browser, url, stockCode, stockName)
        # 插入mongodb的Collection中
        if insertData != {}:
            finance.insert_one(insertData)
            # 归档成功（默认为False）
            stock['archived'] = True
            stock['exception'] = None
        elif insertData == {}:
            print(stockName, '[', stockCode, ']', '的报表在同花顺不存在')
            logging.warning(msg=stockCode)
            stock['archived'] = False
            stock['exception'] = '同花顺不存在该报表'
    except Exception as ex:
        print(ex)
        logging.warning(msg=stockCode + ':' + ex)
        # 默认是None的数据
        stock['exception'] = str(ex)
    finally:
        # 更新最新的情况
        stockList.update_one({'code': stockCode}, {'$set': stock})

print('Ready to close the browser!')
logging.warning(msg='Ending')
print('All is over:', time.asctime())
browser.close()
browser.quit()
