# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 15:53:14 2015

@author: uwe
"""
import logging
from matplotlib import pyplot as plt
from shapely import geometry as shape
from descartes import PolygonPatch
import fiona
from shapely.ops import cascaded_union


class region():

    def __init__(self, geometry=None, nuts=None, file=None):

        # Das muss noch schlauer gemacht werden
        # 3 Möglichkeiten entweder wird ein fertiges shapely-Objekt übergeben
        # oder eine List mit mindestens einem Nuts-Code oder ein Pfad zu
        # einer shp-Datei.
        try:
            # Der Ausdruck ist irreführend, denn ein Fehler wird ausgeworfen,
            # wenn 'geometry kein shapely-Objekt ist, denn dann gibt es die
            # Methode 'is_valid' nicht. Wenn es aber ein shaply-Objekt ist
            # dann gibt es keinen Fehler. Ist die Geometry fehlerhaft wird
            # False zurückgegeben, aber das hat keine Auswirkung. Ei
            if geometry.is_valid:
                self.__geometry__ = geometry
            else:
                raise TypeError('No valid geometry given.')
        except:
            if isinstance(nuts, list):
                self.__geometry__ = self.get_polygon_from_nuts(nuts)
            elif isinstance(file, str):
                    self.__geometry__ = self.get_polygon_from_shp_file(file)
            else:
                logging.error('No valid geometry given.')
                raise

    def get_polygon_from_nuts(self, nuts):
        'If at least one nuts-id is given, the polygon is loaded from the db.'
        logging.debug('Getting polygon from DB')

    def get_polygon_from_shp_file(self, file):
        'If a file name is given the polygon is loaded from the file.'
        logging.debug('Loading polygon from file: {0}'.format(file))
        multi = shape.MultiPolygon(
            [shape.shape(pol['geometry']) for pol in fiona.open(file)])
        return cascaded_union(multi)

    def centroid(self):
        'Returns the centroid of the given geometry as a shapely point-object.'
        return self.__geometry__.centroid

    def plot(self):
        'Simple plot to check the geometry'
        BLUE = '#6699cc'
        GRAY = '#9FF999'
        fig, ax = plt.subplots()
        if self.__geometry__.geom_type == 'MultiPolygon':
            for polygon in self.__geometry__:
                patch = PolygonPatch(polygon, fc=GRAY, ec=BLUE, alpha=0.5)
                ax.add_patch(patch)
        else:
            patch = PolygonPatch(
                self.__geometry__, fc=GRAY, ec=BLUE, alpha=0.5)
            ax.add_patch(patch)
        ax.set_xlim(self.__geometry__.bounds[0], self.__geometry__.bounds[2])
        ax.set_ylim(self.__geometry__.bounds[1], self.__geometry__.bounds[3])


if __name__ == "__main__":
    geo = shape.Polygon([(0, 0), (1, 1), (1, 0), (2, 5)])
    a = region(geometry=geo)
    b = region(nuts=['1234', '1236'])
    c = region(file='/home/uwe/Wittenberg.shp')

    c.plot()
    plt.plot(c.centroid().x, c.centroid().y, 'x', color='r')
    plt.show()

    a.plot()
    plt.plot(a.centroid().x, a.centroid().y, 'x', color='r')
    plt.show()
