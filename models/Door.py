from operator import itemgetter

from .Frame import Frame
from .validation.schema_validation_methods import validate_door_schema
from .validation.NumberValidator import NumberValidator

class Door:
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
    wall_index = NumberValidator(
                                minvalue=0, 
                                maxvalue=3, 
                                int_only= True,
                                additional_msg="Wall index"
                                )
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
        validate_door_schema(desc)
        (
        self.wall_index,
        self.position,
        self.width,
        self.height
        ) = itemgetter('wall_index','position','width','height')(desc)
        self.frame = Frame(desc['frame'])

    def __str__(self):
        """
        Returns string with Door object info.
        """
        frame_string = self.frame.__str__()
        return(
              'Door:\n'
              '\tWall index: {:6d} \n' 
              '\tPosition:      {:6.2f}\n' 
              '\tWidth:         {:6.2f}\n' 
              '\tHeight:        {:6.2f}\n'
              f'\t{ frame_string }\n'
              .format(
                     self.wall_index,
                     self.position,
                     self.width,
                     self.height
                     )
              )
