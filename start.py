from pybin.mid.data import DataService as midDS
from pybin.keyword.data import DataService as keyDS
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
PROXY = {'http': 'http://211.138.60.25:80'}
NUM_OF_WORKERS = 4


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


def get_task():
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
            info = get_task()

            if 'mid' in info.keys():
                msg.append("--- start " + info['mid'] + ' ' + name + ' ---')
                print(msg[0])
                data_set = midDS(info)
                data_set.make()
                post(data_set)
                for data in data_set.data:
                    try:
                        msg.append(data['option_name'] + ' Finish!')
                    except:
                        msg.append('Finish!')
            else:
                data_set = keyDS(info)
                msg.append("--- start " + info['keyword'] + ' ' + name + ' ---')
                print(msg[0])
                data_set.make()
                msg.append('Finish!')

            msg.append("--- %s seconds ---" % (time.time() - start_time))
            print(msg[-1])

            # if int(time.time() - start_time) < 5:
            #    msg.append("--- Sleeping For %d Sec ---" % int(5 - int(time.time() - start_time)))
            #    print(msg[-1])
            #    time.sleep(5 - int(time.time() - start_time))
            requests.post(MSG_URL,
                          json={'uuid': str(getnode()), 'msg': msg, 'cpu': psutil.cpu_percent()})
            print('')
        except Exception as e:
            print(e)


if __name__ == '__main__':
    workers = []
    for i in range(0, NUM_OF_WORKERS):
        workers.append(Process(target=worker, args=chr(ord('a') + i)))
    for i in range(0, len(workers)):
        workers[i].start()
    for i in range(0, len(workers)):
        workers[i].join()
