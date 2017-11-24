class OtherService:
    def __init__(self, soup):
        self.soup = soup
        self.pkey_list = []
        self.cat = ''
        self.item_name = ''
        self.count = 0
        self.thumbnail = ''

    def pkey(self):
        try:
            valid_txt = self.soup.find('h3', class_='release').find(text=True)
            if '판매중단' in valid_txt or '출시예정' in valid_txt:
                self.pkey_list.append(300)
        except:
            try:
                valid_txt = self.soup.find('span', class_='g_err_ico').find_next_sibling('h2').find(text=True)
                if '상품이' in valid_txt:
                    self.pkey_list.append(300)
            except:
                try:
                    option_list = self.soup.find_all('div', class_='condition_group')[1].findChildren(recursive=False)[
                        1].findChildren(recursive=False)
                    self.pkey_list.append(100)
                    for item in option_list:
                        tmp = str(item.get('data-filter-value'))
                        if tmp != '':
                            tmp_list = [tmp, str(
                                item.findChildren(recursive=False)[2].findChildren(recursive=False)[1].find(
                                    text=True)).strip()]
                            self.pkey_list.append(tmp_list)
                except:
                    self.pkey_list.append(200)

    def others(self):
        self.item_name = str(self.soup.find('div', class_='h_area').find('h2').find(text=True)).strip()
        cat_tmp = self.soup.find_all('span', class_='s_nowrap')
        self.cat = ''
        for item in cat_tmp:
            self.cat += str(item.find('a').find(text=True)) + '>'
        self.cat = self.cat[:-1]

        self.count = int(str(self.soup.find('li', class_='mall_place on').find('em').find(text=True)).replace(',', ''))
        self.thumbnail = str(self.soup.find('img', id='viewImage').get('src'))
