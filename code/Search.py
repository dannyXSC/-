import csv
import time
from typing import List

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

base_url = "https://patentscope.wipo.int/search/en/result.jsf?query=IC:"
# 进入初始search页面要等待的时间(s)
BEGIN_SLEEP = 5
# 每个子页面要等待的时间(s)
EACH_SLEEP = 1


# 入口
def search(IPC_no, driver: WebDriver, output_path="./result.csv"):
    """
    用来获得search页面的信息，根据IPC号获得所有中国地区的信息
    :param IPC_no: IPC号
    :param driver: selenium的任意webdriver
    :param output_path: 输出文件路径
    :return:
    """
    url = "{}\"{}\"".format(base_url, IPC_no)
    driver.get(url)
    # 准备工作，设置中国地区
    prepare(driver)
    # 获得总的页数
    totalPage = getPageNumber(driver)

    infos = []
    # 对于每一页
    for i in range(totalPage):
        print("cur:{}  total:{}".format(i, totalPage))
        cur_page_infos = getPageInfo(driver)
        infos.extend(cur_page_infos)
        goto_next_page(driver)

    output_path = output_path
    output_csv([item.serialization() for item in infos], output_path)


# 保存专利的信息
class Pattern(object):
    def __init__(self, pattern_number="", title="", pubdate="", ipc="", appl_no="", applicant="", inventor=""):
        self.pattern_number = pattern_number
        self.title = title
        self.pubdate = pubdate
        self.ipc = ipc
        self.appl_no = appl_no
        self.applicant = applicant
        self.inventor = inventor

    def set_pattern_number(self, pattern_number):
        self.pattern_number = pattern_number

    def set_title(self, title):
        self.title = title

    def set_pubdate(self, pubdate):
        self.pubdate = pubdate

    def set_ipc(self, ipc):
        self.ipc = ipc

    def set_appl_no(self, appl_no):
        self.appl_no = appl_no

    def set_applicant(self, applicant):
        self.applicant = applicant

    def set_inventor(self, inventor):
        self.inventor = inventor

    def serialization(self):
        return {"pattern_number": self.pattern_number,
                "title": self.title,
                "pubdate": self.pubdate,
                "ipc": self.ipc,
                "appl_no": self.appl_no,
                "applicant": self.applicant,
                "inventor": self.inventor}


def goto_next_page(driver: WebDriver):
    element = driver.find_elements_by_class_name("chevron-right-icon")[0]
    if is_loaded(driver):
        element.click()
    time.sleep(EACH_SLEEP)


def output_csv(dict_list: List[dict], output_path):
    keys = dict_list[0].keys()

    with open(output_path, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(dict_list)


def getPageInfo(driver: WebDriver) -> List[Pattern]:
    infos = []
    cells = getPageCell(driver)
    for cell in cells:
        pattern = getCellInfo(cell)
        print(pattern.serialization())
        infos.append(pattern)
    return infos


def getCellInfo(element: WebElement) -> Pattern:
    pattern_number = element.find_elements_by_class_name("ps-patent-result--title--patent-number")[0].text.strip()
    title = element.find_elements_by_class_name("ps-patent-result--title--title")[0].text.strip()
    pubdate = element.find_elements_by_class_name("ps-patent-result--title--ctr-pubdate")[0].text.strip()
    ipc = element.find_elements_by_class_name("ps-patent-result--ipc")[0].text.strip()
    return Pattern(pattern_number=pattern_number, title=title, pubdate=pubdate, ipc=ipc)


def getPageCell(driver: WebDriver):
    element = driver.find_element_by_id("resultListForm:resultTable_data")
    cells = element.find_elements_by_tag_name("tr")
    return cells


def getPageNumber(driver: WebDriver):
    elements = driver.find_elements_by_class_name("ps-paginator--page--value")
    text = elements[0].text
    # 当前的页号，一般是1
    curPage = int(text[:text.find("/")].strip().replace(",", ""))
    totalPage = int(text[text.find("/") + 1:].strip().replace(",", ""))
    return totalPage


def prepare(driver: WebDriver):
    result = driver.find_elements_by_class_name("ps-field--label")[0]
    result.click()
    window = driver.find_elements_by_class_name("ps-office--input")[0]
    window.click()
    result = driver.find_elements_by_class_name("ps-office--options--item")
    for item in result:
        if item.text.find("China") != -1:
            item.find_elements_by_tag_name("input")[0].click()
            break

    # 搜索
    for item in driver.find_elements_by_class_name("b-button.b-button--is-type_primary"):
        if item.text.find("Search") != -1:
            item.click()
            break
    time.sleep(BEGIN_SLEEP)


def is_loaded(driver: WebDriver):
    return driver.find_element_by_id("pageBlockUI_blocker").is_displayed()
