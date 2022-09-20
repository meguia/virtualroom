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
# Configuracion para probar oclusion de textura en el suelo
#json_file_input = presetdir / 'prueba_oclusion_sala_del_teatro.json'
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
#IMPORTAR assets de door
add_door_assets = any([len(door.assets)>0 for door in room.wall.fetch_doors() if(hasattr(door, 'assets'))])

if add_door_assets:
    assets_names = []
    assets_lib_names = []
    doors_with_assets =  [door for door in room.wall.fetch_doors() if(hasattr(door, 'assets'))]
    for door in doors_with_assets:
        assets_names.extend(door.assets_names_as_array())
        assets_lib_names.extend(door.libs_names_as_array())
    assets_names = list(set(assets_names))
    assets_lib_names = list(set(assets_lib_names))

    asset_object_array = []
    for asset_lib_name in assets_lib_names:
        lib_filepath = libdir / asset_lib_name
        with bpy.data.libraries.load(str(lib_filepath)) as (data_from, data_to):
            for name in data_from.objects:
                for asset_name in assets_names:
                    if (name == asset_name):
                         data_to.objects.append(name)
        asset_object_array += [ob for ob in bpy.data.objects if ob.name in assets_names]
        asset_object_array = list(set(asset_object_array))
    try:
        if(not len(asset_object_array) > 0):
            raise ValueError
        sala = room_utils.make_room(
                                    room,
                                    mat_dict,
                                    with_tiles=False,
                                    asset_data=asset_object_array
                                    )
        bm.link_all(sala,col_sala)
    except ValueError as err:
            print(repr(err) + 'Door assets empty')
else:
    sala = room_utils.make_room(room,mat_dict,with_tiles=False)
    bm.link_all(sala,col_sala)
 
# CARGA SPEAKER y STAND de la libreria source
filepath = libdir / room.source.lib

with bpy.data.libraries.load(str(filepath)) as (data_from, data_to):
    for name in data_from.objects:
        if (name == room.source.speaker_name) or name.startswith(room.source.stand_name):
             data_to.objects.append(name)
         
#PARLANTES
print('Imported ', str(list(data_to.objects)))
stand_data_array = [ob.data for ob in bpy.data.objects if ob.name.startswith(room.source.stand_name)]
print(stand_data_array)
speaker_data = bpy.data.objects[room.source.speaker_name].data
print(speaker_data)
speaker_height = 0.0
if room.source.stand_name == 'Floor_Stand':
    speaker_height = room.source.height
else:
    speaker_height = bpy.data.objects[room.source.stand_name].location[2]
    if room.source.stand_name == 'Tilt_Stand':
        point_camera = True
    
object_list = room_utils.make_speaker_array(room, speaker_data, stand_data_array, speaker_height, point_camera)
bm.list_link(object_list, col_obj)

#LUCES
# importar asset
if(room.lighting.light_source.object == 'asset'):
    assets_names = room.lighting.light_source.assets_names_as_array()
    asset_object_array = []
    for asset_lib_name in room.lighting.light_source.libs_names_as_array():
        lib_filepath = libdir / asset_lib_name
        with bpy.data.libraries.load(str(lib_filepath)) as (data_from, data_to):
            for name in data_from.objects:
                for asset_name in assets_names:
                    if (name == asset_name):
                         data_to.objects.append(name)
        asset_object_array += [ob for ob in bpy.data.objects if ob.name in assets_names]
    if(len(room.lighting.positions) > 0):
        light_source, mount = room_utils.ceiling_lighting_by_positions(
                                                                      room, 
                                                                      bpy.data.objects[type(room.ceiling).__name__], 
                                                                      asset_object_array
                                                                      )
        bm.list_link(light_source,col_luces)
        bm.list_link(mount,col_luces)
    else:
        light_source, mount = room_utils.ceiling_lighting(
                                                         room, 
                                                         bpy.data.objects[type(room.ceiling).__name__],
                                                         asset_object_array
                                                         )
        bm.list_link([light_source, mount],col_luces)
else:
    light_source, mount = room_utils.ceiling_lighting(room, bpy.data.objects[type(room.ceiling).__name__])
    bm.list_link([light_source, mount],col_luces)

#CABLE TRAY 
# import assets
if(room.cable_tray_arrangement is not None):
    assets_names = room.cable_tray_arrangement.assets_names_as_array()
    asset_object_array = []
    # este for no se si esta bien
    for asset_lib_name in room.cable_tray_arrangement.libs_names_as_array():
        lib_filepath = libdir / asset_lib_name
        with bpy.data.libraries.load(str(lib_filepath)) as (data_from, data_to):
            for name in data_from.objects:
                for asset_name in assets_names:
                    if (name == asset_name):
                         data_to.objects.append(name)
        asset_object_array = [ob for ob in bpy.data.objects if ob.name in assets_names]
        # aca va funcion de room utls
    cable_tray = room_utils.make_cable_tray(room, asset_object_array)
    bm.list_link(cable_tray,col_obj)

#bpy.context.view_layer.update()
#bm.apply_transforms(light_source)

#MISCELLANEOUS ASSETS
#import assets
if(room.misc_assets_arrangement is not None):
    assets_names = room.misc_assets_arrangement.assets_names_as_array()
    asset_object_array = []
    for asset_lib_name in room.misc_assets_arrangement.libs_names_as_array():
        lib_filepath = libdir / asset_lib_name
        with bpy.data.libraries.load(str(lib_filepath)) as (data_from, data_to):
            for name in data_from.objects:
                for asset_name in assets_names:
                    if (name == asset_name):
                         data_to.objects.append(name)
        asset_object_array = [ob for ob in bpy.data.objects if ob.name in assets_names]
    misc_objects = room_utils.create_misc_objects(room, asset_object_array)
    bm.list_link(misc_objects, col_obj)

#CAMARA 360
bm.set_cycles()
eqcam =  bm.new_equirectangular(name='Cam360',
                                pos = [room.camera.x,room.camera.y,room.camera.z], 
                                rotation=[radians(90), 0, radians(room.camera.rotation)])
bm.link_all(eqcam,col_luces)

##RENDER CYCLES
# 4k para probar
png_name = 'room360d.jpg'
(w,h) = [8000,4000]
bm.set_resolution(w,h)
bm.set_render_cycles(samples = 128, clmp = 0.5, denoise = True, ao = True)
bm.set_render_output(str(savedir / png_name),format='JPEG',quality=100)
if render:
    bm.render_cam(cam = eqcam)
    print('Rendered ' + png_name)
    room_utils.inject_metadata(thisdir,savedir/png_name,w,h)
print('Finalizado')    
