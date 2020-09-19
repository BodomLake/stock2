from selenium import webdriver
from config.config import *

# 启动浏览器
def launchChrome():
    # 获取chrome浏览器的所有可选项
    options = webdriver.ChromeOptions()
    # 设置window.navigator.webdriver为false
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    # 谷歌文档提到需要加上这个属性来规避bug
    options.add_argument('--disable-gpu')
    # 禁止加载图片
    options.add_argument('blink-settings=imagesEnabled=false')
    # 浏览器不提供可视化页面
    options.add_argument('--headless')
    # 伪装为手机请求头
    options.add_argument(phoneHead)

    # google浏览器
    explorer = webdriver.Chrome(executable_path=driverpath, options=options)
    return explorer
