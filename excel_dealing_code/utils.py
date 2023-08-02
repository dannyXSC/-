import csv
import os

from environment import LOG_file


def list_dict_to_csv(path, list_dict, if_delete=False):
    # 做处理，去除\t \n
    for dictionary in list_dict:
        for key, value in dictionary.items():
            if type(value) is str:
                dictionary[key] = value.replace("\t", "").replace("\n", "")

    if (not os.path.exists(path)) or (if_delete is True):
        list_dict_create_csv(path, list_dict)
    else:
        list_dict_append_to_csv(path, list_dict)


def list_dict_create_csv(path, list_dict):
    keys = list_dict[0].keys()

    with open(path, 'w', newline='', encoding="utf8") as output_file:
        dict_writer = csv.DictWriter(output_file, keys, delimiter="\t")
        dict_writer.writeheader()
        dict_writer.writerows(list_dict)


def list_dict_append_to_csv(path, list_dict):
    keys = list_dict[0].keys()

    with open(path, 'a', newline='', encoding="utf8") as output_file:
        dict_writer = csv.DictWriter(output_file, keys, delimiter="\t")
        dict_writer.writerows(list_dict)


PRINT_TAG = 1


def MY_DEBUG(txt):
    if PRINT_TAG:
        print(txt)


def LOG(txt, path=LOG_file):
    with open(path, "a") as f:
        f.write(txt + "\n")


if __name__ == "__main__":
    a = "B01D15/00,B01D46/00,B01D53/00,B01J20/00,G01N30/00"

    l = a.replace(" ", "").replace("\n", "").split(",")
    cnt = 0
    for item in l:
        print("\"{}\",".format(item), end="")
        cnt += 1
        if cnt % 4 == 0:
            cnt = 0
            print()
