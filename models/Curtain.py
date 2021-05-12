from operator import itemgetter

from .validation.NumberValidator import NumberValidator
from .validation.StringValidator import StringValidator

class Curtain:
    '''
    A class to represent a curtain
    Attributes
    ----------

    wall_index: int
        wall upon which curtain will be placed, 0 right, 1 left, 2 behind, 3 forward
    width: float
        curtian width
    height: float
        curtain height
    position: float

        curtain position along x axis in wall_index cases 0(left) and 1(right)
        and along y axis in cases 2(behind) and 3(forward) 
    '''
    wall_index = NumberValidator(0,4,additional_msg="wall_index 0 right, 1 left, 2 behind, 3 forward")
    offset= NumberValidator(additional_msg="Curtain width")
    width = NumberValidator(additional_msg="Curtain width")
    height= NumberValidator(additional_msg="Curtain height")
    position = NumberValidator(additional_msg="Curtain position")

    def __init__(self, desc = {}):
        """
        Constructs all the necessary attributes for the curtain
        object.
        
        Parameters
        -----------
            desc: dict
                dictionary representing Curtain's information         
        """
        #validate_speaker_schema(desc)
        (
        self.wall_index,
        self.offset,
        self.width,
        self.height,
        self.position,
        ) = itemgetter(
                      'wall_index',
                      'offset',
                      'width',
                      'height',
                      'position',
                      )(desc) 

    def __str__(self):
        """
        Returns string with Speaker object info.
        """
        return(
              '\n\twall_index:   {}\n'
              '\tOffset:         {:6.2f}\n'
              '\tWidth:         {:6.2f}\n'
              '\tHeight:        {:6.2f}\n'
              '\tPosition:      {:6.2f}\n'
              .format(
                     self.wall_index,
                     self.offset,
                     self.width,
                     self.height,
                     self.position,
                     )
              )
