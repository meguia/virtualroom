import pdb
import sys
import os
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

def make_room(room, mat_dict=None, scales=None, sbs_names=None, with_uv=True):
    # ROOMS
    # materials walls, floor, ceil, base, door
    print('ROOM:')
    # temporal para que corra por ahora 
    mats = []
    for names in sbs_names: 
        mats.append(mat_dict[names])
    (l,w,h,t) = [room.depth, room.width, room.height, room.wall_thickness] # length, width, height, thickness
    (dn, dp, dw, dh) = [room.door.wall_index, room.door.position, room.door.width, room.door.height] # wall number, position from border, width, height
    if scales is None:
        scales = [1]*5
    floor = bm.floor('floor',mats[1],dims=[l,w,-t])
    ceil = bm.floor('tceil',mats[2],pos=[0,0,h],dims=[l+2*t,w+2*t,t])
    rots = [radians(180),0,radians(90),radians(-90)]
    uv.uv_board(ceil.data, [w,l,t], front=0, scale = w/scales[2])
    uv.uv_board(floor.data, [w,l,t], front=0, scale = w/scales[1],rot90=True)
    if room.base is not None:
        basedim = [room.base.height, room.base.thickness]
        w1,b1 = bm.wall('wall1',mats[0],pos=[0,-w/2,-t],rot=rots[0], dims=[l+2*t,h+t,t],basemat=mats[3],basedim=basedim)
        w2,b2 = bm.wall('wall2',mats[0],pos=[0,w/2,-t],rot=rots[1], dims=[l+2*t,h+t,t],basemat=mats[3],basedim=basedim)
        w3,b3 = bm.wall('wall3',mats[0],pos=[-l/2,0,-t],rot=rots[2], dims=[w,h+t,t],basemat=mats[3],basedim=basedim)
        w4,b4 = bm.wall('wall4',mats[0],pos=[l/2,0,-t],rot=rots[3], dims=[w,h+t,t],basemat=mats[3],basedim=basedim)
        room_list = [w1,w2,w3,w4,floor,ceil,b1,b2,b3,b4]
    else:
        w1 = bm.wall('wall1',mats[0],pos=[0,-w/2,-t],rot=rots[0], dims=[l+2*t,h+t,t])
        w2 = bm.wall('wall2',mats[0],pos=[0,w/2,-t],rot=rots[1], dims=[l+2*t,h+t,t])
        w3 = bm.wall('wall3',mats[0],pos=[-l/2,0,-t],rot=rots[2], dims=[w,h+t,t])
        w4 = bm.wall('wall4',mats[0],pos=[l/2,0,-t],rot=rots[3], dims=[w,h+t,t])
        room_list = [w1,w2,w3,w4,floor,ceil]
    if with_uv:
        uv.uv_board(w1.data, [l,h,t], front=1, scale = w/scales[0])
        uv.uv_board(w2.data, [l,h,t], front=1, scale = w/scales[0])
        uv.uv_board(w3.data, [w,h,t], front=1, scale = w/scales[0])
        uv.uv_board(w4.data, [w,h,t], front=1, scale = w/scales[0])
        if room.base is not None:
            uv.uv_board(b1.data, [l,basedim[0],basedim[1]], front=1, scale = w/scales[0])
            uv.uv_board(b2.data, [l,basedim[0],basedim[1]], front=1, scale = w/scales[0])
            uv.uv_board(b3.data, [w,basedim[0],basedim[1]], front=1, scale = w/scales[0])
            uv.uv_board(b4.data, [w,basedim[0],basedim[1]], front=1, scale = w/scales[0])
    w0 = eval('w'+str(dn))
    sw = pow(-1,dn)
    if dn<3:
        hpos = [sw*(dp-l/2),w0.location[1],dh/2]
        dpos = [sw*(dp-l/2),w0.location[1]+sw*t/2,0]
        hsize=[dw, 3*t, dh]
        bm.hole(w0,hpos=hpos,hsize=hsize)
        if with_uv:
            uv.uv_board_with_hole(w0.data , [l,h,t], [dp-dw/2,t,dh,dw])
    else:
        hpos = [w0.location[0],sw*(w/2-dp),dh/2]    
        dpos = [w0.location[0]+sw*t/2,sw*(w/2-dp),0]    
        hsize=[3*t,dw, dh]
        bm.hole(w0,hpos=hpos,hsize=hsize)
        if with_uv:
            uv.uv_board_with_hole(w0.data, [w,h,t], [dp-dw/2,t,dh,dw])
    if basedim is not None:
        bm.hole(eval('b'+str(dn)),hpos=hpos,hsize=hsize)
    if room.door.frame is not None: 
        framedim = [room.door.frame.width, room.door.frame.thickness]   
        door,fr = frame_door(mats[4],mats[3],dpos,rots[dn-1],[dw,dh,t],framedim)
        if with_uv:
            uv.uv_planks(fr.data, scale = dh/scales[4])
        room_list.extend([door,fr])
    else:
        door = simple_door(mats[4],dpos,rots[dn-1],[dw,dh,t])   
        room.append(door)
    if with_uv:    
        uv.uv_board(door.data, [dw,dh,t], front=1, scale = dh/scales[3], rot90=True)    
    room_ = bm.list_parent('room',room_list)
    return room_

#def mat_room(path, sbs_names, sbs_types, scales = None):
def mat_room(path, materials, scales = None):
    sbs_names = [material.name for material in materials] 
    mats = dict.fromkeys(sbs_names,0)
    matdicts = []
    #texture names required
    maps = ['basecolor', 'normal','specular','roughness','metallic','height']
    for material in materials:
        # test if path exist if not creates the folder
        sbs_path = path / material.texture_path 
        #pdb.set_trace()
        if not os.path.exists(sbs_path):
            os.makedirs(sbs_path)
        # test if textures are generated if not 
        # render the sbsar using sbsar_utils
        if not all(mu.check_imagedict(sbs_path,maps)):
            print('render textures of ' + str(sbs_path))
            sbs.sbsar_render(sbs_path,material.name,maps)
        matdicts.append(mu.make_imagedict(sbs_path))
    #for n,sbs_name in enumerate(sbs_names):
    #    # test if path exist if not creates the folder
    #    sbs_path = path / sbs_types[n] / sbs_name
    #    if not os.path.exists(sbs_path):
    #        os.makedirs(sbs_path)
    #    # test if textures are generated if not 
    #    # render the sbsar using sbsar_utils
    #    if not all(mu.check_imagedict(sbs_path,maps)):
    #        sbs.sbsar_render(sbs_path,sbs_name,maps)
    #    matdicts.append(mu.make_imagedict(sbs_path))
    for n,name in enumerate(sbs_names):    
        mats[name] = mu.texture_full_material(name,matdicts[n],mapping=mu.Mapping(coord='UV'))
    return mats

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
