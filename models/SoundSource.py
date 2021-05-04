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
    positions 
        Array of speaker objects
    """
    STAND_HEIGHT = 1.535
    PLATESTAND_HEIGHT = 0.27

    lib = StringValidator(
                         minsize=1, 
                         additional_msg=".blend file containen resources"
                         )
    speaker_name = StringValidator(
                                   minsize=1, 
                                   additional_msg="Speaker resource name"
                                   )
    stand_name = StringValidator(minsize=1, additional_msg="Stand resource name")

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
        ) = itemgetter(
                      'lib',
                      'speaker',
                      'stand')(desc) 

        self.positions_from_data = []
        for pos in desc['positions']:
            self.positions_from_data.append(Speaker(pos))

        self.positions = []
        self.positions = self.positions_from_data
        if self.stand_name == 'Stand':
            for pos in self.positions:
                # add stand height
                pos.z = self.STAND_HEIGHT
        elif self.stand_name == 'Plate_Stand':
            for pos in self.positions:
                # add stand height
                pos.z = self.PLATESTAND_HEIGHT 

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
