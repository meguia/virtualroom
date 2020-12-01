from .ElementWithMaterial import ElementWithMaterial

class Ceiling(ElementWithMaterial):
    """
    A class to represent a ceiling.

    Attributes
    ----------
    material: type Material
        ceiling's material
    """

    def __init__(self, desc = {}):
        """
        Constructs all the necessary attributes for the Ceiling object.
        """
        super().__init__(desc["material"])
