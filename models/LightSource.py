from operator import itemgetter

from .validation.StringValidator import StringValidator
from .validation.NumberValidator import NumberValidator
from .validation.OneOfValidator import OneOfValidator

from .validation.schema_validation_methods import validate_tube_schema
from .validation.schema_validation_methods import validate_simple_spot_schema

from .extra.Color import Color
from .Mount import Mount
from .Asset import Asset

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
    blend:
    """

    object = OneOfValidator('tube', 'spot','asset') 
    iesfile = StringValidator(additional_msg="Iesfile path")
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
        # validate desc schema
        self.object = itemgetter('object')(desc)
        if self.object == 'tube':
            validate_tube_schema(desc)
            pass
        elif self.object == 'spot':
            #validate_simple_spot_schema(desc)
            pass
        elif self.object == 'asset':
            try:
                self.asset = Asset(desc['asset_info'])
            except KeyError:
                error_msg = 'Missing asset_info key'
                print(error_msg)
            pass

        (
        self.iesfile,
        self.intensity,
        ) = itemgetter(
                       'iesfile',
                       'intensity',
                       )(desc)
        self.mount = Mount(desc['mount'])
        self.color = Color(desc['color'])

    def color_as_rgba_array(self):
        """
        Returns color as array containing r,g,b,alpha values 
        """
        return [
                self.color.r,
                self.color.g,
                self.color.b,
                self.color.alpha,
               ]

    def color_as_rgb_array(self):
        """
        Returns color as array containing r,g,b values 
        """
        return [
                self.color.r,
                self.color.g,
                self.color.b,
               ]

    def __str__(self):
        """
        Returns string with LightSource object info.
        """
        mount_string = self.mount.__str__()
        color_string = self.color.__str__()
        if(self.asset is not None):
            color_string += self.asset.__str__()
        return(
               f'{ mount_string }'
               '\tObject:\n'
               '\tName:          {0}\n'
               '\tIes file:      {1}\n'
               '\tIntensity:     {2:6.2f}\n'
               f'{ color_string }'
        #       '\tDiamater:      {:6.2f}\n'
               .format(
                      self.object,
                      self.iesfile,
                      self.intensity,
        #              self.diameter,
                      )
               )
