
from .ElementWithMaterial import ElementWithMaterial

class Floor(ElementWithMaterial):
    """
    A class to represent a Floor.

    Attributes
    ----------
    material: type Material
        ceiling's material
    """

    def __init__(self, desc = {}):
        """
        Constructs all the necessary attributes for the Floor object.
        """
        super().__init__(desc['material'])
