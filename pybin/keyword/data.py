from pybin.keyword.node import NodeService
import requests
import socket
from bs4 import BeautifulSoup, SoupStrainer

URL = 'http://shopping.naver.com/search/all.nhn'


class DataService:
    def __init__(self, info):
        self.data = []
        self.id = info['id']
        self.keyword = info['keyword']
        self.agent = str(socket.gethostname())

    def make(self):
        payload = {
            'sort': 'price_asc',
            'query': self.keyword
        }
        soup = BeautifulSoup(requests.get(URL, params=payload).text, 'lxml',
                             parse_only=SoupStrainer('ul', class_='goods_list'))
        nodes = NodeService(soup)
        nodes.make()
        if len(nodes.node_list) == 0:
            self.data.append({
                'id': self.id,
                'keyword': self.keyword,
                'cat_id': 0,
                'pkey': 'NA',
                'is_invalid': 1,
                'meta': {
                    'error': '상품이 존재하지 않습니다.'
                }
            })
        else:
            self.data.append({
                'cat': nodes.node_list[0]['category'],
                'item_name': nodes.node_list[0]['name'],
                'count': len(nodes.node_list),
                'nodes': nodes.node_list,
                'meta': {
                    'cat': nodes.node_list[0]['category'],
                    'thumbnail': soup.find('div', class_='img_area').findChildren(recursive=False)[0].get('href')
                }
            })
