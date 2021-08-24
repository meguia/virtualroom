from operator import itemgetter

from .ElementWithMaterial import ElementWithMaterial

from .Frame import Frame
from .validation.schema_validation_methods import validate_door_schema
from .validation.NumberValidator import NumberValidator

class Door(ElementWithMaterial):
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
        super().__init__(desc['material'], desc['uv_scale'])
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
        material_string = self.material.__str__()

        return(
              'Door:\n'
              '\tPosition:      {:6.2f}\n' 
              '\tWidth:         {:6.2f}\n' 
              '\tHeight:        {:6.2f}\n'
              f'{super().__str__()}'
              f'{ frame_string }\n'
              .format(
                     self.position,
                     self.width,
                     self.height
                     )
              )
