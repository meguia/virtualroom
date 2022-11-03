from operator import itemgetter

from .Speaker import Speaker
from .Door import Door
from .Base import Base 
from .Spot import Spot
from .Camera import Camera
from .Wall import Wall
from .Ceiling import Ceiling
from .Floor import Floor
from .Material import Material
from .Lighting import Lighting
from .ElementWithMaterial import ElementWithMaterial
from .SoundSource import SoundSource
from .CableTrayArrangement import CableTrayArrangement
from .MiscAssetArrangement import MiscAssetArrangement

from .validation.schema_validation_methods import validate_room_schema 
from .validation.NumberValidator import NumberValidator


class Room:
    """
    A class to represent a room.

    Attributes
    ----------
    depth: float
        room's depth in meters
    width: float
        room's width in meters
    height: float
        room's height in meters
    wall_thickness: float
        room's walls thickness in meters
    source: type Source 
        represents sound sources present in the room
    door: type Door 
        represents a door placed in the room
    base: type Base 
        represents the room's skirting
    spot: type Spot
        represents a spot light placed in the room
    camera: type Camera
        represents a camera for Blender present in the room.

    """

    depth = NumberValidator(additional_msg="Room depth")
    width = NumberValidator(additional_msg="Room width")
    height = NumberValidator(additional_msg="Room height")
    wall_thickness = NumberValidator(additional_msg="Room wall thickness")

    def __init__(self, desc = {}):
        """
        Constructs all the necessary attributes for the room object.
        
        Parameters
        -----------
            desc: dict
                dictionary representing room's information
        """
        validate_room_schema(desc)
        self.name = desc['name']
        (
        self.depth, 
        self.width, 
        self.height,
        ) = itemgetter('depth',
                       'width', 
                       'height',
                       )(desc['dimensions'])
        self.wall_thickness = itemgetter('wall_thickness')(desc)
        elements = desc['elements']
        for element in elements: 
            if(element == 'source'):
                self.source = SoundSource(elements[element])
            elif(element == 'wall'):
                self.wall = Wall(elements[element])
            elif(element == 'ceiling'):
                self.ceiling = Ceiling(elements[element])
            elif(element == 'floor'):
                self.floor = Floor(elements[element])
            elif(element == 'door'):
                self.door = Door(elements[element])
            elif(element == 'base'):
                self.base= Base(self.wall_thickness,elements[element]) 
            elif(element == 'cable_tray_arrangement'):
                self.cable_tray_arrangement = CableTrayArrangement(elements[element]) 
            elif(element == 'misc_assets_arrangement'):
                self.misc_assets_arrangement = MiscAssetArrangement(elements[element])

        # check if ceiling or floor have not been created from config file
        # then create them
        if not hasattr(self, 'ceiling'):
            self.ceiling = Ceiling()
        if not hasattr(self, 'floor'):
            self.floor = Floor()

        try:
            self.lighting = Lighting(desc['lighting'])
        except KeyError as err:
            print('No lighting declared for floor')

        try:
            self.camera = Camera(desc['camera'])
        except KeyError as err:
            print('No camera declared for floor')

    def __str__(self):
        """
        Returns string with Room object info.
        """
        return(
              '\nRoom:\n'
              f' Name: { self.name }\n'
              'Dimensions:\n' 
              '\tdepth:         {:6.2f}\n' 
              '\twidth:         {:6.2f}\n'
              '\theight:        {:6.2f}\n' 
              '\twall thickness:{:6.2f}\n'
              .format(
                     self.depth, 
                     self.width,
                     self.height,
                     self.wall_thickness
                     )
              )

    def dump_room_info(self):
        """
        Returns string with all room's info.
        """
        room_string = ''
        room_string +='\n------------------------------------------------------------\n'
        room_string += self.__str__()
        room_string +='\n------------------------------------------------------------\n'
        if hasattr(self, 'source'):
            room_string +='\n------------------------------------------------------------\n'
            room_string += self.source.__str__()
        if hasattr(self, 'wall'):
            room_string +='\n------------------------------------------------------------\n'
            room_string += self.wall.__str__()
        if hasattr(self, 'ceiling'):
            room_string +='\n------------------------------------------------------------\n'
            room_string += self.ceiling.__str__()
        if hasattr(self, 'floor'):
            room_string +='\n------------------------------------------------------------\n'
            room_string += self.floor.__str__()
        if hasattr(self, 'lighting'):
            room_string +='\n------------------------------------------------------------\n'
            room_string += self.lighting.__str__()
            room_string +='\n------------------------------------------------------------\n'
        if hasattr(self, 'cable_tray_arrangement'):
            room_string +='\n------------------------------------------------------------\n'
            room_string += self.cable_tray_arrangement.__str__()
        if hasattr(self, 'misc_assets_arrangement'):
            room_string +='\n------------------------------------------------------------\n'
            room_string += self.misc_assets_arrangement.__str__()
        if hasattr(self, 'camera'):
            room_string +='\n------------------------------------------------------------\n'
            room_string += self.camera.__str__()
        return room_string

    def materials_names(self):
        """
        Returns an array with room materials name.
        """
        names = []
        for material in self.materials:
            names.append(material.name)
        return names

    def materials_categories(self):
        """
        Returns an array with room materials categories.
        """
        category_names = []
        for material in self.materials:
            category_names.append(material.category)
        return category_names

    def materials_from_elements(self):
        # check if elements have materials
        elements = [
                    self.wall,
                    self.floor,
                    self.ceiling,
                    #self.door,
                    #self.door.frame,
                    #self.base,
                    ]
        materials = [element.material for element in elements if hasattr(element, 'material')]
        for material in self.wall.fetch_bands_materials():
            materials.append(material)
        for material in self.wall.fetch_doors_materials():
            materials.append(material)
        mat_dict_substance = {}
        for m in materials:
            mat_dict_substance[m.name] = m          
        return mat_dict_substance 
