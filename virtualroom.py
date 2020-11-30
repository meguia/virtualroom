# Version 1 simple usando Cycles
# Usa materiales de Substance
import sys
import bpy
import json
from pathlib import Path
homedir = Path.home() 
thisdir = homedir / 'virtualroom' 
savedir = homedir / 'Renders'
utildir = homedir / 'blender_utils'
libdir = thisdir / 'lib'
json_file_input = thisdir / 'input.json'
modelsdir = thisdir / 'models'
# esta seria la unica para ajustar segun donde tenga casa uno, podemos probar algo en la 
# nube que quede con una referencia fija
mats_path = homedir / 'Textures'

sys.path.append(str(utildir))   
sys.path.append(str(thisdir))   
sys.path.append(str(modelsdir)) 
import blender_methods as bm
import clear_utils as cu
import  room_utils 
from math import radians
from models.Room import Room
import importlib as imp

imp.reload(room_utils)

with open(json_file_input) as json_file:
    try:
        input = json.load(json_file)
    except json.JSONDecodeError as exc:
        print(exc)

room = Room(input['room'])
roomString = room.dump_room_info()
print(f'{roomString}')

render = False # si va a hacer el render

rot_camara = radians(-90)

# borra todo lo anterior
cu.clear()
cu.clear_act()
# Crea tres colecciones separadas para sala luces y objetos y las linkea a la escena 
col_sala = bm.iscol('Mesh')
col_luces = bm.iscol('LUCES')
col_obj = bm.iscol('Mesh')
bm.link_col(col_sala)
bm.link_col(col_obj)
bm.link_col(col_luces)

# MATERIALES CYCLES orden paredes,piso,techo,puerta,zocalos
 # pasar esto a room utils
sbs_names = room.materials_textures()
sbs_types = room.materials_categories()
mats = room_utils.mat_room(mats_path,sbs_names,sbs_types)
print(mats)

# CREA LA SALA
#Escala de los mapas UV orden paredes,piso,techo,puerta,zocalos
scales = [1.0, 2.0, 6.0, 5.0, 1.0]
sala = room_utils.make_room(room,mats,scales)
bm.link_all(sala,col_sala)
 
#Agrega un Parlante en un pie fijo
#filepath = libdir / 'Genelec.blend'
filepath = libdir / room.speaker.mesh_resource_name
with bpy.data.libraries.load(str(filepath)) as (data_from, data_to):
    try:
        data_to.objects = [name for name in data_from.objects]
    except UnicodeDecodeError as exc:
        print(exc)    
print('Imported ', str(list(data_to.objects)))
pie = bpy.data.objects['Stand']
parlante = bpy.data.objects['Genelec']
#pie.location = pos_parlante
pie.location = [room.speaker.x, room.speaker.y, room.speaker.z]
pie.rotation_euler = [0,0,radians(room.speaker.rotation)]
bm.list_link([pie,parlante],col_obj)

room_lighting_elements = []
for element in room.lighting_elements:
    if type(element).__name__ == 'Spot': 
        room_lighting_elements.append(bm.new_spot(**element.to_dict()))

#LUCES crea una diccionario con todos los parametros
#Lp = {
#    'name':'Spot1',
#    'pos': pos_spot,
#    'rot': rot_spot,
#    'energy':1000,
#    'size':radians(160.0),
#    'blend':1
#    }
#spot1 = bm.new_spot(**Lp)    
# Spot simetrico
#pos_spot[1] *= -1
#rot_spot[0] *= -1
#Lp['name']='Spot2'
#Lp['pos']= pos_spot
#Lp['rot']= rot_spot
#spot2 = bm.new_spot(**Lp)
#bm.list_link([spot1,spot2],col_luces)
bm.list_link(room_lighting_elements,col_luces)

# Camara 360
bm.set_cycles()
eqcam =  bm.new_equirectangular(name='Cam360',
                                pos = [room.camera.x,room.camera.y,room.camera.z], 
                                rotation=[radians(90), 0, radians(room.camera.rotation)])
bm.link_all(eqcam,col_luces)

##RENDER CYCLES
# 4k para probar
png_name = 'room360d.jpg'
(w,h) = [4000,2000]
bm.set_resolution(w,h)
bm.set_render_cycles(samples = 128, clmp = 0.5, denoise = False, ao = True)
bm.set_render_output(str(savedir / png_name),format='JPEG',quality=100)
if render:
    bm.render_cam(cam = eqcam)
    print('Rendered ' + png_name)
    room_utils.inject_metadata(thisdir,savedir/png_name,w,h)
print('Finalizado')    
