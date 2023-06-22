from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from Inventory import get_info

from Search import search

# driver_path = "D:\\web_driver\\chromedriver\\chromedriver.exe"
driver_path = "/Users/xiesicheng/Desktop/OpenSource/chromedriver/chromedriver"

driver = webdriver.Chrome(executable_path=driver_path)
try:
    search("F02C 3/28", driver)
    input()
finally:
    driver.quit()
