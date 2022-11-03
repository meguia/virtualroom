
from .ElementWithMaterial import ElementWithMaterial

class Floor(ElementWithMaterial):
    """
    A class to represent a Floor.

    Attributes
    ----------
    material: type Material
        ceiling's material
    """

    def __init__(self, desc = {}):
        """
        Constructs all the necessary attributes for the Floor object.
        """
        try:
            super().__init__(desc['material'], desc['uv_scale'])
        except KeyError as err:
            print('No material declared for floor')

    def __str__(self):

        """
        Returns string with Floor object info.
        """
        mat_str = ''
        if hasattr(self, 'material') and hasattr(self,'uv_scale'):
            mat_str += super().__str__()
        return(
              'Floor:\n'
              '{}'
              .format(mat_str)
              )
