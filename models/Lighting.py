from operator import itemgetter
from .validation.NumberValidator import NumberValidator
from .validation.OneOfValidator import OneOfValidator

from .LightSource import LightSource

class Lighting:
    """
    A class to represent Room lighting.

    Attributes
    ----------
    array_x: int
        lighting x array size
    array_y: int
        lighting y array size
        
    """
    array_x = NumberValidator()
    array_y = NumberValidator()

    def __init__(self, desc = {}):
        """
        Constructs all the necessary attributes for the Lighting object.
        
        Parameters
        -----------
            desc: dict
                dictionary representing light source information
        """
        (
        self.array_x, 
        self.array_y, 
        ) = itemgetter(
                     'x',
                     'y',
                     )(desc['arrangement'])
        self.light_source = LightSource(desc['light_source'])
    '''
        {
            "lighting": {
                "arrangement" : {"x": valx, "y": valy},
                "light_source": {
                    "object" : "Tube",
                    "iesfile": "file/path",
                    "intensity" : 400,
                    "mount": {
                        "size": {
                        "x": 10.0,
                        "y": 10.0,
                        "z": 10.0,
                        }
                    }
                }
            }
        }
    '''

    def __str__(self):
        """
        Returns string with LightSource object info.
        """

        light_source_string = self.light_source.__str__()

        return(
              'Lighting:\n'
              'Arrangement:\n'
              '\tX:  {0:6.2f}\n'
              '\tY:  {1:6.2f}\n' 
              f'{ light_source_string }\n'
              .format(
                     self.array_x,
                     self.array_y,
                     )
              )
