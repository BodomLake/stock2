import os

# stocks

# main_indicators
# balance_sheets
# profit_statement
# cash_flow_statement
# bank_specific_indicators

tablename = 'main_indicators'
line_size = 1000

# 文件名称
old_file_name = 'D:\\Finance\\2020-06-28\\sz\\' + tablename + '.sql';

# 要写入的新文件
new_file_name = 'D:\\Finance\\2020-06-28\\sz\\quickInsert\\' + tablename + '.sql';

# 文件大小
print('文件大小:', os.path.getsize(old_file_name))

# 边读边写
# 长时间打开新文件 追加模式
with open(new_file_name, mode='a', encoding='utf8') as new_sql_file:
    # 读取文件
    sql_file = open(old_file_name, mode='r', encoding='utf8')
    # 新文件写入
    new_sql_file.write('INSERT INTO `' + tablename + '` VALUES ')
    # 内部计数
    count = 0
    # lineList = sql_file.readlines()
    for line in sql_file.readlines():
        # 如果是插入语句 就进入 sql拼接
        if line.startswith('INSERT'):
            # 打印改行
            # print(lines, end='')
            # 取出values后面的部分
            data = line.split(sep='VALUES')[1].split(';')[0]
            # 打印该行的数据部分
            # print(data)
            # 向新文件写入该数据
            new_sql_file.write(data)
            # (index < len(lineList) - 3)
            # index = lineList.index(line)
            # 如果不是这一段插入语句的最后一条数据，就加入逗号分离
            if count < line_size - 1:
                new_sql_file.write(',')
            count = count + 1
            # 如果是最后一条数据，就用分号结尾
            if count == line_size:
                new_sql_file.write(';')
                new_sql_file.write('\n')
                new_sql_file.write('INSERT INTO `' + tablename + '` VALUES ')
                count = 0

sql_file.close()

# 处理尾部多余括号
with open(new_file_name, mode='rb+') as file0:
    file0.seek(0, 2)
    file0.truncate(file0.tell() - 1)
file0.close()

# 尾部分号结尾
with open(new_file_name, mode='a') as file1:
    file1.write(';')
file1.close()
