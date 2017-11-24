from pybin.mid.node import NodeService
from pybin.mid.other import OtherService
import requests
import socket
from bs4 import BeautifulSoup, SoupStrainer

URL = 'http://shopping.naver.com/detail/detail.nhn'
URL_2 = 'http://m.shopping.naver.com/detail/price_compare_list_area.nhn'


class DataService:
    def __init__(self, info):
        self.data = []
        self.id = info['id']
        self.mid = info['mid']
        self.agent = str(socket.gethostname())

    def make(self):
        header = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 7.0; SAMSUNG SM-G955U Build/NRD90M) AppleWebKit/537.36 (KHTML, '
                          'like Gecko) SamsungBrowser/5.4 Chrome/51.0.2704.106 Mobile Safari/537.36',
            'Accept': 'text / html'
        }
        payload = {
            'nv_mid': self.mid
        }

        other_soup = BeautifulSoup(requests.get(URL, params=payload).text.replace('\n', ''), 'lxml',
                                   parse_only=SoupStrainer('div'))
        other = OtherService(other_soup)
        other.pkey()
        if other.pkey_list[0] == 300:
            self.data.append({
                'id': self.id,
                'mid': self.mid,
                'cat_id': 0,
                'pkey': 'NA',
                'is_invalid': 1,
                'meta': {
                    'error': '상품이 존재하지 않습니다.'
                }
            })

        elif other.pkey_list[0] == 200:
            other.others()
            payload_2 = {
                'nvMid': self.mid,
                'withFee': False
            }
            req_1 = requests.get(URL_2, headers=header, params=payload_2)
            html_1 = req_1.json()['htReturnValue']['contents'][0]
            soup_1 = BeautifulSoup(html_1, 'lxml', parse_only=SoupStrainer('li', class_='_itemSection'))

            payload_2['withFee'] = True
            req_2 = requests.get(URL_2, headers=header, params=payload_2)
            html_2 = req_2.json()['htReturnValue']['contents'][0]
            soup_2 = BeautifulSoup(html_2, 'lxml', parse_only=SoupStrainer('li', class_='_itemSection'))

            node = NodeService(soup_1, soup_2)
            node.make()
            tmp_data = {
                'cat': other.cat,
                'item_name': other.item_name,
                'count': other.count,
                'nodes': node.nodes,
                'meta': {
                    'cat': other.cat,
                    'thumbnail': other.thumbnail
                }
            }
            self.data.append(tmp_data)

        elif other.pkey_list[0] == 100:
            other.others()
            for item in other.pkey_list[1:]:
                payload_2 = {
                    'nvMid': self.mid,
                    'pkey': item[0],
                    'withFee': False
                }
                req_1 = requests.get(URL_2, headers=header, params=payload_2)
                html_1 = req_1.json()['htReturnValue']['contents'][0]
                soup_1 = BeautifulSoup(html_1, 'lxml', parse_only=SoupStrainer('li', class_='_itemSection'))

                payload_2['withFee'] = True
                req_2 = requests.get(URL_2, headers=header, params=payload_2)
                html_2 = req_2.json()['htReturnValue']['contents'][0]
                soup_2 = BeautifulSoup(html_2, 'lxml', parse_only=SoupStrainer('li', class_='_itemSection'))

                node = NodeService(soup_1, soup_2)
                node.make()
                tmp_data = {
                    'cat': other.cat,
                    'item_name': other.item_name,
                    'option_name': item[1],
                    'pkey': item[0],
                    'count': other.count,
                    'nodes': node.nodes,
                    'meta': {
                        'cat': other.cat,
                        'thumbnail': other.thumbnail
                    }
                }
                self.data.append(tmp_data)
