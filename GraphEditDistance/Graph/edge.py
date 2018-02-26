# -*- coding: UTF-8 -*-
from .node import Node

class Edge():

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def equals(self, e):
        if e is None:
            return False
        return self.start.equals(e.start) and  self.end.equals(e.end)

    @classmethod
    def from_json(self, json_object):
         if 'start' in json_object:
             s = Node(json_object['start']['x'], json_object['start']['y']) 
             e = Node(json_object['end']['x'], json_object['end']['y']) 
             return Edge(s, e)

