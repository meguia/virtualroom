from operator import itemgetter

from .validation.NumberValidator import NumberValidator
from .validation.StringValidator import StringValidator

from .extra.AssetManagerModel import AssetManagerModel

class CableTrayArrangement(AssetManagerModel):
    '''
    A class to represent a Cable Tray Arrangement 
    Attributes
    ----------
    
    x_offset: float
     _  absolute distance between tray and roof along the x axis
    y_offset: float
     _  absolute distance between tray and roof along the y axis
    z_offset: float
        absolute distance between tray and roof along the z axis
    assets: array
        array of tray assets: ie Tray and TrayConnector
    '''
    
    x_offset = NumberValidator(minvalue= 0.0, additional_msg="X offest")
    y_offset = NumberValidator(minvalue= 0.0, additional_msg="Y offest")
    z_offset = NumberValidator(minvalue= 0.0, additional_msg="Z offest")

    def __init__(self, desc= {}):
        """
        Constructs all the necessary attributes for the CableTrayArrangement object.
        
        Parameters
        -----------
            desc: dict
                dictionary representing cable tray arrangement information
        """
        super().__init__(desc)
        (
        self.x_offset,
        self.y_offset,
        self.z_offset,
        ) = itemgetter(
                      'x-offset',
                      'y-offset',
                      'z-offset',
                      )(desc)

    def __str__(self):
        """
        Returns string with CalbeTrayArrangement object info.
        """
        assets_string = ''
        if(len(self.assets) > 0):
            for asset in self.assets:
                assets_string += asset.__str__()
        
        return(
              'Cable Tray Arrangement:\n'
              '\tX offset:{0:6.2f}\n'
              '\tY offset:{1:6.2f}\n'
              '\tZ offset:{2:6.2f}\n'
              f'{ assets_string }\n'
              .format(
                     self.x_offset,
                     self.y_offset,
                     self.z_offset,
                     )
              )
