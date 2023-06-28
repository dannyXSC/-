import os

from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from Inventory import get_info, Inventory

from Search import search
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

driver_path = "D:\\web_driver\\chromedriver\\chromedriver.exe"
# driver_path = "/Users/xiesicheng/Desktop/OpenSource/chromedriver/chromedriver"
driver = webdriver.Chrome(executable_path=driver_path)

save_root_path = "C:\\资源\\green"


def search_inventory(inv: Inventory, dri: WebDriver, pre_path=save_root_path):
    cur_name = inv.name
    cur_path = os.path.join(pre_path, cur_name)
    if not os.path.exists(cur_path):
        os.makedirs(cur_path)
    for ipc in inv.IPC_list:
        search(ipc, driver, os.path.join(cur_path, ipc + ".csv"))
    for child in inv.children:
        search_inventory(child, driver, cur_path)


# driver = webdriver.Chrome()
try:
    # # 获得所有的IPC号
    # inventory = get_info(driver, "./IPC_result.txt")
    # # 根据一个IPC号获得所有的信息
    # search_inventory(inventory, driver)
    search('C10L 5/00', driver, os.path.join("1.csv"))
    input()
except Exception:
    input()
finally:
    driver.quit()
