class nods():
    def __init__(self):
        self.id = ''
        self.name = ''
        self.mall = ''
        self.price = 0
        self.delivery = 0
        self.npay = 0

class data():
    def __init__(self):
        self.id = 0
        self.mid = 0
        self.pkey = 0
        self.cat = ''
        self.cat_id = ''
        self.count = 0
        self.item_name = ''
        self.option_name = ''
        self.nodes = []
        self.meta = {}

class meta():
    def __init__(self):
        self.cat = ''
        self.cats = []
        self.cat_id = ''
        self.compare_count = ''
        self.review_count = ''
        self.infos = ''
        self.thumbnail = ''
        self.jjim = ''
        self.thumbs = []

class category():
    def __init__(self):
        self.id = ''
        self.depth = 0
        self.name = ''