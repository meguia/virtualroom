from operator import itemgetter
from math import radians

from .AssetManagerModel import AssetManagerModel
from ..Asset import Asset
from ..validation.NumberValidator import NumberValidator

class  BlenderObjectDAO():
    '''
    A class to access and represent Blender Object data.
    Attributes
    ----------
    Asset: asset 
        Path to .blend file containing resource
    location_x: float 
        Blender Object x location  
    location_y: float 
        Blender Object y location  
    location_z: float 
        Blender Object z location  
    rotation_x: float 
        Blender Object x rotation  
    rotation_y: float 
        Blender Object y rotation  
    rotation_z: float 
        Blender Object z rotation  
    scale_x: float 
        Blender Object x scale  
    scale_y: float 
        Blender Object y scale  
    scale_z: float 
        Blender Object z scale  
    '''
    location_x = NumberValidator(additional_msg="X location")
    location_y = NumberValidator(additional_msg="Y location")
    location_z = NumberValidator(additional_msg="Z location")

    rotation_x = NumberValidator(additional_msg="X rotation")
    rotation_y = NumberValidator(additional_msg="Y rotation")
    rotation_z = NumberValidator(additional_msg="Z rotation")

    scale_x = NumberValidator(additional_msg="X scale")
    scale_y = NumberValidator(additional_msg="Y scale")
    scale_z = NumberValidator(additional_msg="Z scale")

    def __init__(self, desc = {}):
        '''
        Constructs Blender Object DAO an object that stores values representing
        a Blender Object.
        '''
        
        try:
            self.asset = Asset(desc['asset'])
        except KeyError as err:
            print(repr(err))
            print('missing asset key')

        (
        self.location_x, 
        self.location_y, 
        self.location_z,
        ) = itemgetter('x',
                       'y', 
                       'z',
                       )(desc['location'])
        (
        self.rotation_x, 
        self.rotation_y, 
        self.rotation_z,
        ) = itemgetter('x',
                       'y', 
                       'z',
                       )(desc['rotation'])
        (
        self.scale_x, 
        self.scale_y, 
        self.scale_z,
        ) = itemgetter('x',
                       'y', 
                       'z',
                       )(desc['scale'])

    def location_as_array(self):
        '''
        Returns location as array containing x, y and z values in order
        '''
        return [
               self.location_x,
               self.location_y,
               self.location_z
               ]

    def rotation_as_array(self):
        '''
        Returns rotation as array containing x, y and z values in order
        '''
        return [
               radians(self.rotation_x),
               radians(self.rotation_y),
               radians(self.rotation_z)
               ]

    def scale_as_array(self):
        '''
        Returns scale as array containing x, y and z values in order
        '''
        return [
               self.scale_x,
               self.scale_y,
               self.scale_z
               ]

    def __str__(self):
        """
        Returns string with Blender object info.
        """
        asset_string = self.asset.__str__()

        return(
              'Blender Object: \n'
               f'{ asset_string }'
              '\tLocation: \n'
              '\tX:     {:6.2f}\n'
              '\tY:     {:6.2f}\n'
              '\tZ:     {:6.2f}\n'
              '\tRotation: \n'
              '\tX:     {:6.2f}\n'
              '\tY:     {:6.2f}\n'
              '\tZ:     {:6.2f}\n'
              '\tScale: \n'
              '\tX:     {:6.2f}\n'
              '\tY:     {:6.2f}\n'
              '\tZ:     {:6.2f}\n'
              .format(
                     self.location_x, 
                     self.location_y, 
                     self.location_z,
                     self.rotation_x, 
                     self.rotation_y, 
                     self.rotation_z,
                     self.scale_x, 
                     self.scale_y, 
                     self.scale_z,
                     )
              )
