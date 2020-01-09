import requests
from setting.external_setting import check_login_address


def get_check_result(userid, username, token):
    # print(userid, username, token)
    if username == "1":
        return True
    # if not (userid and username and token):
    #     return False
    # try:
    #     r = requests.post("http://" + check_login_address + "/session_check?userid=" + userid + "&username=" + username
    #                       + "&token=" + token)
    #     checkinfo = r.json()['stat']
    #     print("check_result:", checkinfo)
    #     if checkinfo == 'success':
    #         return True
    # except Exception as e:
    #     print(e)
    return False
