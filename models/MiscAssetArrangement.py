from operator import itemgetter

from .validation.NumberValidator import NumberValidator
from .validation.StringValidator import StringValidator

from .extra.AssetManagerModel import AssetManagerModel

class MiscAssetArrangement(AssetManagerModel):
    '''
    An arrengement of Miscellaneous Blender Objects
    Attributes
    ----------
    
    x_pos: float
       absolute distance between tray and roof along the x axis
    y_pos: float
       absolute distance between tray and roof along the y axis
    z_pos: float
        absolute distance between tray and roof along the z axis
    assets: list 
        
    '''

    def __init__(self, desc= {}):
        pass
