from operator import itemgetter
import glob
from pathlib import Path

from .validation.schema_validation_methods import validate_speaker_schema
from .validation.NumberValidator import NumberValidator
from .validation.StringValidator import StringValidator

from .Speaker import Speaker

class SoundSource:
    """
    A class to represent sound sources on the room.

    Attributes
    ----------
                "lib": "Genelec.blend",
                "speaker": "Genelec",
                "stand": "Stand",
    lib: string
        Path to .blend file containing resources
    speaker_name: string
        Name of speaker resource
    stand_name: string
        Name of stand resource
    height: float
        Speakers height value
    positions 
        Array of speaker objects
    """

    lib = StringValidator(
                         minsize=1, 
                         additional_msg=".blend file container resources"
                         )
    speaker_name = StringValidator(
                                   minsize=1, 
                                   additional_msg="Speaker resource name"
                                   )
    stand_name = StringValidator(minsize=1, additional_msg="Stand resource name")
    height = NumberValidator(1.20, 1.75, additional_msg="Stand height must be bigger than 1.20 and smaller than 1.75")

    def __init__(self, desc = {}):
        """

        Constructs all the necessary attributes for the sound source object.
        
        Parameters
        -----------
            desc: dict
                dictionary representing Sounde source info
        """
        #validate_speaker_schema(desc)
        (
        self.lib,
        self.speaker_name,
        self.stand_name,
        self.height,
        ) = itemgetter(
                      'lib',
                      'speaker',
                      'stand',
                      'height')(desc) 

        self.positions_from_data = []
        for pos in desc['positions']:
            self.positions_from_data.append(Speaker(pos))

        self.positions = []
        self.positions = self.positions_from_data

    def __str__(self):
        """
        Returns string with Speaker object info.
        """
        speakerString = ''
        for speaker in self.positions:
            index = self.positions.index(speaker)
            speakerString += '\nSpeaker '+str(index)
            speakerString += speaker.__str__()

        return(' Sound source:\n'
               '\tResource file:     {0}\n'
               '\tSpeaker name:      {1}\n'
               '\tStand   name:      {2}\n'
               '\tSpeaker Positions:\n'
               '\t{3}'
               .format(
                      self.lib,
                      self.speaker_name,
                      self.stand_name,
                      speakerString,
                      )
               )
