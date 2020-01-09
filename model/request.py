import requests
import json
from setting.external_setting import sid_address, device_info_address, device_passwd, device_username


def get_device_request_SID(username, password):
    if not (username and password):
        return ""
    try:
        r = requests.post("http://" + sid_address + "/login/?username=" + username + "&password=" + password)
        sidinfo = r.json()
        print("check_result:", sidinfo)
        if sidinfo['type'] == 0:
            return sidinfo["SID"]
    except Exception as e:
        print(e)
    return ""


def get_deviceinfos(iplist):
    # print(iplist)
    size = len(iplist)
    result = [""] * size
    SID = get_device_request_SID(device_username, device_passwd)
    try:
        cursor = 0
        page_index = 1
        while cursor < size:
            r = requests.get(
                "http://" + device_info_address + "/api/asset/query_node_properties/?iplist=" + json.dumps(iplist)
                + "&page_index=" + str(page_index) + "&SID=" + SID)
            r = r.json()
            if r["code"] == 200:
                data = r["Data"]
                for d in data:
                    # result[cursor] = json.dumps(d, indent=4, ensure_ascii=False)
                    result[cursor] = d["device_type"]
                    cursor += 1
                page_index += 1
            else:
                break
    except Exception as e:
        print(e)
    return result
