import requests
from bs4 import BeautifulSoup
from pybin.data import DataService
from pybin.meta import MetaService
import time
import datetime
import json
import os
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
            #chk_ver(r_json['clientVersion'])
            return r_json
        except:
            print('Server is Down')
            time.sleep(10)


def post(info, data_list):
    data = {
        'agent': str(socket.gethostname()),
        'id': info['id'],
        'mid': info['mid'],
        'data': data_list
    }
    while 1:
        try:
            a = requests.post(POST_URL, json=data)
            if a.status_code == 500:
                print(a.text)
            return
        except:
            print('Server is Down')
            time.sleep(10)


def get_pkey(mid):
    work_list = []
    s = requests.Session()
    req = s.get(URL_F + mid)
    html = req.text
    soup = BeautifulSoup(html, 'lxml')
    try:
        valid_txt = soup.find('h3', class_='release').find(text=True)
        if '판매중단' in valid_txt:
            tmp_list = []
            tmp_list.append(mid)
            tmp_list.append(True)
            work_list.append(tmp_list)
            return work_list
        elif '출시예정' in valid_txt:
            tmp_list = []
            tmp_list.append(mid)
            tmp_list.append(True)
            work_list.append(tmp_list)
            return work_list
    except:
        try:
            valid_txt = soup.find('span', class_='g_err_ico').find_next_sibling('h2').find(text=True)
            if '상품이' in valid_txt:
                tmp_list = [mid, True]
                work_list.append(tmp_list)
                return work_list
        except:
            try:
                option_list = soup.find_all('div', class_='condition_group')[1].findChildren(recursive=False)[
                    1].findChildren(recursive=False)
                for item in option_list:
                    tmp = str(item.get('data-filter-value'))
                    if tmp != '':
                        tmp_list = [mid, tmp, str(
                            item.findChildren(recursive=False)[2].findChildren(recursive=False)[1].find(text=True))]
                        work_list.append(tmp_list)
            except:
                tmp_list = [mid, '']
                work_list.append(tmp_list)
            return work_list


def Crawl(work_list):
    if work_list[1] == True:
        data = DataService('', '', work_list[0], '', work_list[1], '')
        data.make()
        try:
            print(data.data.option_name + ' Finish!')
        except:
            print('Finish!')
        return data.data.__dict__
    else:
        s = requests.Session()
        if work_list[1] != '':
            #req_1 = requests.post(URL_F + work_list[0] + URL_M + work_list[1] + URL_T + 'False')
            #req_2 = requests.post(URL_F + work_list[0] + URL_M + work_list[1] + URL_T + 'True')
            req_1 = requests.post(URL_F + work_list[0] + URL_M + work_list[1] + URL_T + 'False', proxies=PROXY)
            req_2 = requests.post(URL_F + work_list[0] + URL_M + work_list[1] + URL_T + 'True', proxies=PROXY)

            html_1 = req_1.text
            soup_1 = BeautifulSoup(html_1, 'lxml')
            html_2 = req_2.text
            soup_2 = BeautifulSoup(html_2, 'lxml')
            meta = MetaService(soup_1)
            meta.make()
            data = DataService(soup_1, soup_2, work_list[0], work_list[2], False, work_list[1])
        else:
            #req_1 = requests.post(URL_F + work_list[0] + URL_T + 'False')
            #req_2 = requests.post(URL_F + work_list[0] + URL_T + 'True')
            req_1 = requests.post(URL_F + work_list[0] + URL_T + 'False', proxies=PROXY)
            req_2 = requests.post(URL_F + work_list[0] + URL_T + 'True', proxies=PROXY)

            html_1 = req_1.text
            soup_1 = BeautifulSoup(html_1, 'lxml')
            html_2 = req_2.text
            soup_2 = BeautifulSoup(html_2, 'lxml')
            meta = MetaService(soup_1)
            meta.make()
            data = DataService(soup_1, soup_2, work_list[0], '', False, '')

        data.data.meta = meta.meta
        data.make()
        try:
            print(data.data.option_name + ' Finish!')
        except:
            print('Finish!')
        return data.data.__dict__


def worker(name):
    while 1:
        try:
            msg = []
            start_time = time.time()
            info = get_MID()

            msg.append("--- start " + info['mid'] + ' ' + name + ' ---')
            print(msg[0])

            data_list = []
            for item in get_pkey(info['mid']):
                data_list.append(Crawl(item))

            cpu_first = psutil.cpu_percent()
            post(info, data_list)

            for data in data_list:
                try:
                    msg.append(data['option_name'] + ' Finish!')
                except:
                    msg.append('Finish!')

            msg.append("--- %s seconds ---" % (time.time() - start_time))
            print(msg[-1])

            #if int(time.time() - start_time) < 5:
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
