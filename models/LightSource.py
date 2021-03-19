from operator import itemgetter

from .validation.StringValidator import StringValidator
from .validation.NumberValidator import NumberValidator
from .validation.OneOfValidator import OneOfValidator

class LightSource:
    """
    A class to represent a Light Source.

    Attributes
    ----------
    source: object 
        Light type, Tube, Spot, etc
    color: float
        light color
    iesfile: Path
       path to iesfiles 
    intensity: float
        light intensity
    diameter: float
        light diameter 
    length: float
        light length
    """

    source = OneOfValidator('Tube', 'Spot') 
    iesfile = StringValidator(additional_msg="Iesfile path")
    color = NumberValidator(0,255)
    intensity = NumberValidator()
    diameter = NumberValidator()

    def __init__(self, desc = {}):
        """
        Constructs all the necessary attributes for the LightSource object.
        
        Parameters
        -----------
            desc: dict
                dictionary representing light source information
        """
        (
        self.source,
        self.iesfile,
        self.color,
        self.intensity,
        self.diameter
        ) = itemgetter('source',
                       'iesfile',
                       'color',
                       'intensity',
                       'diameter',
                       )(desc)

    def __str__(self):
        """
        Returns string with LightSource object info.
        """
        return('Material:\n'
               '\tName:          {self.source}\n'
               '\tIes file:      {self.iesfile}\n'
               '\tColor:         {:6.2f}\n'
               '\tIntensity:     {:6.2f}\n'
               '\tDiamater:      {:6.2f}\n'
               .format(
                      self.color,
                      self.intensity,
                      self.diameter,
                      )
               )
