from operator import itemgetter

from .validation.StringValidator import StringValidator

class Asset:
    '''
    A generic asset for blender.
    Attributes
    ----------
    lib: string
        Path to .blend file containing resource
    name: string
        Name of asset 
    '''
    lib = StringValidator(
                         minsize=1, 
                         additional_msg=".blend file containing resources"
                         )
    name = StringValidator(
                          minsize=1, 
                          additional_msg="Asset name"
                          )

    def __init__(self, desc={}):
        """
        Constructs the data object representing an asset. 
        
        Parameters
        -----------
            desc: dict
                dictionary representing asset information
        """
        (
        self.lib,
        self.name,
        ) = itemgetter(
                      'lib',
                      'name',
                      )(desc)

    def __str__(self):
        """
        Returns string with Asset object info.
        """
        return(
              'Asset:\n'
              '\tname:  {}\n'
              '\tlib:   {}\n' 
              .format(
                     self.name,
                     self.lib,
                     )
              )
