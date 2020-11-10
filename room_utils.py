import sys
import os
from pathlib import Path
homedir = Path.home() 
utildir = homedir / 'blender_utils'
sys.path.append(str(utildir))   

import blender_methods as bm
import material_utils as mu
import uv_utils as uv
import importlib as imp
from math import radians, pow

imp.reload(bm)
imp.reload(uv)

def gray(val,alpha=1):
    return [val,val,val,alpha]


def make_room(dims = [1,1,1,0.1], base=None, frame=None, mats=None, door=[1,0.5, 0.1,0.5], scales=None, with_uv=True):
    # ROOMS
    # materials walls, floor, ceil, base, door
    print('ROOM:')
    (l,w,h,t) = dims # length, width, height, thickness
    (dn, dp, dw, dh) = door # wall number, position from border, width, height
    if scales is None:
        scales = [1]*5
    floor = bm.floor('floor',mats[1],dims=[l,w,-t])
    ceil = bm.floor('tceil',mats[2],pos=[0,0,h],dims=[l+2*t,w+2*t,t])
    rots = [radians(180),0,radians(90),radians(-90)]
    uv.uv_board(ceil.data, [w,l,t], front=0, scale = w/scales[2])
    uv.uv_board(floor.data, [w,l,t], front=0, scale = w/scales[1],rot90=True)
    if base is not None:
        w1,b1 = bm.wall('wall1',mats[0],pos=[0,-w/2,-t],rot=rots[0], dims=[l+2*t,h+t,t],basemat=mats[3],basedim=base)
        w2,b2 = bm.wall('wall2',mats[0],pos=[0,w/2,-t],rot=rots[1], dims=[l+2*t,h+t,t],basemat=mats[3],basedim=base)
        w3,b3 = bm.wall('wall3',mats[0],pos=[-l/2,0,-t],rot=rots[2], dims=[w,h+t,t],basemat=mats[3],basedim=base)
        w4,b4 = bm.wall('wall4',mats[0],pos=[l/2,0,-t],rot=rots[3], dims=[w,h+t,t],basemat=mats[3],basedim=base)
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
        if base is not None:
            uv.uv_board(b1.data, [l,base[0],base[1]], front=1, scale = w/scales[0])
            uv.uv_board(b2.data, [l,base[0],base[1]], front=1, scale = w/scales[0])
            uv.uv_board(b3.data, [w,base[0],base[1]], front=1, scale = w/scales[0])
            uv.uv_board(b4.data, [w,base[0],base[1]], front=1, scale = w/scales[0])
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
    if base is not None:
        bm.hole(eval('b'+str(dn)),hpos=hpos,hsize=hsize)
    if frame is not None:    
        door,fr = frame_door(mats[4],mats[3],dpos,rots[dn-1],[dw,dh,t],frame)
        if with_uv:
            uv.uv_planks(fr.data, scale = dh/scales[4])
        room_list.extend([door,fr])
    else:
        door = simple_door(mats[4],dpos,rots[dn-1],[dw,dh,t])   
        room.append(door)
    if with_uv:    
        uv.uv_board(door.data, [dw,dh,t], front=1, scale = dh/scales[3], rot90=True)    
    room = bm.list_parent('room',room_list)
    return room

def mat_room(paths, names, scales = None):
    mats = []
    matdicts = []
    maps = []
    if scales is None:
        scales = [[1.0,1.0,1.0]]*len(names)
    for p in paths:
        matdicts.append(mu.make_imagedict(p))
    for s in scales:
        maps.append(mu.Mapping(scale=s,coord='UV'))
    for n in range(len(names)):    
        mats.append(mu.texture_full_material(names[n],matdicts[n],mapping=maps[n]))
    return mats

def simple_door(mat_door,dpos,rot,dims):
    # simple door with no frame
    door = bm.wall('door',mat_door,pos=dpos,rot=rot,dims=dims)
    return door

def frame_door(mat_door,mat_frame,dpos,rot,dims,frame):
    # simple door with frame
    (fw, ft) = frame # frame width, thickness
    fpos = [dpos[0],dpos[1],dpos[2]+dims[1]/2]
    frame = bm.frame('frame',mat_frame,pos=fpos,rot=rot,dims_hole=dims,dims_frame=[fw,ft])
    dims[0] -= 2*ft
    dims[1] -= 2*ft
    dpos[2] += ft
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