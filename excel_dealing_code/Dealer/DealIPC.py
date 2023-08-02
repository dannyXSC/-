from IPC_Dataset.WipoIPC import IPC_list_to_index_list as Wipo_IPC_list_to_index_list


def deal_ipc(str_ipc_list: str):
    ipc_list = str_ipc_list.replace(" ", "").split(";")
    result, cnt = Wipo_IPC_list_to_index_list(ipc_list)
    return result, cnt
