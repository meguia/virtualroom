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

#CARGA CONFIGURACION
with open(json_file_input) as json_file:
    try:
        input = json.load(json_file)
    except json.JSONDecodeError as exc:
        print(exc)

room = Room(input['room'])
roomString = room.dump_room_info()
print(f'{roomString}')

render = False # si va a hacer el render
generate_template = False
# BORRA LO ANTERIOR 
cu.clear()
cu.clear_act()
# COLECCIONES compatibles con el pipeline para Unreal
col_sala = bm.iscol('Mesh')
col_luces = bm.iscol('Lights')
col_obj = bm.iscol('Mesh')
bm.link_col(col_sala)
bm.link_col(col_obj)
bm.link_col(col_luces)

# MATERIALES 
# carga los materiales con los atributos de substance y las rutas
# esto se podria hacer directamente en make_room
mat_dict_substance = room.materials_from_elements() # cambiar

if generate_template:
    data = room_utils.mat_getdict(mats_path, mat_dict_substance)
    with open(json_material_template,'w') as json_file:
        json.dump(data,json_file, indent=4, sort_keys=True)
        
# genera un diccionario de materiales de blender a partir del diccionario de materiales de substance
mat_dict = room_utils.mat_room(mats_path,presetdir,mat_dict_substance)


# CREA LA SALA
#Escala de los mapas UV orden paredes,piso,techo,puerta,zocalos
sala = room_utils.make_room(room,mat_dict,with_tiles=False)
bm.link_all(sala,col_sala)
 
#PARLANTE
# en lugar de speaker :-> sources (fuentes de sonido)
# ver como importar solo lo necesario
filepath = libdir / room.speaker.mesh_resource_name
with bpy.data.libraries.load(str(filepath)) as (data_from, data_to):
    try:
        data_to.objects = [name for name in data_from.objects]
    except UnicodeDecodeError as exc:
        print(exc)   
         
# room.sources.array (posiciones de las fuentes posiciones x,y)         
# room.sources.speaker name (Genelec, JBL, Edifier)
# room.sources.stand name (o type) (Floor_stand, Plate, None), data geometrica adicional, 
# solo altura en z para el acople del parlante

# las instancia se obtienen loopeando sobre room.sorces.array
print('Imported ', str(list(data_to.objects)))
pie = bpy.data.objects['Stand']
parlante = bpy.data.objects['Genelec']
pie.location = [room.speaker.x, room.speaker.y, room.speaker.z]
pie.rotation_euler = [0,0,radians(room.speaker.rotation)]
bm.list_link([pie,parlante],col_obj)

#LUCES
light_source, mount = room_utils.ceiling_lighting(room, bpy.data.objects[type(room.ceiling).__name__])
bm.list_link([light_source, mount],col_luces)

#bpy.context.view_layer.update()
#bm.apply_transforms(light_source)



#CAMARA 360
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
