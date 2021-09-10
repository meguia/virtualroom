from operator import itemgetter

from .ElementWithMaterial import ElementWithMaterial
from .extra.AssetManagerModel import AssetManagerModel

from .Frame import Frame
from .validation.schema_validation_methods import validate_door_schema
from .validation.NumberValidator import NumberValidator

class Door(ElementWithMaterial, AssetManagerModel):
    """
    A class to represent a door.

    Attributes
    ----------
    wall_index: int 
        wall onto which the door is added.
        values 0 to 3
    position: float
        door position in meters
    width: float
        door width in meters
    height: float
        door height in meters
    frame: type Frame 
        represent door frame
    """

    position = NumberValidator(additional_msg="Door position")
    width = NumberValidator(additional_msg="Door width")
    height = NumberValidator(additional_msg="Door height")

    def __init__(self, desc = {}):
        """
        Constructs all the necessary attributes for the door 
        object.
        
        Parameters
        -----------
            desc: dict
                dictionary representing Door's information
        """
        #validate_door_schema(desc)
        # door should be one of these ElementWithMaterial or AssetManagerModel 
        # not two
        # if material in desc instantiate as ElementWithMaterial
        try:
            if 'material' in desc:
                ElementWithMaterial.__init__(self,desc['material'], desc['uv_scale'])
                if 'assets_info' in desc:
                    raise KeyError
            # if asset in desc instantiate as AssetManagerModel 
            elif 'assets_info' in desc:
                AssetManagerModel.__init__(self,desc['assets_info'])
                if 'material' in desc:
                    raise KeyError
        except KeyError:
            print('Error Door should contain one of two material or assets_info')
        (
        self.position,
        self.width,
        self.height
        ) = itemgetter('position','width','height')(desc)

        self.frame = None
        if 'frame' in desc:
            self.frame = Frame(desc['frame'])

    def __str__(self):
        """
        Returns string with Door object info.
        """

        frame_string = ''
        if self.frame is not None:
            frame_string = self.frame.__str__()

        material_string = ''
        if hasattr(self, 'material'):
            if self.material.name is not None:
                material_string += ElementWithMaterial.__str__(self)

        asset_string = ''
        if hasattr(self, 'assets'): 
            if len(self.assets) != 0:
                asset_string += AssetManagerModel.__str__(self)

        return(
              'Door:\n'
              '\tPosition:      {:6.2f}\n' 
              '\tWidth:         {:6.2f}\n' 
              '\tHeight:        {:6.2f}\n'
              f'{ material_string }'
              f'{ asset_string }\n'
              .format(
                     self.position,
                     self.width,
                     self.height
                     )
              )
