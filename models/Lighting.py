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
    array_x = NumberValidator(minvalue=1, int_only=True)
    array_y = NumberValidator(minvalue=1, int_only=True)

    def __init__(self, desc = {}):
        """
        Constructs all the necessary attributes for the Lighting object.
        By default arrangement should be specified.
        Specifying positions(optional) overrides arrangement.

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
        self.positions = []
        if 'positions' in desc:
            for pos in desc['positions']:
                self.positions.append({
                                       'x': pos['x'],
                                       'y': pos['y'],
                                     })

        self.light_source = LightSource(desc['light_source'])

    def __str__(self):
        """
        Returns string with LightSource object info.
        """

        light_source_string = self.light_source.__str__()
        positions_string = ''
        if(len(self.positions) > 0):
            positions_string += '\tMount positions:\n'
            for idx, pos in enumerate(self.positions):
                positions_string += '\tLight ' + str(idx) +':\n'
                positions_string += '\tX: ' + str(pos['x']) +'\n'
                positions_string += '\tY: ' + str(pos['y']) +'\n'


        return(
              'Lighting:\n'
              'Arrangement:\n'
              '\tX:  {0:6.2f}\n'
              '\tY:  {1:6.2f}\n' 
              f'{ light_source_string }\n'
              f'{ positions_string }'
              .format(
                     self.array_x,
                     self.array_y,
                     )
              )
