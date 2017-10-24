from Crawling.item import nods
from bs4 import BeautifulSoup


class mk_node():
    def __init__(self, html_1, html_2):
        self.source_1 = html_1
        self.source_2 = html_2
        self.node_list = []

    def make(self):
        id_list = []
        soup = BeautifulSoup(self.source_1, 'html.parser')
        item_list = soup.find_all('table', class_='tbl tbl_v')
        for item in item_list:
            node = nods()

            # 상품 id가져오기
            node.id = int(item.get('data-ex-nv-mid'))
            id_list.append(node.id)

            # 상품명 가져오기
            node.name = str(
                item.findChildren(recursive=False)[2].findChildren(recursive=False)[0].findChildren(recursive=False)[
                    1].findChildren(recursive=False)[0].find(text=True))

            # 상품 판매처, 네이버 페이 가져오기
            try:
                node.mall = str(
                    item.findChildren(recursive=False)[2].findChildren(recursive=False)[0].findChildren(
                        recursive=False)[0].findChildren(recursive=False)[0].findChildren(recursive=False)[1].find(
                        text=True))
                node.npay = 1
            except:
                node.mall = str(
                    item.findChildren(recursive=False)[2].findChildren(recursive=False)[0].findChildren(
                        recursive=False)[0].findChildren(recursive=False)[0].get('data-mall-name'))
                node.npay = 0

            # 상품가격 가져오기
            price_tmp = \
                item.findChildren(recursive=False)[2].findChildren(recursive=False)[0].findChildren(recursive=False)[
                    2].findChildren(recursive=False)[0].findChildren(recursive=False)
            for tmp in price_tmp:
                tmp_txt = tmp.find(text=True)
                if '최저' in str(tmp_txt):
                    continue
                try:
                    tmp_txt = tmp_txt.replace(',', '')
                    node.price = int(tmp_txt)
                except:
                    node.price = int(tmp_txt)

            # 상품 배송비 가져오기
            tmp = str(
                item.findChildren(recursive=False)[2].findChildren(recursive=False)[0].findChildren(recursive=False)[
                    3].findChildren(recursive=False)[0].find(text=True))[:-1]
            if '무료' in tmp:
                tmp = '0'
            else:
                try:
                    tmp = tmp.replace(',', '')
                    node.delivery = int(tmp)
                except:
                    node.delivery = int(tmp)

            self.node_list.append(node.__dict__)

        soup = BeautifulSoup(self.source_2, 'html.parser')
        item_list = soup.find_all('table', class_='tbl tbl_v')

        for item in item_list:
            node = nods()

            # 상품 id가져오기
            node.id = int(item.get('data-ex-nv-mid'))
            if node.id in id_list:
                continue

            # 상품명 가져오기
            node.name = str(
                item.findChildren(recursive=False)[2].findChildren(recursive=False)[0].findChildren(recursive=False)[
                    1].findChildren(recursive=False)[0].find(text=True))

            # 상품 판매처, 네이버 페이 가져오기
            try:
                node.mall = str(
                    item.findChildren(recursive=False)[2].findChildren(recursive=False)[0].findChildren(
                        recursive=False)[0].findChildren(recursive=False)[0].findChildren(recursive=False)[1].find(
                        text=True))
                node.npay = 1
            except:
                node.mall = str(
                    item.findChildren(recursive=False)[2].findChildren(recursive=False)[0].findChildren(
                        recursive=False)[0].findChildren(recursive=False)[0].get('data-mall-name'))
                node.npay = 0

            # 상품가격 가져오기
            price_tmp = \
                item.findChildren(recursive=False)[2].findChildren(recursive=False)[0].findChildren(recursive=False)[
                    2].findChildren(recursive=False)[0].findChildren(recursive=False)
            for tmp in price_tmp:
                tmp_txt = tmp.find(text=True)
                if '최저' in str(tmp_txt):
                    continue
                try:
                    tmp_txt = tmp_txt.replace(',', '')
                    node.price = int(tmp_txt)
                except:
                    node.price = int(tmp_txt)

            # 상품 배송비 가져오기
            tmp = str(
                item.findChildren(recursive=False)[2].findChildren(recursive=False)[0].findChildren(recursive=False)[
                    3].findChildren(recursive=False)[1].find(text=True))[1:-2]
            if '무료' in tmp:
                node.delivery = 0
            else:
                try:
                    tmp = tmp.replace(',', '')
                    node.delivery = int(tmp)
                except:
                    node.delivery = int(tmp)
