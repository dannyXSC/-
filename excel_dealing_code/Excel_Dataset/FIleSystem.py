import os


def get_data_list(base_path):
    data_path_list = []

    for parent, dirnames, filenames in os.walk(base_path):
        cur_path = os.path.join(base_path, parent)
        for file_name in filenames:
            if file_name.find(".xlsx") != -1 or file_name.find(".xls") != -1:
                file_path = os.path.join(cur_path, file_name)
                data_path_list.append(file_path)
    return data_path_list
