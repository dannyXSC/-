import os.path

import openpyxl
from openpyxl import load_workbook

from DealFile import deal_xlsx_file, deal_xls_file
from FIleSystem import get_data_list
from GlobalVariable import save_path, base_path_list
from tools import list_dict_to_csv, LOG

data_list = []
for base_path in base_path_list:
    data_list.extend(get_data_list(base_path))

cnt = 0
total_num = len(data_list)
# IPC、时间、地区、专利类型、申请人类型
for file in data_list:
    print("当前处理:{}，已经处理:{}，总共:{}".format(file, str(cnt), str(total_num)))
    try:
        if file.find(".xlsx") != -1:
            data, green_no = deal_xlsx_file(file)
        else:
            data, green_no = deal_xls_file(file)
        save_name = file.replace("\\", "_").replace("/", "_")
        save_name = save_name[:save_name.find(".")] + ".tsv"
        list_dict_to_csv(os.path.join(save_path, save_name), data, True)
    except Exception as e:
        LOG(file)
    finally:
        cnt += 1
