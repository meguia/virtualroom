from operator import itemgetter

from .validation.NumberValidator import NumberValidator

class Mount:
    """
    A class to represent a light mount.

    Attributes
    ----------
    sizeX: float
        mount's x size
    sizeY: float
        mount's y size
    sizeZ: float
        mount's z size
    """

    sizeX = NumberValidator()
    sizeY = NumberValidator()
    sizeZ = NumberValidator()

    def __init__(self, desc = {}):
        """
        Constructs all the necessary attributes for the Mount object.
        
        Parameters
        -----------
            desc: dict
                dictionary representing mount information
        """
        (
        self.sizeX,
        self.sizeZ,
        ) = itemgetter(
                       'x',
                       'z',
                       )(desc['size'])

        print(desc['size'])
        if 'y' in desc['size']:
            self.sizeY = itemgetter('y')(desc['size'])
        else:
            self.sizeY = 0

    def as_xyz_array(self):
        """
        Returns mount sizes as x y z array
        """
        return [
                self.sizeX,
                self.sizeY,
                self.sizeZ,
               ]

    def __str__(self):
        """
        Returns string with Mount object info.
        """
        return('Mount:\n'
               '\tSize:\n'
               '\tX:     {:6.2f}\n'
               '\tY:     {:6.2f}\n'
               '\tZ:     {:6.2f}\n'
               .format(
                      self.sizeX,
                      self.sizeY,
                      self.sizeZ,
                      )
               )
