import requests
import json
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import NetworkConfig
import re

def getMacList(ip,password):
    html = requests.get('http://{}/device-map/clients.asp'.format(ip), auth=('admin', password)).text
    macString = '[' + re.findall("var ipmonitor = \[(.*)\]", html)[0] + ']'
    temp_macList = json.loads(macString)
    macList = []
    for i in temp_macList:
        mac = str(i[1]).upper().replace(":","-")
        macList.append(mac)
    return macList



if __name__ == '__main__':
    print()
    # macList = re.findall('"(.{17})"',macString)
    # print(macString)
    # print(len(macList))