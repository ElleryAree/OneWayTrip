__author__ = 'elleryaree'
from OneWayTrip.TileSet import CharacterTileSet

class Thing(object):
    def __init__(self, position, action_positions, description):
        self.action_positions = action_positions
        self.position = position
        self.description = description

class Door(Thing):
    def __init__(self, position, hero_position, map_index, action_positions, description):
        super(Door, self).__init__(position, action_positions, description)
        self.hero_position = hero_position
        self.map_index = map_index

class Item(Thing):
    def __init__(self, id, name, position, action_positions, description, cost):
        super(Item, self).__init__(position, action_positions, description)
        self.name = name
        self.cost = cost
        self.id = id

class Char(Thing):
    def __init__(self, position, action_positions, description, name):
        super(Char, self).__init__((position[0], position[1]), action_positions, description)
        self.tile_set = CharacterTileSet("%s.png" % name)
        self.char_position = position
        self.name = name

    def get_image(self):
        return self.tile_set.get_sprite(self.char_position)[0]