from operator import itemgetter

from .validation.schema_validation_methods import validate_spot_schema
from .validation.NumberValidator import NumberValidator
from .validation.StringValidator import StringValidator

class Spot:
    """
    A class to represent a Blender camera.

    Attributes
    ----------
    name: string
        name of spot
    energy: float
        spot energy
    size: float
        spot size
    blend: float
        spot blend
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

    name = StringValidator(additional_msg="Spot Name value")
    energy= NumberValidator(additional_msg="Spot Energy value")
    size  = NumberValidator(additional_msg="Spot Size value")
    blend = NumberValidator(additional_msg="Spot Blend value") 
    x = NumberValidator(additional_msg="Spot x position")
    y = NumberValidator(additional_msg="Spot y position")
    z = NumberValidator(additional_msg="Spot z position")
    rotX = NumberValidator(additional_msg="Spot x rotation")
    rotY = NumberValidator(additional_msg="Spot y rotation")
    rotZ = NumberValidator(additional_msg="Spot z rotation")

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
        self.name,
        self.energy,
        self.size,
        self.blend 
        ) = itemgetter(
                      'name'  ,
                      'energy',
                      'size'  ,
                      'blend'
                      ) (desc)
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
        return(
               ' Spot:\n'
              f'\tName: {self.name}\n'
              '\tEnergy:       {:6.2f}\n'
              '\tSize:          {:6.2f}\n'
              '\tBlend:         {:6.2f}\n'
              '\tPosition:\n'
              '\tX:             {:6.2f}\n'
              '\tY:             {:6.2f}\n'
              '\tZ:             {:6.2f}\n'
              '\tRotation:\n'
              '\tX:             {:6.2f}\n'
              '\tY:             {:6.2f}\n'
              '\tZ:             {:6.2f}\n'
              .format(
                     self.energy,
                     self.size,
                     self.blend,
                     self.x,
                     self.y,
                     self.z,
                     self.rotX,
                     self.rotY,
                     self.rotZ,
                     )
              )
