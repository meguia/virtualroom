from .AssetManagerModel import AssetManagerModel

class  BlenderObjectDAO(Asset):
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
    def __init__(self):
        pass
