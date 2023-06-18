from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from Inventory import get_info

driver_path = "D:\\web_driver\\chromedriver\\chromedriver.exe"
database_url = "https://patentscope.wipo.int/search/en/result.jsf?query=IC:%22F02C%203/28%22"

driver = webdriver.Chrome(executable_path=driver_path)
try:
    # text = driver.find_element_by_class_name("b-step__content-bottom").text
    # print(text)
    driver.get(database_url)
    result = driver.find_elements_by_class_name("ps-field--label")[0]
    result.click()
    window = driver.find_elements_by_class_name("ps-office--input")[0]
    window.click()
    result = driver.find_elements_by_class_name("ps-office--options--item")
    for item in result:
        print(item.text)
        if item.text.find("China") != -1:
            item.find_elements_by_tag_name("input")[0].click()
            break

    # 搜索
    for item in driver.find_elements_by_class_name("b-button.b-button--is-type_primary"):
        if item.text.find("Search") != -1:
            print(item.text)
            item.click()
    input()
finally:
    driver.quit()
