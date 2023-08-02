import json
from environment import wipo_json_path

IPC_info = []

with open(wipo_json_path) as f:
    raw_IPC_info = json.load(f)


def get_n_layer_IPC(dictionary: dict, layer, cur_layer=0):
    name = dictionary["name"]
    children = dictionary["children"]
    IPC_list = dictionary["IPC_list"]
    children_number = len(children)
    ipc_number = len(IPC_list)

    if cur_layer < layer:
        if children_number == 0:
            IPC_info.append({"name": name, "no": IPC_list})
        else:
            for child in children:
                get_n_layer_IPC(child, layer, cur_layer + 1)
        return []

    # else
    total_IPC_list = IPC_list
    for child in children:
        total_IPC_list.extend(get_n_layer_IPC(child, layer, cur_layer + 1))

    if layer == cur_layer:
        # 假如就是所需层的，就直接加入
        IPC_info.append({"name": name, "no": total_IPC_list})
        return []
    else:
        return total_IPC_list


get_n_layer_IPC(raw_IPC_info, 3)

IPC_category_list = [item["name"] for item in IPC_info]

perfect_match_dict = {}
prefix_match_dict = {}

category_number = len(IPC_info)
for i in range(category_number):
    name = IPC_info[i]["name"]
    for ipc_no in IPC_info[i]["no"]:
        ipc_no = ipc_no.replace(" ", "")
        if ipc_no.find("/") == -1:
            if ipc_no not in prefix_match_dict:
                prefix_match_dict[ipc_no] = []
            prefix_match_dict[ipc_no].append(i)
        else:
            if ipc_no not in perfect_match_dict:
                perfect_match_dict[ipc_no] = []
            perfect_match_dict[ipc_no].append(i)


def IPC_list_to_index_list(ipc_list):
    def find_right_first_character(s):
        length = len(s)
        for i in range(length - 1, -1, -1):
            if ("A" <= s[i] <= "Z") or ("a" <= s[i] <= "z"):
                return i
        return -1

    index_dict = {item: 0 for item in IPC_category_list}
    index_dict["unknown"] = 0
    cnt = 0
    for ipc_no in ipc_list:
        prefix = ipc_no[:find_right_first_character(ipc_no) + 1]
        cur_cnt = 0
        if prefix in prefix_match_dict:
            for idx in prefix_match_dict[prefix]:
                index_dict[IPC_category_list[idx]] = 1
                cur_cnt += 1
        if ipc_no in perfect_match_dict:
            for idx in perfect_match_dict[ipc_no]:
                index_dict[IPC_category_list[idx]] = 1
                cur_cnt += 1
        if cur_cnt == 0:
            index_dict["unknown"] = 1
        cnt += cur_cnt
    if cnt > 0:
        cnt = 1
    return index_dict, cnt
