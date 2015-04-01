"""
This module is a naming-wrapper for the Grid-Class.
It just makes it easier to read, when referring to Regions in some cases.


Author: Steffen Peleikis
Date: 31.03.2015


"""



from base_grid import Grid

class Region(Grid):
    def __init__(self, region_id, position=None):
        super(Region, self).__init__(region_id, position)