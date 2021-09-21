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
from .CurtainArrangement import CurtainArrangement
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
            elif(element == 'curtain_arrangement'):
                self.curtain_arrangement = CurtainArrangement(elements[element]) 
            elif(element == 'cable_tray_arrangement'):
                self.cable_tray_arrangement = CableTrayArrangement(elements[element]) 
            elif(element == 'misc_assets_arrangement'):
                self.misc_assets_arrangement = MiscAssetArrangement(elements[element])

        self.lighting = Lighting(desc['lighting'])

        self.camera = Camera(desc['camera'])

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
        roomString = self.__str__()
        sourceString = self.source.__str__()
        baseString = self.base.__str__()
        wallString = self.wall.__str__()
        ceilingString = self.ceiling.__str__()
        floorString = self.floor.__str__()
        lightingString = self.lighting.__str__()
        curtainsArrangementString = self.curtain_arrangement.__str__()
        cableTrayArrangementString = self.cable_tray_arrangement.__str__()
        miscAssetsArrengementString = ''
        if self.misc_assets_arrangement is not None:
            miscAssetsArrengementString += self.misc_assets_arrangement.__str__()


        cameraString = self.camera.__str__()
        room_info = (
                    '\n------------------------------------------------------------\n'
                    '\n------------------------------------------------------------\n'
                    f'{roomString}'
                    '\n------------------------------------------------------------\n'
                    f'{sourceString} ' 
                    '\n------------------------------------------------------------\n'
                    f'{baseString}'
                    '\n------------------------------------------------------------\n'
                    f'{wallString}'
                    '\n------------------------------------------------------------\n'
                    f'{ceilingString}'
                    '\n------------------------------------------------------------\n'
                    f'{floorString}'
                    '\n------------------------------------------------------------\n'
                    f'{lightingString}'
                    '\n------------------------------------------------------------\n'
                    f'{cameraString}'
                    '\n------------------------------------------------------------\n'
                    f'{curtainsArrangementString}'
                    '\n------------------------------------------------------------\n'
                    f'{cableTrayArrangementString}'
                    '\n------------------------------------------------------------\n'
                    f'{miscAssetsArrengementString}'
                    '\n------------------------------------------------------------\n'
                    )
        return(room_info)

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
        materials = [
                    self.wall.material,
                    self.floor.material,
                    self.ceiling.material,
                    #self.door.material,
                    #self.door.frame.material,
                    self.base.material,
                    ]
        for material in self.wall.fetch_bands_materials():
            materials.append(material)
        for material in self.wall.fetch_doors_materials():
            materials.append(material)
        mat_dict_substance = {}
        for m in materials:
            mat_dict_substance[m.name] = m          
        return mat_dict_substance 

    def material_helper(self):
        materials = [
                    self.wall.material,
                    self.floor.material,
                    self.ceiling.material,
                    #self.door.material,
                    #self.door.frame.material,
                    self.base.material,
                    ]
        return materials
