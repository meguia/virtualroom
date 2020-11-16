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
### ==========PARTE DEL SCRIPT PARA MODIFICAR =============================

#CARGA LAS RUTAS PARA LAS TEXTURAS
# Paredes concrete_raw_grey
#path_mat_paredes = mats_path / 'Concrete/concrete_raw_grey'
# Piso parquet_european_ash_grey
#path_mat_piso = mats_path / 'Wood/parquet_european_ash_grey'
# Techo plaster_acoustic_ceiling
#path_mat_techo = mats_path / 'Plaster/plaster_acoustic_ceiling'
# Puerta wood_wenge
#path_mat_puerta = mats_path / 'Wood/wood_wenge'
# Zocalos wood_black_walnut_stripped
#path_mat_zocalo = mats_path / 'Wood/wood_black_walnut_stripped'
render = False # si va a hacer el render

#PARAMETROS GEOMETRICOS DE LA SALA
#(largo,ancho,alto) = [12.10, 7.10, 3.00]
#(largo, ancho, alto) = [room.depth, room.width, room.height]
#esp = 0.15 # espesor de las paredes
#zoc = [esp+0.12, 0.025] # alto y espesor zocalos
##PARAMETROS DE LA PUERTA posicion < largo/2, ancho, alto
#puerta = [3, 2.5, 1.20, 2.20]
#frame = [0.08, 0.03] 
#POSICION DEL PARLANTE (coordenada z en 0)
#pos_parlante = [2,0,0]
# orientacion , el parlante original apunta hacia +x
#rot_parlante = radians(0)
# POSICION Y ORIENTACION DE LOS SPOTS
#pos_spot = [-5,1,2]
pos_spot = [room.spot.x, room.spot.y, room.spot.z]
#rot_spot = [radians(50), radians(-60), 0]
rot_spot = [radians(room.spot.rotX), radians(room.spot.rotY), radians(room.spot.rotZ)]
#POSICION DE LA CAMARA 360 (coordenada z en 1.5)
#pos_camara = [-3,0,1.5]
# orientacion de la parte frontal, la camara originalmente apunta hacia +y
rot_camara = radians(-90)

###===============NO MODIFICAR==========================================
# borra todo lo anterior
cu.clear_all()
# Crea tres colecciones separadas para sala luces y objetos y las linkea a la escena 
col_sala = bm.iscol('SALA')
col_luces = bm.iscol('LUCES')
col_obj = bm.iscol('OBJ')
bm.link_col(col_sala)
bm.link_col(col_obj)
bm.link_col(col_luces)

# MATERIALES CYCLES orden paredes,piso,techo,puerta,zocalos esto va en el json
names = ['Paredes','Piso','Techo','Puerta','Zocalo']
sbs_names = ['concrete_raw_grey','parquet_european_ash_grey','plaster_acoustic_ceiling','wood_wenge','wood_black_walnut_striped']
sbs_types = ['Concrete','Wood','Plaster','Wood','Wood']
maps = ['color', 'normal','specular','roughness','metal','bump']
scales = [1.0, 2.0, 6.0, 5.0, 1.0]
mats = room_utils.mat_room(names,mats_path,sbs_names,sbs_types,maps)
print(mats)
# CREA LA SALA
sala = room_utils.make_room(room,mats,scales)
bm.link_all(sala,col_sala)
 
#Agrega un Parlante en un pie fijo
#filepath = libdir / 'Genelec.blend'
filepath = room.speaker.mesh_path
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

#LUCES crea una diccionario con todos los parametros
Lp = {
    'name':'Spot1',
    'pos': pos_spot,
    'rot': rot_spot,
    'energy':1000,
    'size':radians(160.0),
    'blend':1
    }
spot1 = bm.new_spot(**Lp)    
# Spot simetrico
pos_spot[1] *= -1
rot_spot[0] *= -1
Lp['name']='Spot2'
Lp['pos']= pos_spot
Lp['rot']= rot_spot
spot2 = bm.new_spot(**Lp)
bm.list_link([spot1,spot2],col_luces)

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
