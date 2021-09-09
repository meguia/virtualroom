from ..Asset import Asset

class AssetManagerModel:
    """
    A class to represent a Model that manages assets.

    Attributes
    ----------
    assets: type Array/List 
        List of assets
    """
    def __init__(self, desc = {}):
        '''
        Constructs an array of assts and consumes its info from
        assets_info key in dictionary
        '''
        self.assets= []
        try:
            for asset_idx in range(len(desc)):
                asset = desc[asset_idx]
                self.assets.append(Asset(asset))

        except KeyError:
            error_msg = 'Missing assets_info key'
            print(error_msg)

    def assets_names_as_array(self):
        """
        Returns an array of strings containing assets names
        """
        return [asset.name for asset in self.assets]

    def libs_names_as_array(self):
        """
        Returns a unique list of libs names 
        """
        libs_list = [asset.lib for asset in self.assets]
        return list(set(libs_list))

    def __str__(self):
        """
        Returns asset names and libs
        """
        asset_names_str = self.assets_names_as_array()
        libs_str = self.libs_names_as_array()
        return(
              f'\t{ asset_names_str }\n'
              f'\t{ libs_str }\n'
              )
