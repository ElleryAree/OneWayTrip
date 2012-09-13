from turtle import position
import copy

__author__ = 'elleryaree'

class PathFinder:
    def __init__(self, grid, start, goal):
        self.grid = grid
        self.start = start
        self.goal = goal

    def find(self):
        position = self.start
        visited = [position]
        actions = self.__get_actions(position, visited)
        routes = []
        route = (0, [])

        while len(routes) or len(actions):
            if position == self.goal:
                return route

            for action in actions:
                a_route = copy.copy(route[1])
                a_route.append(action)
                length = len(a_route) + abs(self.goal[0] - action[0][0]) + abs(self.goal[1] - action[0][1])
                routes.append((length, a_route))

            routes.sort()
            route = routes.pop(0)
            position = route[1][len(route[1]) - 1][0]
            visited.append(position)

            actions = self.__get_actions(position, visited)

        return 0, []



    def __get_actions(self, position, visited):
        possible_actions = [((-1, 0), "L"), ((1, 0), "R"), ((0, -1), "U"), ((0, 1), "D")]
        actions = []

        for action in possible_actions:
            x = position[0] + action[0][0]
            y = position[1] + action[0][1]
            if 0 <= y < len(self.grid) and \
               0 <= x < len(self.grid[y]) and self.grid[y][x] == "S" and \
               not (x, y) in visited:
                actions.append(((x, y), action[1]))

        return actions