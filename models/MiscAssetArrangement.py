from operator import itemgetter

from .validation.NumberValidator import NumberValidator
from .validation.StringValidator import StringValidator

from .extra.AssetManagerModel import AssetManagerModel
from .extra.BlenderObjectDAO import BlenderObjectDAO

class MiscAssetArrangement(AssetManagerModel):
    '''
    An arrengement of Miscellaneous Blender Objects
    Attributes
    ----------
        
    '''

    def __init__(self, desc= {}):

        self.blender_objects = []
        try:
            for blender_obj_idx in range(len(desc)):
                blender_obj = desc[blender_obj_idx]
                self.blender_objects.append(
                                            BlenderObjectDAO(blender_obj)
                                            )
        except KeyError:
            error_msg = 'Blender objects key error'
            print(error_msg)

        super().__init__()
        super().__setattr__('assets', self.get_blender_objects_assets())

    def get_blender_objects_assets(self):
        '''
        Returns assets from objects
        '''
        assets = []
        for blender_obj in self.blender_objects:
            assets.append(blender_obj.asset)
        return assets

    def __str__(self):
        '''
        Returns string with Misc Asset Arrangement info
        '''
        objects_string = ''
        for blender_obj in self.blender_objects:
            objects_string += blender_obj.__str__()


        return(
              'Miscellaneous Asset Arrangement:\n'
              f'{ objects_string }'
              )
