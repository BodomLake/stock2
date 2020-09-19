# '数据库类型+数据库驱动名称://用户名:口令@机器地址:端口号/数据库名'
def dbConnInfo(user='root', password='rex123456', host='127.0.0.1', port='3306', args='charset=utf8mb4', schema='stock'):
    # pymysql 会 报出警告
    # return 'mysql+pymysql://' + user + ':' + password + '@' + host + ':' + port + '/' + schema + '?' + args
    return 'mysql+mysqlconnector://' + user + ':' + password + '@' + host + ':' + port + '/' + schema + '?' + args


driverpath = r'D:\Python37\Lib\site-packages\selenium\webdriver\chrome\chromedriver83.0.4103.exe'

phoneHead = '--user-agent=Mozilla/5.0 (iPad; CPU OS 5_0 like Mac OS X) ' \
            'AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3'

