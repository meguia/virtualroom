from operator import itemgetter
from validation.schema_validation_methods import validate_base_schema

class Base:
    """
    A class to represent a room base.

    Attributes
    ----------
    height: float
        room base's height in meters (Note that to the original value an offset that
        represents the room's wall thicknness is added)
    thickness: float
        room base's thickness 

    """
    def __init__(self, offset, desc = {}):
        """
        Constructs all the necessary attributes for the base 
        object.
        
        Parameters
        -----------
            desc: dict
                dictionary representing base's information
        """
        validate_base_schema(desc)
        (
        self.height, 
        self.thickness,
        ) = itemgetter('height', 'thickness')(desc) 
        self.height += offset 

    def __str__(self):
        """
        Returns string with Speaker object info.
        """
        return(' Base:\n'
              f'\tHeight:   {self.height} \n' 
              f'\tThickness:{self.thickness}\n' )

