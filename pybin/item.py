class Node:
    def __init__(self):
        self.id = ''
        self.name = ''
        self.mall = ''
        self.price = 0
        self.delivery = 0
        self.npay = 0

class Data:
    def __init__(self):
        self.cat = ''
        self.count = 0
        self.item_name = ''
        self.nodes = []
        self.meta = {}
        self.agent = ''

class Meta:
    def __init__(self):
        self.cat = ''
        self.thumbnail = ''

class Category:
    def __init__(self):
        self.id = ''
        self.depth = 0
        self.name = ''
