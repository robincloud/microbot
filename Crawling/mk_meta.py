from Crawling.item import meta
from Crawling.mk_cat import mk_cat


class mk_meta():
    def __init__(self, soup):
        self.meta = meta()
        self.soup = soup
        self.cat = []

    def make(self):
        # 카테고리 리스트 생성
        cat = mk_cat(self.soup)
        cat.make()
        self.cat = cat.cat

        category = ''
        for item in self.cat:
            category = category + item['name'] + '>'
        category = category[:-1]
        self.meta.cat = category

        self.meta.cats = self.cat

        self.meta.cat_id = self.cat[self.cat.__len__() - 1]['id']

        detail = self.soup.find('div', id='snb').findChildren(recursive=False)[0].findChildren(recursive=False)

        # 몰 겟수 가져오기
        compare_count = str(detail[0].findChildren(recursive=False)[0].findChildren(recursive=False)[1].find(text=True))
        try:
            compare_count.replace(',', '')
            self.meta.compare_count = int(compare_count.replace(',', ''))
        except:
            self.meta.compare_count = int(compare_count.replace(',', ''))

        # 리뷰 갯수 가져오기
        try:
            review_count = str(
                detail[1].findChildren(recursive=False)[0].findChildren(recursive=False)[1].find(text=True))
        except:
            review_count = str(
                detail[2].findChildren(recursive=False)[0].findChildren(recursive=False)[1].find(text=True))
        try:
            review_count.replace(',', '')
            self.meta.review_count = int(review_count.replace(',', ''))
        except:
            self.meta.review_count = int(review_count.replace(',', ''))

        # info 텍스트 가져오기
        info_list = self.soup.find('div', class_='info_inner').findChildren(recursive=False)[:3]
        text = ''
        for item in info_list:
            text += str(item.find_all(text=True)[0]) + str(item.find_all(text=True)[1]) + ','
        self.meta.infos = text[:-1]

        # 썸네일 가져오기
        self.meta.thumbnail = self.soup.find('img', id='viewImage').get('src')

        # 썸네일 리스트 만들기
        try:
            thumb_list = self.soup.find('ul', class_='_thumb').findChildren(recursive=False)
            for item in thumb_list:
                self.meta.thumbs.append(
                    str(item.findChildren(recursive=False)[0].findChildren(recursive=False)[0].get('src')))
        except:
            self.meta.thumbs.append(self.meta.thumbnail)

        # 찜 갯수 가져오기
        try:
            self.meta.jjim = int(str(self.soup.find('em', class_='cnt _keepCount').find(text=True)).replace(',', ''))
        except:
            self.meta.jjim = int(str(self.soup.find('em', class_='cnt _keepCount').find(text=True)))

        self.meta = self.meta.__dict__
