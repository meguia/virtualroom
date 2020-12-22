from .Material import Material

class ElementWithMaterial:
    """
    A class to represent a Room element with material.

    Attributes
    ----------
    material: type Material
        ceiling's material
    """

    def __init__(self, desc, uv_scale):
        """
        Constructs all the necessary attributes for the Element with material object object.
        """
        self.material = Material(desc)
        self.uv_scale = uv_scale 

    def __str__(self):

        """
        Returns string with Element object info.
        """
        class_name = type(self).__name__
        return(
             f'\tUV scale:      {self.uv_scale:6.2f}\n'
             f'{self.material.__str__()}'
              )

