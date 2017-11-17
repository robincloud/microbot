from pybin.item import Data
from pybin.node import NodeService
import socket


class DataService:
    def __init__(self, soup_1, soup_2, mid, option, valid):
        self.data = Data()
        self.soup_1 = soup_1
        self.soup_2 = soup_2
        self.mid = mid
        self.option = option
        self.valid = valid

    def make(self):
        if not self.valid:
            # node 생성
            nodes = NodeService(self.soup_1, self.soup_2)
            nodes.make()
            self.data.nodes = nodes.node_list

            pkey = str(self.soup_1.find('li', class_='on').get('data-filter-value'))
            if pkey != 'None':
                self.data.pkey = pkey
                self.data.option_name = self.option

            self.data.cat = self.data.meta['cat']
            self.data.count = self.data.meta['compare_count']
            self.data.item_name = str(
                self.soup_1.find('div', class_='h_area').findChildren(recursive=False)[0].find(text=True))
            self.data.item_name = self.data.item_name.replace('\n', '').strip()
            self.data.agent = str(socket.gethostname())

        else:
            self.data.id = self.mid
            self.data.mid = self.mid
            self.data.cat_id = 0
            self.data.pkey = 'NA'
            self.data.is_invalid = 1
            self.data.meta['error'] = {'message': '상품이 존재하지 않습니다.',
                                       'text': '일시적으로 상품이 품절되었거나, 노출이 제한된 상품일 수 있습니다.'}
