import requests
import json
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import NetworkConfig
import re

def getMacList(ip,password):
    ss = requests.session()
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    login_data = {
        "luci_username":"root",
        "luci_password":password
    }
    re = ss.post('http://'+ip+'/cgi-bin/luci/',headers=headers,data=login_data,timeout=1)
    result = ss.post('http://'+ip+'/cgi-bin/luci/?status=1').text
    result = json.loads(result)
    mac_list = result.get('wifinets')[0].get('networks')[0].get('assoclist')
    macList = []
    for key in mac_list:
        macList.append(str(key).upper().replace(":","-"))
    #
    # for user in result[0]:
    #     mac = str(user.get('macaddr')).upper().replace(":","-")
    #     macList.append(mac)
    return macList



if __name__ == '__main__':
    print(getMacList("192.168.1.1",""))
    # macList = re.findall('"(.{17})"',macString)
    # print(macString)
    # print(len(macList))