from bs4 import BeautifulSoup
from Crawling.item import data
from Crawling.mk_node import mk_node
from Crawling.mk_meta import mk_meta

class mk_data():
    def __init__(self, html_1, html_2, mid, option):
        self.data = data()
        self.source_1 = html_1
        self.source_2 = html_2
        self.mid = mid
        self.option = option

    def make(self):
        #meta 생성
        meta = mk_meta(self.source_1)
        meta.make()
        self.data.meta = meta.meta

        #node 생성
        nodes = mk_node(self.source_1, self.source_2)
        nodes.make()
        nodes_json = ''
        self.data.nodes = nodes.node_list

        self.data.id = self.mid
        self.data.mid = self.mid
        self.data.cat_id = meta.meta.cat_id

        soup = BeautifulSoup(self.source_1, 'html.parser')
        self.data.pkey = soup.find('li', class_='on').get('data-filter-value')

        self.data.cat = meta.meta.cat
        self.data.count = meta.meta.compare_count
        self.data.item_name = str(soup.find('div', class_='h_area').findChildren(recursive=False)[0].find(text=True)).replace('\n', '').strip()
        self.data.option_name = self.option
