from bs4 import BeautifulSoup
from Crawling.item import data
from Crawling.mk_node import mk_node
from Crawling.mk_meta import mk_meta


class mk_data():
    def __init__(self, html_1, html_2, mid, option, valid):
        self.data = data()
        self.source_1 = html_1
        self.source_2 = html_2
        self.mid = mid
        self.option = option
        self.valid = valid

    def make(self):
        if not self.valid:
            # meta 생성
            meta = mk_meta(self.source_1)
            meta.make()
            self.data.meta = meta.meta

            # node 생성
            nodes = mk_node(self.source_1, self.source_2)
            nodes.make()
            self.data.nodes = nodes.node_list

            self.data.id = self.mid
            self.data.mid = self.mid
            self.data.cat_id = meta.meta['cat_id']

            soup = BeautifulSoup(self.source_1, 'html.parser')
            self.data.pkey = soup.find('li', class_='on').get('data-filter-value')

            self.data.cat = meta.meta['cat']
            self.data.count = meta.meta['compare_count']
            self.data.item_name = str(
                soup.find('div', class_='h_area').findChildren(recursive=False)[0].find(text=True)).replace('\n',
                                                                                                            '').strip()
            self.data.option_name = self.option

        else:
            self.data.id = self.mid
            self.data.mid = self.mid
            self.data.cat_id = 0
            self.data.pkey = 'NA'
            self.data.is_invalid = 1
            self.data.meta['error'] = {'message': '상품이 존재하지 않습니다.',
                                       'text': '일시적으로 상품이 품절되었거나, 노출이 제한된 상품일 수 있습니다.'}
