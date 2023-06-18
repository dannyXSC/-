import time
from typing import List

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

category_url = "https://www.wipo.int/classifications/ipc/green-inventory/home"


class Inventory(object):
    def __init__(self, name="", children=None, IPC_list=None):
        self.name = name
        self.children = children if children is not None else []
        self.IPC_list = IPC_list if IPC_list is not None else []

    def set_name(self, name):
        self.name = name

    def add_child(self, child):
        self.children.append(child)

    def add_IPC(self, IPC_no):
        self.IPC_list.append(IPC_no)

    def serialize(self):
        pass


class Cell(object):
    def __init__(self, element: WebElement):
        self.element = WebElement
        infos = element.find_elements_by_tag_name("td")
        self.name = infos[0].text
        raw_IPC = infos[2].text
        self.IPC_list = []
        # 如果没有内容，就结束
        if raw_IPC.strip() == '':
            return
        # 否则进行处理
        IPC_info = raw_IPC.split("\n")
        for item in IPC_info:
            IPC_begin = item[:item.find(" ")]
            remain = item[item.find(" ") + 1:].split(",")
            remain = [text.strip() for text in remain]
            for no_text in remain:
                if no_text.find("-") == -1:
                    # 没有-，直接加入
                    self.IPC_list.append(IPC_begin + " " + no_text)
                else:
                    # 前缀
                    no_prefix = no_text[:no_text.find("/")]
                    no_remain = no_text.split("-")
                    # 数字起始
                    no_begin = int(no_remain[0][no_remain[0].find("/") + 1:])
                    # 数字结尾
                    no_end = int(no_remain[1][no_remain[1].find("/") + 1:])
                    # 把所有的IPC加入
                    for i in range(no_begin, no_end + 1):
                        self.IPC_list.append("{} {}/{}".format(IPC_begin, no_prefix, i))

    def to_Inventory(self) -> Inventory:
        return Inventory(name=self.name, IPC_list=self.IPC_list)


# 入口
def get_info(driver: WebDriver):
    driver.get(category_url)
    inventory = Inventory()
    body = driver.find_element_by_class_name("p-treetable-tbody")
    get_all_children(element=body, inventory=inventory)

    with open("./result.txt", 'w') as f:
        def MyPrint(txt):
            f.write(txt + '\n')

        output(inventory=inventory, fun=MyPrint)


def get_all_children(element: WebElement, inventory: Inventory, begin=None, end=None):
    inventory_result = get_children(element=element, begin=begin, end=end)
    length = len(inventory_result)
    for i in range(length):
        inventory_item = inventory_result[i]
        inventory.add_child(inventory_item)
        unfold(element, inventory_item)
        get_all_children(element=element, inventory=inventory_item, begin=inventory_item.name,
                         end=end if i == length - 1 else inventory_result[i + 1].name)
        print("{} {} {}".format(inventory_item.name, inventory_item.IPC_list, len(inventory_item.children)))


def unfold(element: WebElement, inventory: Inventory):
    category_list = element.find_elements_by_class_name("node-row")
    cell_list = [Cell(content) for content in category_list]
    length = len(cell_list)
    for i in range(length):
        item = cell_list[i]
        if item.name == inventory.name:
            category_list[i].find_elements_by_class_name("topic-data")[0].click()
            break


def get_children(element: WebElement, begin=None, end=None) -> List[Inventory]:
    category_list = element.find_elements_by_class_name("node-row")
    cell_list = [Cell(content) for content in category_list]
    length = len(cell_list)
    begin_index = 0
    if begin is not None:
        begin_index = length - 1
        while begin_index >= 0 and cell_list[begin_index].name != begin:
            begin_index -= 1
        # 指定begin即要把begin排除
        begin_index += 1
    end_index = length
    if end is not None:
        # 指定了end即要把end也排除
        end_index -= 1
        while end_index >= 0 and cell_list[end_index].name != end:
            end_index -= 1
    inventory_list = []
    for i in range(begin_index, end_index):
        inventory_list.append(cell_list[i].to_Inventory())
    return inventory_list


def output(inventory: Inventory, fun, pretext="", layer=0):
    length = len(inventory.children)
    for i in range(length):
        item = inventory.children[i]
        prefix = pretext + ("." if layer > 0 else "") + str(i)
        fun(prefix + " " + item.name + " " + str(item.IPC_list))
        output(item, fun, prefix, layer + 1)
