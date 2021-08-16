import logging
import time
import pymongo as pymg
from utils.launchBrowser import launchChrome
from utils.processStock import processStock

# format='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'
# 设置输出 log文件位置
logging.basicConfig(filename='../log/stock.log', filemode='a', level=logging.WARNING,
                    format='%(asctime)s - %(pathname)s - %(levelname)s: %(message)s')
# 启动浏览器
print('Ready to launch the browser!')
# 打印日志 表示正式启动程序
logging.warning(msg='Starting')
# 目标url前缀
domain = 'http://stockpage.10jqka.com.cn/'
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
# 深市 沪市
doc1 = stockList.find({'marketType': {'$in': [0, 1, 6]}})
for z in doc1:
    stockArray.append({'code': z['code'], 'name': z['name']});
# {'code': z['code'], 'name': z['name']}

# 启动浏览器 准备爬取信息
browser = launchChrome()
# 循环每个股票代表的url
for stock in stockArray:
    try:
        stockCode = stock['code']
        stockName = stock['name']
        url = domain + stockCode + subject
        browser.get(url=url)
        # 指定的浏览器 资源路径 股票名称 股票代码 要插入的数据库 ；返回处理好的bson数据源
        insertData = processStock(browser, url, stockCode, stockName)
        # 插入mongodb的Collection中
        if insertData != {}:
            finance.insert_one(insertData)
        elif insertData == {}:
            print(stockName, '[', stockCode, ']','的报表在同花顺不存在')
            logging.warning(msg=stockCode)
    except Exception as ex:
        print(ex)
        logging.warning(msg=stockCode + ':' + ex)

print('Ready to close the browser!')
logging.warning(msg='Ending')
print('All is over:', time.asctime())
browser.close()
browser.quit()
