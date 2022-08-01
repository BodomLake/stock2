import time

# 处理财报
from bs4 import BeautifulSoup


# 目标url前缀

def processStock(broswer, url, stockCode, stockName):
    # 开始请求的计时
    time_request = time.time()
    # 获取页面
    broswer.get(url)
    print(stockName, '[', stockCode, ']', ':Url-Request Time Cost', time.time() - time_request, 's')
    # 开始计时
    time_start = time.time()

    # 切换iframe 以保证准确定位
    #  http://basic.10jqka.com.cn 这个地址比较干净，没有那么多<frame>，根本不需要定位frame
    # 如果是 http://stockpage.10jqka.com.cn/ 就有至少3个<frame>，需要定位frame，否者无法找到指定的 #document.body
    # try:
    #     broswer.switch_to.frame('dataifm')
    # except Exception as ex:
    #     print(ex)
    #     return {};
    # 获取财务报表所有的表的类型
    sideNav = broswer.find_elements_by_xpath('//*[@class="newTab"]/li')

    # 要插入mongodb的大对象（对应一个股票的所有财报）
    insertData = {
        "name": stockName,
        "code": stockCode,
        "tables": [],
    }

    # 循环每一张财报；从主要指标表开始
    for report_type in range(0, len(sideNav)):

        # 当前报表名称
        report_statement_type = sideNav[report_type].text
        print('Current Finance Report Statement:', report_statement_type)

        # 导航栏中的当前链接
        sheet_href = sideNav[report_type].find_element_by_tag_name('a')

        html = BeautifulSoup(broswer.page_source, 'lxml')
        left_div = html.select(".left_thead")
        # 各项指标
        indicators = BeautifulSoup(str(left_div), 'lxml').select('th')
        indicators.pop(0)
        indicatorsNum = len(indicators)
        # for indicator in indicators:
        # print(indicator.text)

        # 数据表格<table>
        # 包含 报告期
        # 包含报告期下的各个财务数据
        right_div = html.select('.data_tbody')
        data_and_periods = BeautifulSoup(str(right_div), 'lxml')
        periods_table = data_and_periods.select('.top_thead')
        periods = BeautifulSoup(str(periods_table[0]), 'lxml').find_all('div', class_='td_w')

        # 数据表格
        data_table = data_and_periods.select('.tbody')
        # 整个表格的数据
        dataGrid = BeautifulSoup(str(data_table), 'lxml').select('tr')

        # 处理数据，存入数据库
        data = []
        # 处理每一行
        for y in range(0, len(indicators)):
            for x in range(0, len(periods)):
                # 当前表格单元的文字
                cell_text = (dataGrid[y].contents[x].text).strip()
                # 默认单位是：''
                unit = ''
                # 默认值是小数：0.0
                value = 0.0
                if cell_text != '--' and cell_text != '':
                    lastChar = list(cell_text)[-1]
                    if lastChar == '亿' or lastChar == '万' or lastChar == '%':
                        unit = lastChar
                        lastTwoChars = cell_text[len(cell_text) - 2:len(cell_text)]
                        if lastTwoChars == '万亿' or lastTwoChars == '千亿':
                            value = float(cell_text[0:-2])
                            unit = lastTwoChars
                        else:
                            value = float(cell_text[0:-1])
                obj = {
                    "period": periods[x].text,
                    "indicator": indicators[y].text,
                    "text": cell_text,
                    "value": value,
                    "unit": unit
                }
                data.append(obj)
        # 插入当前一列

        # 要插入mongodb 的报表对象
        table = {
            "name": report_statement_type,
            "indicators": list(map(lambda x: x.text, indicators)),
            "periods": list(map(lambda x: x.text, periods)),
            "data": data
        }
        # 向大对象中加入当前报表数据
        insertData['tables'].append(table)

        # 默认table还没有刷新
        refreshFlag = False

        # 试图切换表格
        try:
            # 如果不是最后一页，就切换表格！
            if report_type < len(sideNav) - 1:
                # 点击导航栏中的下一个链接
                sideNav[report_type + 1].find_element_by_tag_name('a').click()
                time.sleep(0.1)
                while not refreshFlag:
                    new_left_div = BeautifulSoup(broswer.page_source, 'lxml').select(".left_thead")
                    nextIndicatorSum = BeautifulSoup(str(new_left_div), 'lxml').select('th')
                    refreshFlag = indicatorsNum != len(nextIndicatorSum)
        except Exception as ex:
            print('出现问题了:', ex)
        finally:
            print(sheet_href.text, '输出完毕')

    # 打印结束信息
    print(stockName, '[', stockCode, ']', ':Data-Handle Time Cost', time.time() - time_start, 's')
    print("=======================================")
    return insertData;

