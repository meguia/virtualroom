from operator import itemgetter

from .ElementWithMaterial import ElementWithMaterial

from .validation.schema_validation_methods import validate_frame_schema
from .validation.NumberValidator import NumberValidator

class Frame(ElementWithMaterial):
    """
    A class to represent a door frame.

    Attributes
    ----------
    width: float
        door width in meters 
    thickness: float
        door thickness in meters
    """

    width = NumberValidator(additional_msg="Frame width")
    thickness = NumberValidator(additional_msg="Frame thickness")

    def __init__(self, desc = {}):
        """
        Constructs all the necessary attributes for the door 
        frame object.
        
        Parameters
        -----------
            desc: dict
                dictionary representing Frame's information
        """
        validate_frame_schema(desc)
        super().__init__(desc['material'], desc['uv_scale'])
        self.width, self.thickness= itemgetter('width','thickness')(desc)
    def __str__(self):
        """
        Returns string with Door object info.
        """
        return(
              'Frame:\n'
              '\tWidth:         {:6.2f}\n' 
              '\tThickness:     {:6.2f}\n'
             f'{super().__str__()}\n'
              .format(
                     self.width,
                     self.thickness
                     )
              )
