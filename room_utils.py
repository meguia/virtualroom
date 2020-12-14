from operator import truediv
import pdb
import sys
import os
import json
from pathlib import Path
homedir = Path.home() 
utildir = homedir / 'blender_utils'
thisdir = homedir / 'virtualroom' 
sys.path.append(str(utildir)) 
sys.path.append(str(thisdir))  

import blender_methods as bm
import material_utils as mu
import uv_utils as uv
import sbsar_utils as sbs
from math import radians, pow
import importlib as imp
imp.reload(bm)
imp.reload(mu)
imp.reload(sbs)

def make_room(room, mat_dict=None, with_uv=True):
    # ROOMS
    # materials walls, floor, ceil, base, door
    print('ROOM:')
    # temporal para que corra por ahora 
    (l,w,h,t) = [room.depth, room.width, room.height, room.wall_thickness] # length, width, height, thickness
    (dn, dp, dw, dh) = [room.door.wall_index, room.door.position, room.door.width, room.door.height] # wall number, position from border, width, height
    floor = bm.floor('floor', mat_dict[room.floor.material.name],pos=[0,0,-t],dims=[l,w,t])
    ceil = bm.floor('tceil',mat_dict[room.ceiling.material.name],pos=[0,0,h],dims=[l+2*t,w+2*t,t])
    rots = [radians(180),0,radians(90),radians(-90)]
    uv.uv_board(ceil.data, [w,l,t], front=0, scale = w/room.ceiling.uv_scale)
    uv.uv_board(floor.data, [w,l,t], front=0, scale = w/room.floor.uv_scale,rot90=True)
    mat_wall = mat_dict[room.wall.material.name]
    mat_base = mat_dict[room.base.material.name]
    if room.base is not None:
        basedim = [room.base.height, room.base.thickness]
        w1,b1 = bm.wall('wall1',mat_wall,pos=[0,-w/2,-t],rot=rots[0], dims=[l+2*t,h+t,t],basemat=mat_base,basedim=basedim)
        w2,b2 = bm.wall('wall2',mat_wall,pos=[0,w/2,-t],rot=rots[1], dims=[l+2*t,h+t,t],basemat=mat_base,basedim=basedim)
        w3,b3 = bm.wall('wall3',mat_wall,pos=[-l/2,0,-t],rot=rots[2], dims=[w,h+t,t],basemat=mat_base,basedim=basedim)
        w4,b4 = bm.wall('wall4',mat_wall,pos=[l/2,0,-t],rot=rots[3], dims=[w,h+t,t],basemat=mat_base,basedim=basedim)
        room_list = [w1,w2,w3,w4,floor,ceil,b1,b2,b3,b4]
    else:
        w1 = bm.wall('wall1',mat_wall,pos=[0,-w/2,-t],rot=rots[0], dims=[l+2*t,h+t,t])
        w2 = bm.wall('wall2',mat_wall,pos=[0,w/2,-t],rot=rots[1], dims=[l+2*t,h+t,t])
        w3 = bm.wall('wall3',mat_wall,pos=[-l/2,0,-t],rot=rots[2], dims=[w,h+t,t])
        w4 = bm.wall('wall4',mat_wall,pos=[l/2,0,-t],rot=rots[3], dims=[w,h+t,t])
        room_list = [w1,w2,w3,w4,floor,ceil]
    if with_uv:
        wall_scale = room.wall.uv_scale
        uv.uv_board(w1.data, [l,h,t], front=1, scale = w/wall_scale)
        uv.uv_board(w2.data, [l,h,t], front=1, scale = w/wall_scale)
        uv.uv_board(w3.data, [w,h,t], front=1, scale = w/wall_scale)
        uv.uv_board(w4.data, [w,h,t], front=1, scale = w/wall_scale)
        if room.base is not None:
            base_scale = room.base.uv_scale
            uv.uv_board(b1.data, [l,basedim[0],basedim[1]], front=1, scale = w/base_scale)
            uv.uv_board(b2.data, [l,basedim[0],basedim[1]], front=1, scale = w/base_scale)
            uv.uv_board(b3.data, [w,basedim[0],basedim[1]], front=1, scale = w/base_scale)
            uv.uv_board(b4.data, [w,basedim[0],basedim[1]], front=1, scale = w/base_scale)
    w0 = eval('w'+str(dn))
    sw = pow(-1,dn)
    if dn<3:
        hpos = [sw*(dp-l/2),w0.location[1],dh/2]
        dpos = [sw*(dp-l/2),w0.location[1]+sw*t/2,0]
        hsize=[dw, 3*t, dh]
        bm.hole(w0,hpos=hpos,hsize=hsize)
        #if with_uv:
            #uv.uv_board_with_hole(w0.data , [l,h,t], [dp-dw/2,t,dh,dw])
    else:
        hpos = [w0.location[0],sw*(w/2-dp),dh/2]    
        dpos = [w0.location[0]+sw*t/2,sw*(w/2-dp),0]    
        hsize=[3*t,dw, dh]
        bm.hole(w0,hpos=hpos,hsize=hsize)
        #if with_uv:
            #uv.uv_board_with_hole(w0.data, [w,h,t], [dp-dw/2,t,dh,dw])
    if basedim is not None:
        bm.hole(eval('b'+str(dn)),hpos=hpos,hsize=hsize)
    if room.door.frame is not None: 
        framedim = [room.door.frame.width, room.door.frame.thickness]   
        door,fr = frame_door(mat_dict[room.door.material.name],mat_dict[room.door.frame.material.name],dpos,rots[dn-1],[dw,dh,t],framedim)
        if with_uv:
            uv.uv_planks(fr.data, scale = dh/room.door.frame.uv_scale)
        room_list.extend([door,fr])
    else:
        door = simple_door(mat_dict[room.door.material.name],dpos,rots[dn-1],[dw,dh,t])   
        room.append(door)
    if with_uv:    
        uv.uv_board(door.data, [dw,dh,t], front=1, scale = dh/room.door.uv_scale, rot90=True)    
    room_ = bm.list_parent('room',room_list)
    return room_

def mat_getdict(path, materials):
    '''
    Return dictionary with template for json from materials substance dictionary 
    (without presets, only defaults)
    '''
    data = {}
    for m in materials.values():
        sbsar_file = str(path / m.sbs_file) 
        parameters = sbs.sbsar_loadparam(str(sbsar_file))
        data[m.sbs_name] = parameters
    return data    

def mat_room(mats_path, preset_path, materials):
    '''
    Generates a dictionary of blender materials from a dictionary of substance materials
    Also generate all textures if they are not generated or were generated with different 
    parameter values. Invoke texture_full_material for creating the material with the
    default shader node structure
    '''
    
    mat_dict = dict.fromkeys(materials.keys(),0)
    imagedicts = []
    #texture names required 
    channels = ['basecolor', 'normal','specular','roughness','metallic','height']
    for mat_name, material in materials.items():
        generate_textures = False
        # load parameters from preset (esto puede ir cuando se instancia el material) ###########
        with open(str(preset_path / material.preset) + '.json') as json_file:
            preset = json.load(json_file)
            parameters = preset[material.sbs_name]
        # test if path exist if not creates the folder
        texture_path = mats_path / material.texture_path
        sbs_path = mats_path / material.sbs_file
        if not os.path.exists(texture_path):
            # the material folder was not even created 
            os.makedirs(texture_path)
            generate_textures = True
        else:     
            # the material folder exists
            if not all(mu.check_imagedict(texture_path,channels)):
                 #not all textures were generated
                generate_textures = True
            else:     
                # the material folder exists and all textures were generated
                # then it is presumed that a parameters.json exists
                with open(str(texture_path / 'parameters.json')) as json_file:
                    parameters_generated = json.load(json_file)
                if parameters != parameters_generated:
                    # (agregar un chequeo de diferencia minima)
                    generate_textures = True    
        if generate_textures:
            print('rendering textures of ' + str(texture_path))
            sbs.sbsar_render(sbs_path,texture_path,mat_name,channels,parameters)
        imagedict = mu.make_imagedict(texture_path)
        mat_dict[mat_name] = mu.texture_full_material(mat_name,imagedict,mapping=mu.Mapping(coord='UV'))
    return mat_dict

def simple_door(mat_door,dpos,rot,dims):
    # simple door with no frame
    door = bm.wall('door',mat_door,pos=dpos,rot=rot,dims=dims)
    return door

def frame_door(mat_door,mat_frame,dpos,rot,dims,framedim):
    # simple door with frame
    fpos = [dpos[0],dpos[1],dpos[2]+dims[1]/2]
    frame = bm.frame('frame',mat_frame,pos=fpos,rot=rot,dims_hole=dims,dims_frame=framedim)
    dims[0] -= 2*framedim[1]
    dims[1] -= 2*framedim[1]
    dpos[2] += framedim[1]
    door = bm.wall('door',mat_door,pos=dpos,rot=rot,dims=dims)
    return door, frame

def wall_tiles(tile,dims,base,frame,door):
    # cover walls with tiles using array. cut the tiles at the end of the wall
    (l,w,h) = dims # length, width, height, thickness
    (dn, dp, dw, dh) = door # wall number, position, width, height
    tile.location=[-l/2+0.5,-w/2,0.5+base[0]]
    tile.rotation_euler=[radians(90),0,0]
    panelx = tile.modifiers.new(name='tilex', type='ARRAY')
    panelx.fit_type = 'FIT_LENGTH'
    panelx.fit_length = l-1
    panelx.relative_offset_displace = [1,0,0]
    panely = tile.modifiers.new(name='tiley', type='ARRAY')
    panely.fit_type = 'FIT_LENGTH'
    panely.fit_length = h-1
    panely.relative_offset_displace = [0,1,0]
    return [tile]
    
    
    

def inject_metadata(direxe,pathimg,w=4000,h=2000):
    # inyecta metadata
    metadata360 = {
    'ProjectionType'               : 'equirectangular',
    'InitialHorizontalFOVDegrees'  : 130,
    'PoseHeadingDegrees'           : 0,
    'PosePitchDegrees'             : 0,
    'FullPanoWidthPixels'          : w,
    'FullPanoHeightPixels'         : h,
    'CroppedAreaImageWidthPixels'  : w,
    'CroppedAreaImageHeightPixels' : h,
    'CroppedAreaLeftPixels'        : 0,
    'CroppedAreaTopPixels'         : 0,
    'UsePanoramaViewer'            : True,
    'artist'                       : 'LAPSo'}
    pars = ['-' + it[0] + '=' + str(it[1]) for it in metadata360.items()]
    if os.name is 'posix':
        file = str(pathimg).replace(" ", "\\ ")
        cmd = 'exiftool' + ' ' + ' '.join(pars) + ' '  + file
    else:    
        cmd = str(direxe) + '\exiftool' + ' ' + ' '.join(pars) + ' '  + str(pathimg)
    print(cmd)
    os.system(cmd)
