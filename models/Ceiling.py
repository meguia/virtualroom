from .ElementWithMaterial import ElementWithMaterial

class Ceiling(ElementWithMaterial):
    """
    A class to represent a ceiling.

    Attributes
    ----------
    material: type Material
        ceiling's material
    """

    def __init__(self, desc = {}):
        """
        Constructs all the necessary attributes for the Ceiling object.
        """
        try:
            super().__init__(desc['material'], desc['uv_scale'])
        except KeyError as err:
            print('No material declared for ceiling')

    def __str__(self):

        """
        Returns string with Ceiling object info.
        """
        mat_str = ''
        if hasattr(self, 'material') and hasattr(self,'uv_scale'):
            mat_str += super().__str__()
        return(
              'Ceiling:\n'
              '{}'
              .format(mat_str)
              )
