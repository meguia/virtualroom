from operator import itemgetter

from .ElementWithMaterial import ElementWithMaterial 

from .validation.NumberValidator import NumberValidator

class Wall(ElementWithMaterial):
    """
    A class to represent a wall.

    Attributes
    ----------
    thickness: float
        wall thickness
    material: type Material
        wall's material
    """

    thickness = NumberValidator(additional_msg="Wall thickness")

    def __init__(self, desc = {}):
        """
        Constructs all the necessary attributes for the wall object.
        """
        super().__init__(desc["material"])
        self.thickness = desc["thickness"]

    def __str__(self):

        """
        Returns string with Wall object info.
        """
        return(
              'Wall:\n'
              '\tThickness:     {:6.2f}\n'
             f'{self.material.__str__()}'
              .format(
                     self.thickness
                     )
              )
