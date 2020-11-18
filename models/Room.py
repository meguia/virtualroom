from operator import itemgetter

from .Speaker import Speaker
from .Door import Door
from .Base import Base 
from .Spot import Spot
from .Camera import Camera
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
            elif(element == 'door'):
                self.door = Door(elements[element])
            elif(element == 'base'):
                self.base= Base(self.wall_thickness,elements[element]) 

        #self.spot = Spot(desc['spot'])
        self.lighting_elements = []
        for element in desc['lighting_elements']:
            if element['type'] == 'spot':
                self.lighting_elements.append(Spot(element))
        self.camera = Camera(desc['camera'])

    def __str__(self):
        """
        Returns string with Room object info.
        """
        return('\nRoom:\n'
              f' Name: { self.name }.\n'
               ' Dimensions:\n' 
              f'\tdepth:         { self.depth:6.2f }\n'  
              f'\twidth:         { self.width:6.2f }\n'  
              f'\theight:        { self.height:6.2f }\n'
              f'\twall thickness:{ self.wall_thickness:6.2f }\n'
              )

    def dump_room_info(self):
        """
        Returns string with all room's info.
        """
        roomString = self.__str__()
        speakerString = self.speaker.__str__()
        doorString = self.door.__str__()
        baseString = self.base.__str__()
        #spotString = self.spot.__str__()
        cameraString = self.camera.__str__()
        room_info = (
                    f'{roomString}'
                    f'{speakerString} ' 
                    f'{doorString}'
                    f'{baseString}'
                    f'{spotString}'
                    f'{cameraString}'
                    )
        return(room_info)


