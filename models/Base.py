from operator import itemgetter

from .ElementWithMaterial import ElementWithMaterial
from .validation.schema_validation_methods import validate_base_schema
from .validation.NumberValidator import NumberValidator

class Base(ElementWithMaterial):
    """
    A class to represent a room base.

    Attributes
    ----------
    height: float
        room base's height in meters (Note that to the original value an offset
        that represents the room's wall thickness is added)
    thickness: float
        room base's thickness 

    """
    height = NumberValidator(additional_msg="Base height")
    thickness= NumberValidator(additional_msg="Base thickness")
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
        super().__init__(desc['material'])
        (
        self.height, 
        self.thickness,
        ) = itemgetter('height', 'thickness')(desc) 
        self.height += offset 

    def __str__(self):
        """
        Returns string with Speaker object info.
        """
        material_string = self.material.__str__()
        return(
               ' Base:\n'
              '\tHeight:        {:6.2f}\n' 
              '\tThickness:     {:6.2f}\n'
             f'\t{material_string}'
              .format(
                     self.height,
                     self.thickness
                     )
              )

