from Crawling.item import data
from Crawling.mk_node import mk_node


class mk_data():
    def __init__(self, soup_1, soup_2, mid, option,  valid):
        self.data = data()
        self.soup_1 = soup_1
        self.soup_2 = soup_2
        self.mid = mid
        self.option = option
        self.valid = valid

    def make(self):
        if not self.valid:
            # node 생성
            nodes = mk_node(self.soup_1, self.soup_2)
            nodes.make()
            self.data.nodes = nodes.node_list

            self.data.id = self.mid
            self.data.mid = self.mid
            self.data.cat_id = self.data.meta['cat_id']

            self.data.pkey = self.soup_1.find('li', class_='on').get('data-filter-value')

            self.data.cat = self.data.meta['cat']
            self.data.count = self.data.meta['compare_count']
            self.data.item_name = str(
                self.soup_1.find('div', class_='h_area').findChildren(recursive=False)[0].find(text=True)).replace('\n',
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
