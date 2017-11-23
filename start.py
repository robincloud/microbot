from pybin.data import DataService
import time
import json
import datetime
import os
import requests
import socket
from uuid import getnode
import psutil
from multiprocessing import Process

GET_URL = 'https://robin-api.oneprice.co.kr/tasks?agent='
POST_URL = 'https://robin-api.oneprice.co.kr/items'
POST_URL_LOCAL = 'http://localhost:8081/items'
DEVICE_URL = 'https://robin-api.oneprice.co.kr/agents/enroll'
MSG_URL = 'https://robin-api.oneprice.co.kr/agents/msg'
URL_F = 'http://shopping.naver.com/detail/detail.nhn?nv_mid='
URL_M = '&pkey='
URL_T = '&withFee='
PROXY = {'http': 'http://211.138.60.25:80'}


def getNowDate():
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day
    hour = now.hour
    minute = now.minute
    nowDate = str(year) + "-" + str(month) + "-" + str(day) + "," + str(hour) + ":" + str(minute)
    return nowDate


def chk_ver(version):
    path = '/home/pi/Microbot'
    data = {}
    try:
        with open(path + '/version.json', "r") as f:
            json_data = f.read()
            data = json.loads(json_data)
        if version != data['version']:
            with open(path + '/version.json', "w") as f:
                data['version'] = version
                data['date'] = getNowDate()
                data['success'] = True
                json.dump(data, f, ensure_ascii=False, indent="\t")
            os._exit(0)
    except Exception as err:
        print(err)
        with open(path + '/version.json', "w") as f:
            data['date'] = getNowDate()
            data['success'] = False
            data['version'] = version
            json.dump(data, f, ensure_ascii=False, indent="\t")


def get_MID():
    while 1:
        try:
            req = requests.get(GET_URL + str(socket.gethostname()))
            r_json = req.json()[0]
            data = {
                'name': str(socket.gethostname()),
                'uuid': str(getnode()),
            }
            requests.post(DEVICE_URL, json=data)
            # chk_ver(r_json['clientVersion'])
            return r_json
        except:
            print('Server is Down')
            time.sleep(10)


def post(data):
    while 1:
        try:
            res = requests.post(POST_URL, json=data.__dict__)
            if res.status_code == 500:
                print(res.text)
            return
        except:
            print('Server is Down')
            time.sleep(10)


def worker(name):
    while 1:
        try:
            msg = []
            start_time = time.time()
            info = get_MID()

            # mid = '10549634158'
            # info = {'id': 'nv_' + mid, 'mid': mid}

            msg.append("--- start " + info['mid'] + ' ' + name + ' ---')
            print(msg[0])

            data_set = DataService(info)
            data_set.make()

            cpu_first = psutil.cpu_percent()
            post(data_set)

            for data in data_set.data:
                try:
                    msg.append(data['option_name'] + ' Finish!')
                except:
                    msg.append('Finish!')

            msg.append("--- %s seconds ---" % (time.time() - start_time))
            print(msg[-1])

            # if int(time.time() - start_time) < 5:
            #    msg.append("--- Sleeping For %d Sec ---" % int(5 - int(time.time() - start_time)))
            #    print(msg[-1])
            #    time.sleep(5 - int(time.time() - start_time))
            requests.post(MSG_URL,
                          json={'uuid': str(getnode()), 'msg': msg, 'cpu': (cpu_first + psutil.cpu_percent()) / 2})
            print('')
        except Exception as e:
            print(e)


if __name__ == '__main__':
    w1 = Process(target=worker, args='a')
    w2 = Process(target=worker, args='b')
    w3 = Process(target=worker, args='c')
    w4 = Process(target=worker, args='d')
    w5 = Process(target=worker, args='e')
    w6 = Process(target=worker, args='f')
    w1.start()
    w2.start()
    w3.start()
    w4.start()
    w5.start()
    w6.start()
    w1.join()
    w2.join()
    w3.join()
    w4.join()
    w5.join()
    w6.join()
