# -*- coding: UTF-8 -*-

class Node():

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def equals(self, n):
        if n is None:
            return False
        return self.x == n.x and self.y == n.y

    @classmethod
    def from_json(self, json_object):
         if 'x' in json_object:
             return Node(json_object['x'],json_object['y'])
