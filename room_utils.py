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
from math import radians, pow, pi
import importlib as imp
imp.reload(bm)
imp.reload(mu)
imp.reload(uv)
imp.reload(sbs)

def make_room(room, mat_dict=None, with_uv=True, with_tiles=False):
    '''
    Makes room as objects parented to an empty
    the objects are defined in the class Room
    mat_dict contains a dictionary of substance materiales
    also asigns uv maps (and lightmaps) to objects with scale
    '''
    (l,w,h,t) = [room.depth, room.width, room.height, room.wall_thickness] # length, width, height, thickness
    (dn, dp, dw, dh) = [room.door.wall_index, room.door.position, room.door.width, room.door.height] # wall number, position from border, width, height
    # Makes floor and ceiling
    floor = bm.floor(type(room.floor).__name__, mat_dict[room.floor.material.name],pos=[0,0,-t],dims=[l,w,t])
    ceil = bm.floor(type(room.ceiling).__name__,mat_dict[room.ceiling.material.name],pos=[0,0,h],dims=[l+2*t,w+2*t,t])
    if with_uv:
        uv.uv_board(ceil.data, [l,w,t], front=1, scale = room.ceiling.uv_scale)
        uv.uv_board(floor.data, [l+2*t,w+2*t,t], front=2, scale = room.floor.uv_scale)
    room_list = [floor,ceil]    
    # Makes walls with bases in a loop
    # first define rotation, position, door position, main dimension (dim)
    rots = [radians(180),0,radians(90),radians(-90)]
    pos=[[0,-w/2,-t],[0,w/2,-t],[-l/2,0,-t],[l/2,0,-t]]
    dpos = [[l/2-dp-dw/2,-w/2-t/2,0],[-l/2+dp+dw/2,w/2+t/2,0],[-l/2-t/2,-w/2+dp+dw/2,0],[l/2+t/2,w/2-dp-dw/2,0]]
    dim=[l+2*t,l+2*t,w,w]
    tdim = 0.005
    pos2=[[l/2,-w/2+tdim],[-l/2,w/2-tdim],[-l/2+tdim,-w/2],[l/2-tdim,w/2]]
    dpos2 = [[l/2-dp,-w/2+tdim,l/2-dp-dw,-w/2+tdim],[-l/2+dp,w/2-tdim,-l/2+dp+dw,w/2-tdim],
            [-l/2+tdim,-w/2+dp,-l/2+tdim,-w/2+dp+dw],[l/2-tdim,w/2-dp,l/2-tdim,w/2-dp-dw]]
    dim2=[l,l,w,w]

    # For placing the hole an array giving None when there is no hole and the dimensions 
    # of the hole in  the dn wall
    hole=[None]*4
    hole[dn] = [dp, t, dw, dh, dpos2[dn]]
    for n in range(4):
        if room.base is not None:
            basedim = [dim[n], room.base.height, room.base.thickness]
            w,b = bm.wall('wall_' + str(n),mat_dict[room.wall.material.name] ,pos=pos[n],rot=rots[n],dims=[dim[n],h+t,t],hole=hole[n],
                        basemat= mat_dict[room.base.material.name],basedim=[room.base.height, room.base.thickness])            
            if with_uv:
                if n==dn:
                    uv.uv_board_with_hole(b.data,basedim,hole[dn],scale=room.wall.uv_scale,internal=False)
                else:
                    uv.uv_board(b.data,basedim,scale=room.base.uv_scale)    
            room_list.append(b)   
            if with_tiles:
                pos2[n].append(basedim[1]-t)
                print(n)
                tiles =  wall_tiles('tiles_' +str(n),[dim2[n],h-basedim[1]+t],[1,1],pos=pos2[n],rot=[radians(90),0,rots[n]],hole=hole[n],mats=None)
                room_list.extend(tiles)       
        else:
            w = bm.wall('wall_' + str(n),mat_dict[room.wall.material.name] ,pos=pos[n],rot=rots[n],dims=[dim[n],h+t,t],hole=hole[n])
        if with_uv:
            if n==dn:
                uv.uv_board_with_hole(w.data,[dim[n],h+t,t],hole[dn],scale=room.wall.uv_scale)
            else:
                uv.uv_board(w.data,[dim[n],h+t,t],scale=room.wall.uv_scale)
        room_list.append(w)    
    # Makes door and frame 
    if room.door.frame is not None: 
        framedim = [room.door.frame.width, room.door.frame.thickness]   
        door,fr = frame_door(mat_dict[room.door.material.name],mat_dict[room.door.frame.material.name],dpos[dn],rots[dn],[dw,dh,t],framedim)
        if with_uv:
            uv.uv_planks(fr.data, scale = room.door.frame.uv_scale)
        room_list.extend([door,fr])
    else:
        door = simple_door(mat_dict[room.door.material.name],dpos[dn],rots[dn],[dw,dh,t])   
        room.append(door)
    if with_uv:    
        uv.uv_board(door.data,[dw,dh,t],scale=room.door.uv_scale,rot90=True) 
    # Parents the list af all objects to an empty    
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
    #texture names required 
    channels = ['basecolor', 'normal','specular','roughness','metallic','height']
    for mat_name, material in materials.items():
        generate_textures = False
        #if mat_dict.has_key('displacement'):
        if hasattr(material, 'displacement'):
            use_technical = True
            displacement = material.displacement
        else:
            use_technical=False
            displacement = None    
        # load parameters from preset 
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
            sbs.sbsar_render(sbs_path,texture_path,mat_name,channels,parameters,use_technical)
        imagedict = mu.make_imagedict(texture_path)
        mat_dict[mat_name] = mu.texture_full_material(mat_name,imagedict,mapping=mu.Mapping(coord='UV'),displacement=displacement)
    return mat_dict

def simple_door(mat_door,dpos,rot,dims):
    '''
    Make a simple panel door with no frame with material mat_door at position dpos
    and rotation rot of dimension dims
    '''
    # simple door with no frame
    dims[2] /= 2.0
    door = bm.wall('door',mat_door,pos=dpos,rot=rot,dims=dims)
    return door

def frame_door(mat_door,mat_frame,dpos,rot,dims,framedim):
    '''
    Make a panel door with material mat_door at position dpos and rotation rot
    of dimensions dim along with a frame of material mat_frame and dims framedim
    '''
    # simple door with frame
    fpos = [dpos[0],dpos[1],dpos[2]+dims[1]/2]
    frame = bm.frame('frame',mat_frame,pos=fpos,rot=rot,dims_hole=dims,dims_frame=framedim)
    dims[0] -= 2*framedim[1]
    dims[1] -= 2*framedim[1]
    dpos[2] += framedim[1]
    dims[2] /= 2.0
    door = bm.wall('door',mat_door,pos=dpos,rot=rot,dims=dims)
    return door, frame

def wall_tiles(name,dims,tile_size,pos,rot,hole=None,mats=None):
    '''
    Function to apply panels to the walls
    '''
    # cover walls with tiles using array. cut the tiles at the end of the wall
    print(dims)
    print(hole)
    (dx,dy) = tile_size
    (Lx,Ly) = dims
    if hole is not None:
        (x,y,w,h,dpos) = hole
        tile1 = bm.tile_fill(name+'1',dx,dy,x,Ly)
        tile1.location=pos
        tile1.rotation_euler=rot
        tile2 = bm.tile_fill(name+'2',dx,dy,w,Ly-h+y)
        tile2.location=[dpos[0],dpos[1],h]
        tile2.rotation_euler=rot
        tile3 = bm.tile_fill(name+'3',dx,dy,Lx-x-w,Ly)
        tile3.location=[dpos[2],dpos[3],pos[2]]
        tile3.rotation_euler=rot
        if mats is not None:
            tile1.data.materials.append(mats)
            tile2.data.materials.append(mats)
            tile3.data.materials.append(mats)
        return [tile1,tile2,tile3]    
    else:    
        tile = bm.tile_fill(name,dx,dy,Lx,Ly)
        if mats is not None:
            tile.data.materials.append(mats)
        tile.location=pos
        tile.rotation_euler=rot
        return [tile]
    
def ceiling_lighting(room, ceiling):
    #    '''
    #    Function to create an array of LED tubes or SPOTS for ceiling lighting
    #    receive room class and ceiling
    #    lighting = room.lighting
    #    lighting.array: x , y
    #    lighting.... definiria a que lighting source tengo que incluir
    #    
    #    lightSource clase general con   
    #    mount > dimensions . material
    #    color
    #    intensity
    #    
    #    Tube
    #    dimensions ( para el spot no es relevante)
    #    materials list para el caso de tubv
    #    material led es un material solo con shder de emision
    #    de aca se puede derivar spot tube, etc
        
    # Nx , Ny son la cantidad de elementos del array
    # calcular el espaciamiento y la ubicacion del primero objeto mount (x0,y0,z0)
    # para tener una iluminacion uniforme
    # chequear si las dimensiones de mount entran en ese espaciamiento
        
            
    # Primero la parte geometrica depende del objeto
    # x es depth, y es width
    # ceiling esta centrado en 0,0,h, pero igual por las dudas tomamos las coordenadas
    # ojo puede depender de la orientacion
    mount_size = [0.1, 1.5, 0.1]
    lighting_array_x = 5
    lighting_array_y = 2
    (Sx,Sy,Sz) = mount_size
    (Nx,Ny) = [lighting_array_x, lighting_array_y] 
    factor = 0.3
    overlay = 0.01
    dx = (room.depth+(2*factor-1)*Sx)/(Nx+2*factor-1)
    dy = (room.width+(2*factor-1)*Sy)/(Ny+2*factor-1)
    dx0 = factor*dx+(0.5-factor)*Sx
    dy0 = factor*dy+(0.5-factor)*Sy
    x0 = ceiling.location.x - room.depth/2 + dx0
    y0 = ceiling.location.y - room.width/2 + dy0
    z0 = ceiling.location.z - overlay
    # chequear que sea consistente
    # dx>Sx
    # dy>Sy
    
    #crear el objeto mount 
    # si es type tubo es box
    # si es type spot es cilindro
    # con las dimensiones de mount.size
    mount_type = 'tube'
    if mount_type is 'tube':
        # crea el plafon para el tubo como un cubo en base a las dimensiones que estan
        # en lighting.mount.size
        mount = bm.box('mount',dims=[Sx,Sy,Sz], pos=[x0,y0,z0],bottom=False)
    elif mount_type is 'spot':
        mount = bm.tube('mount',dims=[Sx,Sy,Sz], pos=[x0,y0,z0],bottom=False)
    else:
        pass    
    # llaman a una funcion de blender methods
    # spacing puede estar fijo en 0.002 m
    # bm.embed_array(ceiling,nx,ny,dx,dy,x0,y0,z0,mount,spacing)
    bm.embed_array(ceiling,Nx,Ny,dx,dy,mount)
    s1 = mount.modifiers.new('S1','SOLIDIFY')
    
    # ahora creamos las luces en si
    # if type es tube
    # crear un objeto un tube con dimensiones
    # element.diameter
    # element.length
    # invocar una funcion ad-hoc de blender methods que haga un tubo con caps y 
    # dos materiales
    # material1 emisor
    # material2 gris metal con roughness
    # crear material led
    # crear material metal1
    tube_strength = 100
    tube_color = [1,0.8,0.8,1]

    led1 = mu.emission_material('Led1',tube_strength,tube_color)
    metal1 = mu.simple_material('Metal',[0.8, 0.8, 0.8,1], specular=0.9,roughness=0.3,metallic=1.0)
    r_list = [0.02,0.02,0.03,0.03,0.02,0.02]
    l_list = [0.05,0,1.3,0,0.05] # tubo de 1.4 m
    zoffset = 0.7
    tube = bm.tube('tube', mats = [led1,metal1], r=r_list, l=l_list, zoffset=zoffset, pos=[x0,y0,z0+Sz/2], rot=[0,pi/2,pi/2])
    bm.paint_regions(tube,2,[[-1,-0.6,1],[0.6,1,1]])

    # array de nx ny spacing dx dy y posicion original de tubo (x0,y0,z0)
    # aplicar la intensidad y el color al material de emision
    at1 = bm.arraymod(tube,name='AT1',count=Ny,off_constant=[0,dy,0])
    at2 = bm.arraymod(tube,name='AT2',count=Nx,off_constant=[dx,0,0])
    # if type spot
    # crear una funcion en blender methods que haga un array de point lights
    # array de nx ny spacing dx dy y posicion original de point light (x0,y0,z0)
    # spot_list = bm.point_light_array(nx,ny,dx,dy,x0,y0,z0)
    # aplicar ies texture a todos los point lights
    
    # devuelve una lista de objetos para linkear
    return [tube,mount]
    #bm.light_array(ob,Nx,Ny,dx,dy):
    #spot_list.append(mount)
   
    

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
