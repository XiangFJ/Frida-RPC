#!/usr/bin/env python
# _*_ coding:UTF-8 _*_

import requests
import threading

data = {
    "query": "GET /mapi/shop.bin __skck=8f5973b085446090f224af74e30e0181&__skno=8b4a01f5-9bde-4c55-b4aa-ddb6b11fc3b6&__skts=1600930445&__skua=8d61c10bc781eae280782b869d6b2f39&__skvs=1.1&clientuuid=8c9fc2ad-65a3-455d-be3e-e7bf58fb1732&lat=31.23023&lng=129.42543&shopid=1496952723&shopuuid=l7MFkURDg5UpcaC5"
}

url = "http://192.168.1.69:5000/skcy"
url1 = "http://192.168.1.69:5000/index"



def target():
    while True:
        try:
            res = requests.post(url=url, json=data, headers={"Connection": "close"}, timeout=2)
            # res = requests.get(url=url1)
            print(res.json())
        except Exception as e:
            print(e)

threads = []
for i in range(0, 10):
    thread = threading.Thread(target=target)
    threads.append(thread)
    thread.start()
for thread in threads:
    thread.join()

