import requests
from requests.adapters import HTTPAdapter
import json
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import NetworkConfig
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as Wait
from selenium.webdriver.support import expected_conditions as Expect
from selenium.webdriver.chrome.options import Options
import time
from selenium import webdriver
import traceback


class BaseModel:
    ss = requests.session()
    def __init__(self,ip,username='root',password='root'):
        self.ss.mount("http://",HTTPAdapter(max_retries=3))
        self.ip = "http://"+ip
        self.username = username
        self.password = password

    def check_connect(self):
        try:
            web_return = requests.get(self.ip,timeout=60).text
            return True
        except requests.exceptions.RequestException as e:
            print("连接错误：",str(e))
            return False

    def login(self):
        pass

    def check_loggined(self):
        pass

    def get_mac_list(self):
        pass

    def run(self):
        if self.check_connect():
            try:
                if self.check_loggined():
                    mac_list = self.get_mac_list()
                else:
                    self.login()
                    mac_list = self.get_mac_list()
            except:
                print("登录错误:",traceback.print_exc())
                return False
        else:
            return False
        return mac_list

class TpLink(BaseModel):
    stok = ""
    def login(self):
        Login_Data = {
            "login": {
                "password": self.password
            },
            "method": "do"
        }
        self.stok = self.ss.post(self.ip, json=Login_Data,timeout=60).json().get("stok")
        self.send_url = self.ip + "/stok={}/ds".format(self.stok)

    def check_loggined(self):
        if self.stok == "":
            return False
        data = {
            "method": "get"
        }
        error_code = self.ss.post(self.send_url,json=data,timeout=60).json().get('error_code')
        if error_code==0:
            return True
        else:
            return False

    def get_mac_list(self):
        get_mac_data = {
            "hosts_info": {
                "table": [
                    "online_host",
                ]
            },
            "method": "get"
        }
        mac_data = self.ss.post(self.send_url, json=get_mac_data,timeout=60).json()
        mac_iter = mac_data.get('hosts_info').get('online_host')
        mac_list = []
        for m in mac_iter:
            for key, values in m.items():
                mac = str(values.get('mac')).upper()
                mac_list.append(mac)
        return mac_list

class Huawei(BaseModel):
    def login(self):
        # chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
        # chrome_options.add_argument('window-size=1920x3000')  # 指定浏览器分辨率
        # chrome_options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
        # chrome_options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
        # chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # chrome_options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
        # chromedriver = "/usr/bin/chromedriver"
        # driver = webdriver.Chrome(chrome_options=chrome_options,executable_path=chromedriver)
        # driver.get(self.ip+'/html/index.html#/login')
        options = webdriver.FirefoxOptions()
        options.add_argument('-headless')
        driver = webdriver.Firefox(options=options)
        driver.get(self.ip)
        Wait(driver, 300).until(
            Expect.presence_of_element_located((By.ID, "userpassword_ctrl"))
        )
        driver.find_element_by_id('userpassword_ctrl').send_keys(self.password)
        driver.find_element_by_id('loginbtn').click()
        Wait(driver, 300).until(
            Expect.presence_of_element_located((By.ID, "devicecontrol"))
        )
        cookie = driver.get_cookies()
        driver.close()
        for cook in cookie:
            self.ss.cookies.set(name=cook.get('name'),value=cook.get('value'))

    def check_loggined(self):
        re = self.ss.get(self.ip+'/api/system/HostInfo',timeout=60).text
        if re=='':
            return False
        else:
            return True

    def get_mac_list(self):
        re = self.ss.get(self.ip+'/api/system/HostInfo',timeout=60).json()
        mac_list=[]
        for item in re:
            if item.get('Active') is True:
                mac_list.append(str(item.get('MACAddress')).upper().replace(':','-'))
        return mac_list

if __name__ == '__main__':
    print(Huawei('192.168.3.1',password='').run())
    # options = webdriver.FirefoxOptions()
    # options.add_argument('-headless')
    # browser = webdriver.Firefox(options=options)
    # browser.get('http://192.168.3.1')
    # time.sleep(2)
    # print(browser.page_source)