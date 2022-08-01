import time
from datetime import datetime
import calendar

now = datetime.now()
# print(now.time)
# print(now.date)
#
# print(now.year)
# print(now.month)
# print(now.day)
#
# print(now.hour)
# print(now.minute)
# print(now.second)

if __name__ == '__main__':
    errorCodes = []
    with open('../log/ppd-2022-07-31.log') as f:
        lines = f.readlines()
        for line in lines:
            # print(line)
            # print(code_str)
            try:
                code_str = line.split("'")[-2:-1][0]
                code_int = int(code_str)
                errorCodes.append(code_str)
            except Exception as exp:
                print(exp)
    print(errorCodes)
