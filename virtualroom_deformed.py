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
mat_dict_substance = room.materials_from_elements() # cambiar

if generate_template:
    data = room_utils.mat_getdict(mats_path, mat_dict_substance)
    with open(json_material_template,'w') as json_file:
        json.dump(data,json_file, indent=4, sort_keys=True)
        
# genera un diccionario de materiales de blender a partir del diccionario de materiales de substance
mat_dict = room_utils.mat_room(mats_path,presetdir,mat_dict_substance)

# CREA LA SALA
#Escala de los mapas UV orden paredes,piso,techo,puerta,zocalos
scales = [1.0, 2.0, 6.0, 5.0, 1.0]
sala = room_utils.make_room(room,mat_dict,scales)
bm.link_all(sala,col_sala)
 
#LUCES
room_lighting_elements = []
for element in room.lighting_elements:
    if type(element).__name__ == 'Spot': 
        room_lighting_elements.append(bm.new_spot(**element.to_dict()))
bm.list_link(room_lighting_elements,col_luces)

for ob in sala.children:
    ob.select_set(True)
    if ob.name=='floor':
        bpy.context.view_layer.objects.active = ob
        
bpy.ops.object.join()
salaj = sala.children[0]
bm.simple_subdivide(salaj,10)
d1 = bm.deformmod(salaj,'Dx',axis='X',angle=5) 
d2 = bm.deformmod(salaj,'Dy',axis='Y',angle=5) 
d3 = bm.deformmod(salaj,'Dz',axis='Z',angle=5) 
tkeys = [1,20,50,80,110,140,170,200]
fx = [radians(x) for x in [0,0,2,3,3,2,0,0]]
fy = [radians(x) for x in [0,0,3,1,-3,-3,0,0]]
fz = [radians(x) for x in [0,0,3,-3,3,-3,0,0]]
skeys = [0]*8
bm.animate_curve(salaj,'twist','modifiers["Dx"].angle',tkeys,fx,skeys)
bm.animate_curve(salaj,'twist','modifiers["Dy"].angle',tkeys,fy,skeys)
bm.animate_curve(salaj,'twist','modifiers["Dz"].angle',tkeys,fz,skeys)


# Camara 360
bm.set_cycles()
eqcam =  bm.new_equirectangular(name='Cam360',
                                pos = [room.camera.x,room.camera.y,room.camera.z], 
                                rotation=[radians(90), 0, radians(room.camera.rotation)])
bm.link_all(eqcam,col_luces)

# Join Room


##RENDER CYCLES
# 4k para probar
#png_name = 'room360d.jpg'
#(w,h) = [4000,2000]
#bm.set_resolution(w,h)
#bm.set_render_cycles(samples = 128, clmp = 0.5, denoise = False, ao = True)
#bm.set_render_output(str(savedir / png_name),format='JPEG',quality=100)
#if render:
#    bm.render_cam(cam = eqcam)
#    print('Rendered ' + png_name)
#    room_utils.inject_metadata(thisdir,savedir/png_name,w,h)
#print('Finalizado')    
