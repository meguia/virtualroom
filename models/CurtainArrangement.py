from .ElementWithMaterial import ElementWithMaterial
from .Curtain import Curtain

class CurtainArrangement(ElementWithMaterial):
    """
    A class to represent a curtain arrangment(containing one or more curtains) in a room.

    Attributes
    ----------
    material
    """
    def __init__(self, desc={}):
        super().__init__(desc['material'], desc['uv_scale'])
        self.curtains = []
        for curtain_data in desc['curtains']:
            self.curtains.append(Curtain(curtain_data))
    
    def __str__(self):
        """
        Returns string with Curtain Arrangement object info.
        """
        curtainsString = ''
        for curtain in self.curtains:
            index = self.curtains.index(curtain)
            curtainsString += 'Curtain '+str(index)
            curtainsString += '\t' + curtain.__str__()

        return('Curtain Arrangement:\n'
               '{}'
               f'{super().__str__()}'
               .format(
                      curtainsString,
                      )
               )

