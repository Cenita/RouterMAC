import route
import NetworkConfig
import datetime
import time
import threading
import requests
import json
from requests.adapters import HTTPAdapter
#@
#主线程启动
#@
Header = {"Content-Type": "application/json"}
def run_timer_count():
    ss = requests.session()
    ss.mount("http://", HTTPAdapter(max_retries=3))
    network_route = route.Huawei('192.168.3.1', password='')
    while True:
        #获得当前小时，0点-7点不计时，停止服务
        now_hours = datetime.datetime.now().hour
        if now_hours>24 or now_hours<=7:
            continue
        time1 = time.time()
        #获得该地址的MAC地址链接
        tp = network_route.run()
        if tp is False:
            print("route error")
            continue
        mac_list = tp
        try:
            data = requests.post(headers=Header,data=json.dumps({"macList":mac_list}),url=NetworkConfig.SENDURL+'addTime',timeout=5).json()
            print(data)
        except Exception:
            print('network error')
        time2 = time.time()
        interval = int(time2-time1)
        print('reduce_time:',interval)
        time.sleep(60-min(60,interval))



if __name__ == '__main__':
    main_thread = threading.Thread(target=run_timer_count)
    main_thread.start()

