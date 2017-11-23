class NodeService:
    def __init__(self, soup_1, soup_2):
        self.soup_1 = soup_1
        self.soup_2 = soup_2
        self.nodes = []

    def make(self):
        id_list = []
        for item in self.soup_1.find_all('li', class_='_itemSection'):
            delivery = str(item.find('span', class_='ico_del').next).replace(',', '')
            if delivery == '무료배송':
                delivery = '0'
            elif delivery == '착불':
                delivery = '3000'
            tmp = {
                'id': int(item.get('data-nv-mid')),
                'name': str(item.find('span', class_='info_tit').find(text=True)),
                'price': int(
                    str(item.find('span', class_='price').findChildren(recursive=False)[0].next).replace(',', '')),
                'mall': str(item.find('span', class_='mall').find(text=True)),
                'delivery': int(delivery),
                'npay': 0
            }
            if item.find('span', class_='ico_npay') is not None:
                tmp['npay'] = 1
            self.nodes.append(tmp)
            id_list.append(tmp['id'])

        for item in self.soup_2.find_all('li', class_='_itemSection'):
            n_id = int(item.get('data-nv-mid'))
            if n_id in id_list:
                continue
            delivery = str(item.find('span', class_='ico_del').next).replace(',', '')
            price = int(
                str(item.find('span', class_='price').findChildren(recursive=False)[0].next).replace(',', ''))
            if delivery == '무료배송':
                delivery = 0
            elif delivery == '착불':
                delivery = 3000
            else:
                price = price - int(delivery)
            if n_id in id_list:
                continue
            tmp = {
                'id': n_id,
                'name': str(item.find('span', class_='info_tit').find(text=True)),
                'price': price,
                'mall': str(item.find('span', class_='mall').find(text=True)),
                'delivery': delivery,
                'npay': 0
            }
            if item.find('span', class_='ico_npay') is not None:
                tmp['npay'] = 1
            self.nodes.append(tmp)
