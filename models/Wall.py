from operator import itemgetter

from .ElementWithMaterial import ElementWithMaterial 
from .extra.AssetManagerModel import AssetManagerModel

from .validation.NumberValidator import NumberValidator

from .extra.Hole import Hole 
from .extra.Band import Band

class Wall(ElementWithMaterial):
    """
    A class to represent a wall.

    Attributes
    ----------
    thickness: float
        wall thickness
    material: type Material
        wall's material
    holes: array of Hole objects
        wall's holes
    bands: array of Bands objects
        wall's bands 
    """

    thickness = NumberValidator(additional_msg="Wall thickness")

    def __init__(self, desc = {}):
        """
        Constructs all the necessary attributes for the wall object.
        """
        try:
            super().__init__(desc['material'], desc['uv_scale'])
        except KeyError as err:
            print('No material declared for wall')
        self.thickness = desc["thickness"]
        self.holes = []
        if 'holes' in desc:
            for hole in desc['holes']:
                self.holes.append(Hole(hole))
        self.bands = []
        if 'bands' in desc:
            for band in desc['bands']:
                self.bands.append(Band(band))

    def __str__(self):

        """
        Returns string with Wall object info.
        """
        holes_string= ''
        mat_str = ''
        if hasattr(self, 'material') and hasattr(self,'uv_scale'):
            mat_str += super().__str__()
        for hole in self.holes:
            holes_string += hole.__str__()
        bands_string = ''
        for band in self.bands:
            bands_string += band.__str__()
        return(
              'Wall:\n'
              '\tThickness:     {:6.2f}\n'
              '\t{}\n'
              '\tHoles:     \n{}\n'
              '\tBands:     \n{}\n'
              .format(
                     self.thickness,
                     mat_str,
                     holes_string,
                     bands_string
                     )
              )
    def holes_as_array(self):
        """
        Returns holes values index by wall index
        """
        holes_array = [[]]*4
        for idx in range(len(holes_array)):
            position_dims = []
            for hole in self.holes:
                if hole.wall_index == idx:
                    position_dims.append([
                                         [hole.hpos, hole.hpos+hole.hsize], 
                                         [hole.vpos, hole.vpos+hole.vsize]
                                         ])
            holes_array[idx] = position_dims
            position_dims = []
                                          
        return holes_array
    
    def fetch_bands_measures_by_wall_index(self, wall_index):
        """
        Returns list of band measures queried by wall index
        """
        bands_measures = []
        for band in self.bands:
            if wall_index in band.wall_indexes:
                bands_measures.append([band.heights, band.thickness])
        return bands_measures

    def fetch_bands_material_by_wall_index(self, wall_index):
        """
        Returns list of band materials queried by wall index
        """
        bands_materials = []
        for band in self.bands:
            if wall_index in band.wall_indexes:
                bands_materials.append(band.material)
        return bands_materials
    
    def fetch_bands_by_wall_index(self, wall_index):
        """
        Returns list of bands with same wall index
        """
        wanted_bands = []
        for band in self.bands:
            if wall_index in band.wall_indexes:
                wanted_bands.append(band)
        return wanted_bands

    def fetch_bands_materials(self):
        # fetch bands materials if they have them
        materials = [band.material for band in self.bands if hasattr(band, 'material')]
        return materials

    def fetch_doors(self):
        """
        Returns doors on walls
        """
        doors = []
        for hole in self.holes:
            doors.append(hole.door)
        return doors 

    def fetch_doors_by_wall_index(self, wall_index):
        """"
        Return doors belonging to given wall
        """
        doors = []
        for hole in self.holes:
            if wall_index == hole.wall_index and hole.door is not None:
                doors.append(hole.door)
        return doors 

    def fetch_doors_materials(self):
        """"
        Return list of materials used by doors
        """
        doors_materials = []
        for hole in self.holes:
            if hole.door is not None:
                if hasattr(hole.door, 'material'):
                    if hole.door.material.name is not None:
                        doors_materials.append(hole.door.material)
        return list(set(doors_materials)) 
