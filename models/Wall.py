from operator import itemgetter

from .ElementWithMaterial import ElementWithMaterial 

from .validation.NumberValidator import NumberValidator

from .extra.Hole import Hole 

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
        super().__init__(desc['material'], desc['uv_scale'])
        self.thickness = desc["thickness"]
        self.holes = []
        for hole in desc['holes']:
            self.holes.append(Hole(hole))

    def __str__(self):

        """
        Returns string with Wall object info.
        """
        holes_string= ''
        for hole in self.holes:
            holes_string += hole.__str__()
        return(
              'Wall:\n'
              '\tThickness:     {:6.2f}\n'
             f'{super().__str__()}'
              '\tHoles:     \n{}\n'
              .format(
                     self.thickness,
                     holes_string
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
                    position_dims.append([[hole.hpos, hole.hpos+hole.hsize], [hole.vpos, hole.vpos+hole.vsize]])
            holes_array[idx] = position_dims
            position_dims = []
                                          
        return holes_array
