from operator import itemgetter
from .validation.NumberValidator import NumberValidator
from .validation.OneOfValidator import OneOfValidator

from .LightSource import LightSource

class Lighting:
    """
    A class to represent Room lighting.

    Attributes
    ----------
    arrangement: array o tuple?
        x, y represents room lighting arrangement
    mount: object
    whole: tuple
       width, depth 
        
    """
    def __init__(self, desc = {}):
        """
        Constructs all the necessary attributes for the Lighting object.
        
        Parameters
        -----------
            desc: dict
                dictionary representing light source information
        """
        self.whole = itemgetter.('x', 'y')(desc['whole'])
        self.arrangement = itemgetter.('x', 'y')(desc['arrangement'])
        self.light_source = LightSource(desc['light source'])
    '''
        {
            "light source": {
                "whole" : {"x": valx, "y": valy},
                "arrangement" : {"x": valx, "y": valy},
                "light source": {
                    "source" : "Tube",
                    "iesfile": "file/path",
                    "color" : 255,
                    "intensity" : 400,
                    "diameter": 0.01,
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
              '\tWhole x, y: {6.2f} {6.2f}\n' 
              '\tArrangement x, y: {6.2f} {6.2f}\n' 
              f'{ light_source_string }\n'
              .format(
                     self.whole[0],
                     self.whole[1],
                     self.arrangement[0],
                     self.arrangement[1],
                     )
              )
