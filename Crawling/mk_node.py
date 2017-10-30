from Crawling.item import nods


class mk_node():
    def __init__(self, soup_1, soup_2):
        self.soup_1 = soup_1
        self.soup_2 = soup_2
        self.node_list = []

    def make(self):
        id_list = []
        item_list = self.soup_1.find_all('table', class_='tbl tbl_v')
        for item in item_list:
            node = nods()

            # 상품 id가져오기
            node.id = int(item.get('data-ex-nv-mid'))
            id_list.append(node.id)

            # 상품명 가져오기
            node.name = str(
                item.findChildren(recursive=False)[2].findChildren(recursive=False)[1].findChildren(recursive=False)[
                    0].find(text=True))

            # 상품 판매처, 네이버 페이 가져오기
            try:
                node.mall = str(
                    item.findChildren(recursive=False)[2].findChildren(recursive=False)[0].findChildren(
                        recursive=False)[0].findChildren(recursive=False)[1].find(
                        text=True))
                node.npay = 1
            except:
                node.mall = str(
                    item.findChildren(recursive=False)[2].findChildren(recursive=False)[0].findChildren(recursive=False)[0].get('data-mall-name'))
                node.npay = 0

            # 상품가격 가져오기
            price_tmp = \
                item.findChildren(recursive=False)[2].findChildren(recursive=False)[2].findChildren(recursive=False)[
                    0].findChildren(recursive=False)
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
            tmp_deliver = str(
                item.findChildren(recursive=False)[2].findChildren(recursive=False)[
                    3].findChildren(recursive=False)[0].find(text=True))[:-1]
            if '무료' in tmp_deliver:
                tmp_deliver = '0'
            else:
                try:
                    tmp_deliver = tmp_deliver.replace(',', '')
                    node.delivery = int(tmp_deliver)
                except:
                    node.delivery = int(tmp_deliver)

            self.node_list.append(node.__dict__)

        if self.soup_2 != '':
            item_list = self.soup_2.find_all('table', class_='tbl tbl_v')

            for item in item_list:
                node = nods()

                # 상품 id가져오기
                node.id = int(item.get('data-ex-nv-mid'))
                if node.id in id_list:
                    continue

                # 상품명 가져오기
                node.name = str(
                    item.findChildren(recursive=False)[2].findChildren(recursive=False)[1].findChildren(
                        recursive=False)[0].find(text=True))

                # 상품 판매처, 네이버 페이 가져오기
                try:
                    node.mall = str(
                        item.findChildren(recursive=False)[2].findChildren(recursive=False)[0].findChildren(
                            recursive=False)[0].findChildren(recursive=False)[1].find(
                            text=True))
                    node.npay = 1
                except:
                    node.mall = str(
                        item.findChildren(recursive=False)[2].findChildren(recursive=False)[0].findChildren(
                            recursive=False)[0].get('data-mall-name'))
                    node.npay = 0

                # 상품가격 가져오기
                price_tmp = \
                    item.findChildren(recursive=False)[2].findChildren(recursive=False)[2].findChildren(
                        recursive=False)[
                        0].findChildren(recursive=False)
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
                tmp_deliver = str(
                    item.findChildren(recursive=False)[2].findChildren(recursive=False)[
                        3].findChildren(recursive=False)[1].find(text=True))[1:-2]
                if '무료' in tmp_deliver:
                    tmp_deliver = '0'
                else:
                    try:
                        tmp_deliver = tmp_deliver.replace(',', '')
                        node.delivery = int(tmp_deliver)
                    except:
                        node.delivery = int(tmp_deliver)

                self.node_list.append(node.__dict__)
