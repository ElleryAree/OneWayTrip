__author__ = 'elleryaree'

class OnMapThing:
    def __init__(self, id, name):
        self.name = name
        self.id = id

class Street(OnMapThing):
    def __init__(self, houses, id, name, x, y):
        OnMapThing.__init__(self, id, name)
        self.x = x
        self.y = y
        self.houses = houses

class House(OnMapThing):
    def __init__(self, id, name):
        OnMapThing.__init__(self, id, name)

