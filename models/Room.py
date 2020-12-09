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
from .ElementWithMaterial import ElementWithMaterial
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
    speaker: type Speaker
        represents a speaker placed in the room
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
            if(element == 'speaker'):
                self.speaker = Speaker(elements[element])
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

        #self.spot = Spot(desc['spot'])
        self.lighting_elements = []
        for element in desc['lighting_elements']:
            if element['type'] == 'spot':
                self.lighting_elements.append(Spot(element))

        self.materials = []
        for material in desc['materials']:
            self.materials.append(Material(material))

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
        speakerString = self.speaker.__str__()
        doorString = self.door.__str__()
        baseString = self.base.__str__()
        wallString = self.wall.__str__()
        ceilingString = self.ceiling.__str__()
        floorString = self.floor.__str__()
        lightingString = ""
        for element in self.lighting_elements:
            lightingString += f'{element.__str__()}'
        materialsString = ""
        for material in self.materials:
            materialsString += f'{material.__str__()}'
        cameraString = self.camera.__str__()
        room_info = (
                    f'{roomString}'
                    f'{speakerString} ' 
                    f'{doorString}'
                    f'{baseString}'
                    f'{wallString}'
                    f'{ceilingString}'
                    f'{floorString}'
                    f'{lightingString}'
                    f'{cameraString}'
                    f'{materialsString}'
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
        # orden paredes,piso,techo,puerta,zocalos
        materials = [
                    self.wall.material,
                    self.floor.material,
                    self.ceiling.material,
                    self.door.material,
                    self.door.frame.material,
                    self.base.material,
                    ]
        print(len(materials))            
        return materials

