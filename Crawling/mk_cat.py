from Crawling.item import category


class mk_cat():
    def __init__(self, soup):
        self.cat = []
        self.soup = soup

    def make(self):
        wrap = self.soup.find_all('span', class_='s_nowrap')
        depth = 0
        for item in wrap:
            # 객체 생성
            tmp = category()

            # 카테고리 가져오기
            try:
                cat_tag = item.findChildren(recursive=False)[0].findChildren(recursive=False)[0]
            except:
                cat_tag = item.findChildren(recursive=False)[0]

            # 각각 데이터 삽입
            tmp.name = str(cat_tag.find(text=True))
            tmp.depth = depth
            depth += 1
            id = str(cat_tag.get('href'))
            tmp.id = id[id.find('id='):]
            self.cat.append(tmp.__dict__)
