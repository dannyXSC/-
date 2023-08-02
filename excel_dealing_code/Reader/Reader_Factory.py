from Reader.Reader import Reader
from Reader.XLSX_Reader import XLSX_Reader
from Reader.XLS_Reader import XLS_Reader


def get_excel_reader(file_name) -> Reader:
    if file_name.find("xlsx") != -1:
        return XLSX_Reader(file_name)
    else:
        return XLS_Reader(file_name)
