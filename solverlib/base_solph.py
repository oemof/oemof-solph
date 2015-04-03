"""
This module contains a minimal solver for the "first-example"-implementation.
It doesn't do anything interesting fpr now.
"""

class Solph(object):
    def __init__(self):
        pass

    def solve(self, grid):

        #calculates sum of all entities

        entities = grid.get_all_entities()

        l = 8760

        r = {}

        for i in range(0,l):
            t = 0
            for id,e in entities.items():
                try:
                    t += e["output"][i]
                except:
                    continue
            r[i] = t
            i+=1

        result = {"sum" : r}
        return result