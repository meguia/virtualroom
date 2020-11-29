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

render = False # si va a hacer el render
pos_spot = [room.spot.x, room.spot.y, room.spot.z]
rot_spot = [radians(room.spot.rotX), radians(room.spot.rotY), radians(room.spot.rotZ)]
rot_camara = radians(-90)
# MATERIALES CYCLES orden paredes,piso,techo,puerta,zocalos esto va en el json
names = ['Paredes','Piso','Techo','Puerta','Zocalo']
sbs_names = ['concrete_raw_grey','parquet_european_ash_grey','plaster_acoustic_ceiling','wood_wenge','wood_black_walnut_striped']
sbs_types = ['Concrete','Wood','Plaster','Wood','Wood']
maps = ['color', 'normal','specular','roughness','metal','bump']
scales = [2.0, 2.0, 6.0, 5.0, 1.0]
mats = room_utils.mat_room(names,mats_path,sbs_names,sbs_types,maps)
print(mats)
# CREA LA SALA
sala = room_utils.make_room(room,mats,scales)
bm.link_all(sala,col_sala)
 
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
