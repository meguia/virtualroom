from operator import itemgetter

from validation.schema_validation_methods import validate_speaker_schema

class Speaker:                
    """
    A class to represent a speaker.

    Attributes
    ----------
    x: float
        speaker's x position in meters
    y: float
        speaker's y position in meters
    z: float
        speaker's z position in meters
    rotation: float
        speaker's rotation in degrees
    """
    def __init__(self, desc = {}):
        """
        Constructs all the necessary attributes for the speaker
        object.
        
        Parameters
        -----------
            desc: dict
                dictionary representing Speaker's information: x, y and z
                position and rotation
        """
        validate_speaker_schema(desc)
        (
        self.x,
        self.y,
        self.z,
        ) = itemgetter('x','y','z')(desc['position']) 
        self.rotation = desc.get('rotation')

    def __str__(self):
        """
        Returns string with Speaker object info.
        """
        return(' Speaker:\n'
               f'\tPos x:    {self.x}\n'
               f'\tPos y:    {self.y}\n'
               f'\tPos z:    {self.z}\n'
               f'\tRotation: {self.rotation}\n')
