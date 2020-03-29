import requests
import json
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import NetworkConfig
import re

def getMacList(ip,password):
    ss = requests.session()
    html = ss.post('http://{}/'.format(ip), auth=('root', password)).text
    print(html)
    html = ss.get('http://{}/status-devices.asp'.format(ip)).text
    print(html)
    # macString = '[' + re.findall("var ipmonitor = \[(.*)\]", html)[0] + ']'
    # temp_macList = json.loads(macString)
    # macList = []
    # for i in temp_macList:
    #     mac = str(i[1]).upper().replace(":","-")
    #     macList.append(mac)
    # return macList



if __name__ == '__main__':
    print()
    getMacList("192.168.1.1","tomato.org.cn")
    # macList = re.findall('"(.{17})"',macString)
    # print(macString)
    # print(len(macList))