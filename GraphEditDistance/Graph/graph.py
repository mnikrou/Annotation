# -*- coding: UTF-8 -*-
from .edge import Edge

class Graph():

    def __init__(self, edges):
        self.edges = edges

    def add_edge(self, edge):
        self.edges.append(edge)

    def get_nodes(self):
        if self.edges:
            return [self.edges[0].start] + [e.end for e in self.edges]
        else:
            return []

    def size(self):
        return len(self.get_nodes())

    @classmethod
    def from_json(self, json_object):
        if 'edges' in json_object:
            g = Graph([])
            eds = json_object['edges']
            if eds:
                for e in eds:
                    g.add_edge(Edge.from_json(e))
            return g

    @classmethod
    def create_from(self, filename):
        import json
        
        f = open(filename, 'r')
        data  = json.loads(f.read())
        g = Graph.from_json(data)
        return g

