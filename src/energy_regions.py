# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 15:53:14 2015

@author: uwe
"""

from shapely import geometry


class region:

    def __init__(self, geometry=None, nuts=None):
        try:
            self.__polygon_type__ = geometry.geom_type
            self.__geometry__ = geometry
            print('Got valid geometry')
        except:
            if isinstance(nuts, list):
                self.__polygon__ = self.get_polygon_from_nuts(nuts)

    def get_polygon_from_nuts(self, nuts):
        print('Getting polygon from DB')


if __name__ == "__main__":
    geo = geometry.Polygon([(0, 0), (1, 1), (1, 0)])
    b = region(nuts=['1234', '1236'])
    c = region(geometry=geo)
