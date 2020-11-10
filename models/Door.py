from operator import itemgetter

from .Frame import Frame

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
    def __init__(self, desc = {}):
        """
        Constructs all the necessary attributes for the door 
        object.
        
        Parameters
        -----------
            desc: dict
                dictionary representing Door's information
        """
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
        return('Door:\n'
              f'\tWall index: {self.wall_index} \n' 
              f'\tPosition:   {self.position}\n' 
              f'\tWidth:      {self.width}    \n' 
              f'\tHeight:     {self.height}   \n'
              f'\t{ frame_string }\n'
              )
