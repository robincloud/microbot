from pybin.item import Meta
from pybin.category import CategoryService


class MetaService:
    def __init__(self, soup):
        self.meta = Meta()
        self.soup = soup
        self.cat = []

    def make(self):
        # 카테고리 리스트 생성
        cat = CategoryService(self.soup)
        cat.make()
        self.cat = cat.cat

        category = ''
        for item in self.cat:
            category = category + item['name'] + '>'
        category = category[:-1]
        self.meta.cat = category
        detail = self.soup.find('div', id='snb').findChildren(recursive=False)[0].findChildren(recursive=False)

        # 몰 겟수 가져오기
        compare_count = str(detail[0].findChildren(recursive=False)[0].findChildren(recursive=False)[1].find(text=True))
        try:
            compare_count.replace(',', '')
            self.meta.compare_count = int(compare_count.replace(',', ''))
        except:
            self.meta.compare_count = int(compare_count.replace(',', ''))
        # 썸네일 가져오기
        self.meta.thumbnail = self.soup.find('img', id='viewImage').get('src')

        self.meta = self.meta.__dict__
