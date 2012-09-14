__author__ = 'elleryaree'

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