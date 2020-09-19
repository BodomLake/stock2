import pymysql

cursor = None


class DBUtil(object):

    # 初始化数据库连接信息
    def __init__(self):
        self.__db_host = "localhost"
        self.__db_port = 3306
        self.__db_user = "root"
        self.__db_password = "rex123456"
        self.__db_database = "stock"
        self.__db_charset = 'utf8mb4'

    # 打开数据库连接
    def isConnectionOpen(self):
        self.__db = pymysql.connect(
            host=self.__db_host,
            port=self.__db_port,
            user=self.__db_user,
            password=self.__db_password,
            database=self.__db_database,
            charset=self.__db_charset,
        )
        # 初始化mysql光标
        global cursor
        cursor = self.__db.cursor()

    # 检查表的初始化
    def initTable(self, path: str):
        # 引用全局游标
        self.isConnectionOpen()
        global cursor
        with open(path, encoding='utf-8', mode='r') as file:
            sqls = file.read().split(';')[:-1]
            for sql in sqls:
                # 判断包含空行的
                if '\n' in sql:
                    # 替换空行为1个空格
                    sql = sql.replace('\n', ' ')

                # 判断多个空格时
                if '    ' in sql:
                    # 替换为空
                    sql = sql.replace('    ', '')

                # sql语句添加分号结尾
                sql_item = sql + ';'
                print("执行语句：", sql_item)
                cursor.execute(sql_item)

    # 插入数据
    def insert(self, rows: []):
        try:
            # connect the database
            self.isConnectionOpen()
            # 全局游标
            global cursor
            # sql命令

            code = rows[0]
            name = rows[1]
            market = rows[2]
            market_type = rows[3]
            sql = str("insert into stocks(code,name,market,market_type) value(")
            sql = sql + str(code) + ","
            sql = sql + "'" + name + "',"
            sql = sql + "'" + market + "',"
            sql = sql + str(market_type)
            sql = sql + ");"
            print("执行语句：", sql)
            # 执行sql命令
            cursor.execute(sql)
        except Exception as ex:
            print(ex)
        finally:
            # 关闭游标
            cursor.close()
            # 提交
            self.__db.commit()

    def closeConnect(self):
        # 关闭数据库连接
        self.__db.close()
