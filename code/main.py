from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from Inventory import get_info

# driver_path = "D:\\web_driver\\chromedriver\\chromedriver.exe"
from Search import search

driver_path = "/Users/xiesicheng/Desktop/OpenSource/chromedriver/chromedriver"
database_url = "https://patentscope.wipo.int/search/en/result.jsf?query=IC:%22F02C%203/28%22"

driver = webdriver.Chrome(executable_path=driver_path)
try:
    search("F02C 3/28", driver)
    input()
finally:
    driver.quit()
