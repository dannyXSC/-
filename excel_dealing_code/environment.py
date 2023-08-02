import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
base_path = r"E:\绿色专利（房东）\incopat"
save_path = r"E:\绿色专利结果"
wipo_json_path = os.path.join(ROOT_DIR, "IPC_Dataset/result.json")
base_path_list = [r"E:\绿色专利数据\2012-2015专利\2012\04"]

green_cnt_log_file = os.path.join(ROOT_DIR, "output/cnt_log.txt")
LOG_file = os.path.join(ROOT_DIR, "output/log.txt")