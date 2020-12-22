from operator import itemgetter
from pathlib import Path

from .validation.StringValidator import StringValidator

class Material:
    """
    A class to represent a material texture.

    Attributes
    ----------
    name: string 
        material name 
    category: string 
        texture category 
    texture_path: string 
        path to texture 

    """
    name = StringValidator(additional_msg="Material Name value")
    category= StringValidator(additional_msg="Material Category value")

    def __init__(self, desc = {}):
        """
        Constructs all the necessary attributes for the Material object.
        
        Parameters
        -----------
            desc: dict
                dictionary representing material's information
        """
        (
        self.sbs_name,
        self.category,
        self.preset,
        ) = itemgetter('sbs_name',
                       'category',
                       'preset'
                       )(desc)
        self.name = self.sbs_name + '_' + self.preset
        self.texture_path = Path(
                                self.category,
                                self.name
                                )
        self.sbs_file = str(Path(self.category , self.sbs_name)) + '.sbsar'
        if 'displacement' in desc.keys():
            self.displacement = desc['displacement']

    def __str__(self):
        """
        Returns string with Material object info.
        """
        return('Material:\n'
               '\tName:          {0}\n'
               '\tCategory:      {1}\n'
               '\tPath:          {2}\n'
               '\tPreset:        {3}\n'
               .format(
                      self.name,
                      self.category,
                      self.texture_path,
                      self.preset  
                      )
               )
