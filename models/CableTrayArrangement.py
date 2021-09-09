from operator import itemgetter

from .validation.NumberValidator import NumberValidator
from .validation.StringValidator import StringValidator

from .extra.AssetManagerModel import AssetManagerModel

class CableTrayArrangement(AssetManagerModel):
    '''
    A class to represent a Cable Tray Arrangement 
    Attributes
    ----------
    
    x_offset: float
     _  absolute distance between tray and roof along the x axis
    y_offset: float
     _  absolute distance between tray and roof along the y axis
    z_offset: float
        absolute distance between tray and roof along the z axis
    assets: list 
        list of tray assets: ie Tray and TrayConnector
    config: list
        list of configuration for conditional placing of tray and tray
        connector on different walls
    '''
    
    x_offset = NumberValidator(minvalue= 0.0, additional_msg="X offest")
    y_offset = NumberValidator(minvalue= 0.0, additional_msg="Y offest")
    z_offset = NumberValidator(minvalue= 0.0, additional_msg="Z offest")

    def __init__(self, desc= {}):
        """
        Constructs all the necessary attributes for the CableTrayArrangement object.
        
        Parameters
        -----------
            desc: dict
                dictionary representing cable tray arrangement information
        """
        try:
            super().__init__(desc['assets_info'])
        except KeyError as err:
            print(repr(err))
            print('missing assets_info key')
        (
        self.x_offset,
        self.y_offset,
        self.z_offset,
        ) = itemgetter(
                      'x-offset',
                      'y-offset',
                      'z-offset',
                      )(desc)

        self.config = []
        if 'config' in desc:
            for configuration in desc['config']:
                self.config.append({
                                    'Wall_index': configuration['wall_index'],
                                    'Tray': configuration['has_tray'], 
                                    'Connector': configuration['has_connector'],
                                  })
        else:
            for idx in range(4):
                self.config.append({
                                    'Wall_index': True,
                                    'Tray': True, 
                                    'Connector': True,
                                  })

    def __str__(self):
        """
        Returns string with CalbeTrayArrangement object info.
        """
        assets_string = ''
        if(len(self.assets) > 0):
            for asset in self.assets:
                assets_string += asset.__str__()
        config_string = ''
        if(len(self.config) > 0):
            config_string += '\tTray and connector config:\n'
            for conf in self.config:
                config_string += '\tWall index ' + str(conf['Wall_index']) +':\n'
                config_string += '\tTray: '+ str(conf['Tray'])+'\n'
                config_string += '\tConnector: '+ str(conf['Connector'])+'\n'

        
        return(
              'Cable Tray Arrangement:\n'
              '\tX offset:{0:6.2f}\n'
              '\tY offset:{1:6.2f}\n'
              '\tZ offset:{2:6.2f}\n'
              f'{ assets_string }\n'
              f'{ config_string }'
              .format(
                     self.x_offset,
                     self.y_offset,
                     self.z_offset,
                     )
               ) 

    def get_wall_config_by_wall_index(self, wall_index):
        try:
            for conf in self.config:
                if wall_index == conf['Wall_index']:    
                    return ({'Tray': conf['Tray'], 'Connector': conf['Connector']})
            raise ValueError('Could not find config with specified wall index') 
        except Exception as error:
            print('Error '+repr(error))
