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
        self.cat = ''
        self.count = 0
        self.item_name = ''
        self.nodes = []
        self.meta = {}
        self.agent = ''

class meta():
    def __init__(self):
        self.cat = ''
        self.thumbnail = ''

class category():
    def __init__(self):
        self.id = ''
        self.depth = 0
        self.name = ''