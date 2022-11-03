from operator import itemgetter

from ..validation.NumberValidator import NumberValidator

from ..ElementWithMaterial import ElementWithMaterial

class Band(ElementWithMaterial):
    """

    a class to represent a Band used for material or thickness in a Wall
    object.

    bands.append([[0,bh,bh*1.1],[bt,bt,0]])

    Attributes
    ----------
    wall_indexes: list 
       list of wall index values 
    heights: list 
       list of band edges height 
    thickness: list 
        list of band thickness
    """

    def __init__(self, desc = {}):
        """
        constructs all the necessary attributes for the Band object.
        
        parameters
        -----------
            desc: dict
                dictionary representing Band information
        """
        try:
            super().__init__(desc['material'], desc['uv_scale'])
        except KeyError as err:
            print('No material declared for wall')

        self.heights = []
        for height_value in desc['heights']:
            self.heights.append(height_value)
        try:
            if len(self.heights) == 0:
                raise ValueError('Height list should not be empty')
        except ValueError as err:
            print('Invalid band list size: '+repr(err))

        self.thickness = []
        for thickness_value in desc['thickness']:
            self.thickness.append(thickness_value)
        try:
            if len(self.thickness) == 0:
                raise ValueError('Thickness list should not be empty')
        except ValueError as err:
            print('Invalid band list size: '+repr(err))


        self.wall_indexes = []
        for wall_index_value in desc['wall_index']:
            self.wall_indexes.append(wall_index_value)
        try:
            if len(self.wall_indexes) == 0:
                raise ValueError('Wall index list should not be empty')
        except ValueError as err:
            print('Invalid band list size: '+repr(err))

    def __str__(self):
        """
        returns string with color object info.
        """
        mat_str = ''
        if hasattr(self, 'material') and hasattr(self,'uv_scale'):
            mat_str += super().__str__()
        return(
               '\tBand:\n'
               '\t- Wall Index:    {}\n'
               '\t- Heights:       {}\n'
               '\t- Thickness:     {}\n'
               '\t{}\n'
               .format(
                      self.wall_indexes,
                      self.heights,
                      self.thickness,
                      mat_str,
                      )
               )
