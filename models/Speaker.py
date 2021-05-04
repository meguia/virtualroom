from operator import itemgetter
import glob
from pathlib import Path

from .validation.schema_validation_methods import validate_speaker_schema
from .validation.NumberValidator import NumberValidator
from .validation.StringValidator import StringValidator

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

    x = NumberValidator(additional_msg="Speaker x position")
    y = NumberValidator(additional_msg="Speaker y position")
    z = NumberValidator(additional_msg="Speaker z position")
    rotation = NumberValidator(additional_msg="Speaker rotation")
    mesh_resource_name= StringValidator(minsize=1, additional_msg="Speaker 3d model")

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
        #validate_speaker_schema(desc)
        (
        self.x,
        self.y,
        self.z,
        ) = itemgetter('x','y','z')(desc) 
        self.rotation = desc.get('rotation')
        #self.mesh_resource_name = itemgetter('3d_model')(desc)
        #self.path_resources = Path.home() / 'virtualroom/lib'
        #self.expected_mesh_path = self.path_resources / f'{self.mesh_resource_name}.blend'
        #matching_paths = glob.glob(str(self.expected_mesh_path))
        #if not matching_paths:
        #    error_msg = (
        #                'Could not find '
        #                f'{self.mesh_resource_name}.blend '
        #                f'on {self.path_resources}'
        #                )
        #    raise FileNotFoundError(error_msg)
        #if matching_paths:
        #    self.mesh_path = Path(matching_paths[0])

    def __str__(self):
        """
        Returns string with Speaker object info.
        """
        return(
              '\n\tX:             {:6.2f}\n'
              '\tY:             {:6.2f}\n'
              '\tZ:             {:6.2f}\n'
              '\tRotation:      {:6.2f}\n'
              .format(
                     self.x,
                     self.y,
                     self.z,
                     self.rotation
                     )
              )
