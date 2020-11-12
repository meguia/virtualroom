from operator import itemgetter

from validation.schema_validation_methods import validate_spot_schema

class Spot:
    """
    A class to represent a Blender camera.

    Attributes
    ----------
    x: float
        spot's x position in meters
    y: float
        spot's y position in meters
    z: float
        spot's z position in meters
    rotX: float
        spot x rotation in degrees 
    rotY: float
        spot y rotation in degrees 
    rotZ: float
        spot z rotation in degrees 
    """
    def __init__(self, desc = {}):
        """
        Constructs all the necessary attributes for the 
        spot object.

        Parameters
        -----------
            desc: dict
                dictionary representing Spot's information
        """
        validate_spot_schema(desc)
        (
        self.x,
        self.y,
        self.z
        ) = itemgetter('x','y','z')(desc['position'])
        (
        self.rotX,
        self.rotY,
        self.rotZ
        ) = itemgetter('x','y','z')(desc['rotation'])

    def __str__(self):
        """
        Returns string with Spot object info.
        """
        return(' Spot\n'
                '\tPosition:\n'
              f'\tX:    {self.x}\n'
              f'\tY:    {self.y}\n'
              f'\tZ:    {self.z}\n'
               '\tRotation\n'
              f'\tX:    {self.rotX}\n'
              f'\tY:    {self.rotY}\n'
              f'\tZ:    {self.rotZ}\n'
              )
