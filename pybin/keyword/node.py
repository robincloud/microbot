class NodeService:
    def __init__(self, soup):
        self.soup = soup
        self.node_list = []

    def make(self):
        item_list = self.soup.find('ul', class_='goods_list').find_all('li', class_='_itemSection')
        if len(item_list) == 0:
            return

        for item in item_list:
            info = item.find('div', class_='info')
            delivery = item.find('ul', class_='mall_option').find('em').text

            if delivery == '배송비 무료':
                delivery = 0
            elif delivery == '착불':
                delivery = 3000
            else:
                delivery = int(delivery[3:-1].replace(',', ''))

            try:
                price = int(info.find('span', class_='num _price_reload').text.replace(',', ''))
            except:
                continue

            self.node_list.append({
                'name': info.find('a', class_='tit').get('title'),
                'price': price,
                'category': info.find_all('a', class_=lambda val: val and 'cat_id' in val)[-1].get('title'),
                'mall': item.find('p', class_='mall_txt').findChildren(recursive=False)[0].text,
                'delivery': delivery

            })
            if len(self.node_list) == 25:
                break
