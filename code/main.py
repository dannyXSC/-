from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from Inventory import get_info

from Search import search

# driver_path = "D:\\web_driver\\chromedriver\\chromedriver.exe"
driver_path = "/Users/xiesicheng/Desktop/OpenSource/chromedriver/chromedriver"
driver = webdriver.Chrome(executable_path=driver_path)

# driver = webdriver.Chrome()
try:
    # # 获得所有的IPC号
    # get_info(driver, "./IPC_result.txt")
    # # 根据一个IPC号获得所有的信息
    # search("F02C 3/28", driver, "F02C 3/28.csv")
    input()
finally:
    driver.quit()
