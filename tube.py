
import sys
import bpy
import json
from pathlib import Path
homedir = Path.home() 
thisdir = homedir / 'virtualroom' 
savedir = homedir / 'Renders'
utildir = homedir / 'blender_utils'
libdir = thisdir / 'lib'
presetdir = thisdir / 'presets'
json_file_input = presetdir / 'sala_lapso.json'
json_material_template = thisdir / 'materials.json'
modelsdir = thisdir / 'models'
mats_path = homedir / 'Textures'

sys.path.append(str(utildir))   
sys.path.append(str(thisdir))   
sys.path.append(str(modelsdir)) 
import blender_methods as bm
import clear_utils as cu
import  room_utils 
from math import radians
import models
from models.Room import Room
import importlib as imp
imp.reload(room_utils)
imp.reload(models)
imp.reload(models.Room)

# BORRA LO ANTERIOR 
cu.clear()
cu.clear_act()
cylinder = bm.cylinder('Tube', n=16, mats = None, r=1.0, h=1.0, hlist=[0.0,1.0, 2.0 ,3.0, 4.0], pos = [0,0,0], rot = [0,0,0])
bpy.context.scene.collection.objects.link( bpy.data.objects['Tube'] )
