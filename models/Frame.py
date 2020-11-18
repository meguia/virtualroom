from operator import itemgetter

from .validation.schema_validation_methods import validate_frame_schema
from .validation.NumberValidator import NumberValidator

class Frame:
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
        self.width, self.thickness= itemgetter('width','thickness')(desc)
    def __str__(self):
        """
        Returns string with Door object info.
        """
        return('Frame:\n'
              f'\t Width:    {self.widt:6.2fh}    \n' 
              f'\t Thickness:{self.thickness:6.2f}\n' )
