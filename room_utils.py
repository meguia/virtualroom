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
import numpy_mesh as nm
import material_utils as mu
import uv_utils as uv
import sbsar_utils as sbs
import bmesh_utils as bu
from math import radians, pow, pi, atan2, tan, sin, sqrt
import importlib as imp
imp.reload(bm)
imp.reload(nm)
imp.reload(mu)
imp.reload(uv)
imp.reload(bu)
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
            wall,base= bm.wall('wall_' + str(n),mat_dict[room.wall.material.name] ,pos=pos[n],rot=rots[n],dims=[dim[n],h+t,t],hole=hole[n],
                        basemat= mat_dict[room.base.material.name],basedim=[room.base.height, room.base.thickness])            
            if with_uv:
                if n==dn:
                    uv.uv_board_with_hole(base.data,basedim,hole[dn],scale=room.wall.uv_scale,internal=False)
                else:
                    uv.uv_board(base.data,basedim,scale=room.base.uv_scale)    
            room_list.append(base)   
            if with_tiles:
                pos2[n].append(basedim[1]-t)
                print(n)
                tiles =  wall_tiles('tiles_' +str(n),[dim2[n],h-basedim[1]+t],[1,1],pos=pos2[n],rot=[radians(90),0,rots[n]],hole=hole[n],mats=None)
                room_list.extend(tiles)       
        else:
            wall = bm.wall('wall_' + str(n),mat_dict[room.wall.material.name] ,pos=pos[n],rot=rots[n],dims=[dim[n],h+t,t],hole=hole[n])
        if with_uv:
            if n==dn:
                uv.uv_board_with_hole(wall.data,[dim[n],h+t,t],hole[dn],scale=room.wall.uv_scale)
            else:
                uv.uv_board(wall.data,[dim[n],h+t,t],scale=room.wall.uv_scale)
        # agregar condicion para dividir la pared y que lea a que altura
        bu.face_split(wall.data,4,edge_indices=[1,3],fac=0.9)        
        room_list.append(wall)    
    # Makes door and frame 
    if room.door.frame is not None: 
        framedim = [room.door.frame.width, room.door.frame.thickness]   
        door,fr = frame_door(mat_dict[room.door.material.name],mat_dict[room.door.frame.material.name],dpos[dn],rots[dn],[dw,dh,t],framedim)
        if with_uv:
            uv.uv_planks(fr.data, scale = room.door.frame.uv_scale)
        room_list.extend([door,fr])
    else:
        door = simple_door(mat_dict[room.door.material.name],dpos[dn],rots[dn],[dw,dh,t])   
        # este no deberia ser room_list?
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
    
def ceiling_lighting(room, ceiling, asset_data=None):
    '''
    Function to create an array of LED tubes or SPOTS for ceiling lighting
    receive room class and object ceiling
    lighting = room.lighting
    lighting.array: x , y
    lighting.... definiria a que lighting source tengo que incluir
    
    lightSource clase general con   
    mount > dimensions . material
    color
    intensity
    '''
       
    mount_size = room.lighting.light_source.mount.as_xyz_array()
    (Sx,Sy,Sz) = mount_size
    #(Sx,Sy,Sz)= [0.1,0.1,0.13]
    (Nx,Ny) = [room.lighting.array_x, room.lighting.array_y] 
    factor = 0.3
    overlay = 0.0
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
    
    # CREAR EL material para MOUNT
    
    # con las dimensiones de mount.size
    mount_type = room.lighting.light_source.object #'tube'
    if mount_type == 'tube':
        # crea el plafon para el tubo como un cubo en base a las dimensiones que estan
        # en lighting.mount.size
        mount = bm.box('mount',dims=[Sx,Sy,Sz], pos=[x0,y0,z0],bottom=False)
        bm.embed_array(ceiling,Nx,Ny,dx,dy,mount)
        s1 = mount.modifiers.new('S1','SOLIDIFY')
    elif mount_type == 'spot':
        mount = bm.tube('mount', r=Sx, l=Sz, pos=[x0,y0,z0], bot=False)
        bm.embed_array(ceiling,Nx,Ny,dx,dy,mount)
        s1 = mount.modifiers.new('S1','SOLIDIFY')
    elif mount_type == 'asset':
        pass
    else:
        pass
    
    if mount_type == 'tube':
        # Crea TUBO
        tube_strength = room.lighting.light_source.intensity
        tube_color = room.lighting.light_source.color_as_rgba_array()
        # crea material
        led1 = mu.emission_material('Led1',tube_strength,tube_color)
        metal1 = mu.simple_material('Metal',[0.8, 0.8, 0.8,1], specular=0.9,roughness=0.3,metallic=1.0)
        # dimensiones del tubo
        tube_gap = 0.03
        tube_radius = 0.03
        cap_length = 0.05
        tube_length = (Sy-2.0*tube_gap-2.0*cap_length)
        cap_radius = 0.02
        r_list = [cap_radius,cap_radius,tube_radius,tube_radius,cap_radius,cap_radius]
        l_list = [cap_length,0,tube_length,0,cap_length] # tubo de 1.4 m
        zoffset = (tube_length+cap_length+tube_gap)/2.0
        light_source = bm.tube('tube', mats = [led1,metal1], r=r_list, l=l_list, zoffset=zoffset, axis=1)
        bm.paint_regions(light_source,1,[[-tube_length/2,-tube_length/2+cap_length,1],[tube_length/2-cap_length,tube_length/2,1]])
        at1 = bm.arraymod(light_source,name='AT1',count=Ny,off_constant=[0,dy,0])
        at2 = bm.arraymod(light_source,name='AT2',count=Nx,off_constant=[dx,0,0])
    elif mount_type == 'spot':
        # Crea SPOT
        spot_strength = room.lighting.light_source.intensity
        spot_color = room.lighting.light_source.color_as_rgb_array()
        # creamos el spot aplicando IES
        #spot = bm.new_spot(name='spot',size=radians(90),blend=0.9,color=spot_color,energy=spot_strength,spot_size=0.1)
        ies_path = str(thisdir / room.lighting.light_source.iesfile)
        spot = bm.new_ieslight(ies_path,color=spot_color,power=spot_strength)
        # creamos copias del spot en un array
        light_source = bm.light_grid(spot,Nx-1,Ny-1,dx,dy)
        light_source.show_instancer_for_viewport = False
        light_source.show_instancer_for_render = False
    elif mount_type == 'asset':
        #stand_name_ob = room.source.stand_name+ '_' + str(idx)
        try:
            if(asset_data == None):
                raise ValueError('asset_data should contain blender object data')
            for asset in asset_data:
                if asset.name == 'Lamp':
                    mount = bm.object_from_data('Lamp', asset.data)
            mount.location = [x0, y0, z0]
            at1 = bm.arraymod(mount,name='AT1',count=Ny,off_constant=[0,dy,0])
            at2 = bm.arraymod(mount,name='AT2',count=Nx,off_constant=[dx,0,0])

            spot_strength = room.lighting.light_source.intensity
            spot_color = room.lighting.light_source.color_as_rgb_array()

            # creamos el spot aplicando IES
            ies_path = str(thisdir / room.lighting.light_source.iesfile)
            spot = bm.new_ieslight(ies_path,color=spot_color,power=spot_strength)
            # offest hardcodeado para que no quede en z igual a techo
            spot.location.z -= 0.40
            light_source = bm.light_grid(spot,Nx-1,Ny-1,dx,dy)
            light_source.show_instancer_for_viewport = False
            light_source.show_instancer_for_render = False

        except Exception as error:
            print('Error'+repr(error))
    else:
        pass
    # if type spot
    # crear una funcion en blender methods que haga un array de point lights
    # array de nx ny spacing dx dy y posicion original de point light (x0,y0,z0)
    # spot_list = bm.point_light_array(nx,ny,dx,dy,x0,y0,z0)
    # aplicar ies texture a todos los point lights
    #bm.light_array(ob,Nx,Ny,dx,dy)
    #general
    light_source.parent = mount
    
    return light_source,mount


def ceiling_lighting_by_positions(room, ceiling, asset_data=None):
    '''
    Function to add lighting assets on roof by position
    TODO: add spot and tube by position
    '''
    mount_type = room.lighting.light_source.object #'tube'
    mount = []
    light_source = []
    if mount_type == 'asset':
        try:
            if(asset_data == None):
                raise ValueError('asset_data should contain blender object data')
            for asset in asset_data:
                if asset.name == 'Lamp':
                    mount_asset_data = asset.data
            z = ceiling.location.z
            ies_path = str(thisdir / room.lighting.light_source.iesfile)
            for idx, pos in enumerate(room.lighting.positions):
                lamp_name = 'Lamp_' + str(idx)
                lamp_copy = mount_asset_data.copy()
                lamp_object = bm.object_from_data(lamp_name, lamp_copy)
                lamp_object.location = [pos['x'], pos['y'], z]
                spot_strength = room.lighting.light_source.intensity
                spot_color = room.lighting.light_source.color_as_rgb_array()
                spot = bm.new_ieslight(ies_path,color=spot_color,power=spot_strength)
                ## offest hardcodeado para que no quede en z igual a techo
                spot.location = lamp_object.location
                spot.location.z -= 0.80
                mount.append(lamp_object)
                light_source.append(spot)

        except Exception as error:
            print('Error'+repr(error))
    #light_source.parent = mount
    return light_source,mount


# en room utils 
# make_speaker_array(room,speaker_data,[pie_data,pie_data2],speaker_height)
# devuelve object_list

def make_speaker_array(room, speaker_data, stand_data_array, speaker_height, point_camera):
    '''
    A function to create blender objects such as a speaker and a stand
    Returns a list of blender objects

    Parameters
    ----------
        room (Room): An object containing room data
        speaker_data (blender object data): blender object data representing a speaker
        stand_data_array (array): an array of blender objects data representing a speaker stand 
        point_camera (bool): True for Tilt_Stand only, points the speaker to the camera position
    '''
    object_list = []
    for idx, p in enumerate(room.source.positions):
        stand_name_ob = room.source.stand_name+ '_' + str(idx)
        stand_data_copy = stand_data_array[0].copy()
        stand = bm.object_from_data(stand_name_ob, stand_data_copy)
        stand.location = [p.x, p.y, speaker_height]
        object_list.append(stand)
        if len(stand_data_array) > 1:
            stand_name_ob = room.source.stand_name + '_' + str(idx) + '_B'
            stand2_data_copy = stand_data_array[1].copy()
            stand2 = bm.object_from_data(stand_name_ob, stand2_data_copy)
            stand2.parent = stand
            object_list.append(stand2)    
        if point_camera:
            cpos = [room.camera.x,room.camera.y,room.camera.z]
            pitch,yaw = get_tilt_angles(stand.location,cpos)
            tilt_base(stand,[0,pitch,yaw])
        else:
            stand.rotation_euler = [0,0,radians(p.rotation)]
        speaker_name_ob = room.source.speaker_name+ '_' + str(idx)
        speaker_data_copy = speaker_data.copy()
        speaker = bm.object_from_data(speaker_name_ob, speaker_data_copy)
        speaker.parent = stand
        object_list.append(speaker)
    return object_list


def get_tilt_angles(pos_ob, pos_target):
    '''
    Computes the tilt angles in Y and Z for (pitch and yaw) needed for object in 
    pos_ob to point in direction of pos_target
    '''
    yaw = atan2(pos_ob[1]-pos_target[1],pos_ob[0]-pos_target[0])
    dist = sqrt((pos_ob[1]-pos_target[1])**2+(pos_ob[0]-pos_target[0])**2)
    pitch = atan2(pos_target[2]-pos_ob[2],dist)
    return pitch,yaw
    

def tilt_base(base, rotation):
    '''
    Tilt Base with threaded rods with angle in degrees. 
    Geometrical data are obtained from the mesh assuming that min z coordinate
    of the mesh is on the floor and the max x xoordinate is the pivoting point
    '''
    h = abs(min([v.co.z for v in base.data.vertices]))
    D = abs(max([v.co.x for v in base.data.vertices]))
    var = base.children[0]
    d = abs(max([v.co.x for v in var.data.vertices]))
    alpha = rotation[1]
    z = h + (D-h*tan(alpha))*sin(alpha)
    l = (D+d)*tan(alpha)
    base.rotation_euler = rotation
    base.location.z = z
    var.location.z = -l


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
    if os.name == 'posix':
        file = str(pathimg).replace(" ", "\\ ")
        cmd = 'exiftool' + ' ' + ' '.join(pars) + ' '  + file
    else:    
        cmd = str(direxe) + '\exiftool' + ' ' + ' '.join(pars) + ' '  + str(pathimg)
    print(cmd)
    os.system(cmd)


def make_room2(room, mat_dict=None, with_uv=True, with_tiles=False, asset_data=None):
    '''
    Makes room as objects parented to an empty
    the objects are defined in the class Room
    mat_dict contains a dictionary of substance materiales
    also asigns uv maps (and lightmaps) to objects with scale
    '''
    (l,w,h,t) = [room.depth, room.width, room.height, room.wall_thickness] # length, width, height, thickness
    #(dp, dw, dh) = [room.door.position, room.door.width, room.door.height] # wall number, position from border, width, height
    # Makes floor and ceiling
    floor = bm.floor(type(room.floor).__name__, mat_dict[room.floor.material.name],pos=[0,0,-t],dims=[l+2*t,w+2*t,t])
    ceil = bm.floor(type(room.ceiling).__name__,mat_dict[room.ceiling.material.name],pos=[0,0,h],dims=[l+2*t,w+2*t,t])
    if with_uv:
        # esto esta bien?
        uv.uv_board(ceil.data, [l,w,t], front=1, scale = room.ceiling.uv_scale)
        uv.uv_board(floor.data, [l+2*t,w+2*t,t], front=2, scale = room.floor.uv_scale)
    room_list = [floor,ceil]    
    # Makes walls with bases in a loop
    # first define rotation, position, door position, main dimension (dim)
    rots = [radians(180),0,radians(90),radians(-90)]
    pos=[[0,-w/2-t/2,0],[0,w/2+t/2,0],[-l/2-t/2,0,0],[l/2+t/2,0,0]]
    #dpos = [[l/2-dp-dw/2,-w/2-t/2,0],[-l/2+dp+dw/2,w/2+t/2,0],[-l/2-t/2,-w/2+dp+dw/2,0],[l/2+t/2,w/2-dp-dw/2,0]]
    dim=[l+2*t,l+2*t,w,w]
    tdim = 0.005
    #para tiles (no se usa por ahora)
    pos2=[[l/2,-w/2+tdim],[-l/2,w/2-tdim],[-l/2+tdim,-w/2],[l/2-tdim,w/2]]
    #dpos2 = [[l/2-dp,-w/2+tdim,l/2-dp-dw,-w/2+tdim],[-l/2+dp,w/2-tdim,-l/2+dp+dw,w/2-tdim],
    #        [-l/2+tdim,-w/2+dp,-l/2+tdim,-w/2+dp+dw],[l/2-tdim,w/2-dp,l/2-tdim,w/2-dp-dw]]
    dim2=[l,l,w,w]
    holes = room.wall.holes_as_array()
    door_count = 0
    
    for n in range(4):
        bandmats = [mat_dict[room.wall.material.name]]
        bands = []
        bands_by_wall_index = room.wall.fetch_bands_by_wall_index(n)
        for band in bands_by_wall_index:
            bands.append([band.heights, band.thickness])
            bandmats.append(mat_dict[band.material.name])

        wall = nm.wall('wall_' + str(n),pos=pos[n],rot=rots[n],dims=[dim[n],h,t/2],holes=holes[n],bandmats=bandmats,bands=bands)
        if with_uv:
            #pendiente
            uv.uv_board_hbands(wall.data, scale=1)
        room_list.append(wall)    

        doors = room.wall.fetch_doors_by_wall_index(n)
        print('doors by index')
        print(doors)
        #import pdb; pdb.set_trace()
        for door in doors:
            # Makes door and frame 
            #recalculo
            (dp, dw, dh) = [door.position, door.width, door.height] # position from border, width, height
            dpos = [
                    [l/2-dp-dw/2+t,-w/2-t/2,0],
                    [-l/2+dp+dw/2-t,w/2+t/2,0],
                    [-l/2-t/2,-w/2+dp+dw/2,0],
                    [l/2+t/2,w/2-dp-dw/2,0]
                   ]
            if door.frame is not None: 
                framedim = [room.door.frame.width, room.door.frame.thickness]   
                door_obj,fr = frame_door(
                                    mat_dict[door.material.name],
                                    mat_dict[door.frame.material.name],
                                    dpos[n],
                                    rots[n],
                                    [door.width,door.height,t],
                                    framedim
                                    )
                if with_uv:
                    uv.uv_planks(fr.data, scale = door.frame.uv_scale)
                room_list.extend([door_obj,fr])
            else:
                if hasattr(door, 'material'):
                    if door.material is not None:
                        door_obj = simple_door(
                                              mat_dict[door.material.name],
                                              dpos[n],
                                              rots[n],
                                              [door.width,door.height,t]
                                              )   
                        # este no deberia ser room_list?
                        room_list.append(door_obj)
                    if with_uv:    
                        uv.uv_board(
                                    door_obj.data,
                                    [door.width,door.height,t],
                                    scale=door.uv_scale,
                                    rot90=True
                                    ) 
                elif hasattr(door, 'assets'):
                    if len(door.assets) > 0:
                        # for all imported assets
                        for asset in asset_data:
                            # for assets in door 
                            for door_asset in door.assets:
                                # if name of asset of door equals name of imported
                                if door_asset.name == asset.name:
                                    door_count += 1
                                    # create
                                    door_name = 'Door-'+str(door_count)+'-Wall-'+str(n)
                                    asset_data_copy = asset.data.copy()
                                    door_obj = bm.object_from_data(door_name,
                                            asset_data_copy)
                                    # door context
                                    if n == 0:
                                        door_obj.location = dpos[n]
                                        door_obj.rotation_euler = [0.0,0.0,radians(180)]
                                        #l/2-dp-dw/2+t
                                    if n == 1:
                                        door_obj.location = dpos[n]
                                        door_obj.rotation_euler = [0.0,0.0,radians(90)]
                                    if n == 2:
                                        door_obj.location = dpos[n]
                                        door_obj.rotation_euler = [0.0,0.0,0.0]
                                    if n == 3:
                                        door_obj.location = dpos[n]
                                        door_obj.rotation_euler = [0.0,0.0,radians(-90)]
                                    #door_obj.rotation_euler =
                                    room_list.append(door_obj)

    room_ = bm.list_parent('room',room_list)
    return room_

def create_misc_objects(room,asset_data):
    '''
    Returns a list of blender object
    Parameters
    ----------
        room (Room): An object containing room data
        asset data (blender object data array): blender object data
        representing a miscelanneous objects 
    '''
    misc_obj_list = []
    misc_obj_idx = 0
    try:
        if(asset_data == None):
            raise ValueError('asset_data should contain blender object data')
        for blender_obj in room.misc_assets_arrangement.blender_objects:
            for asset in asset_data:
                if blender_obj.asset.name == asset.name:
                    misc_obj_name = asset.name + str(misc_obj_idx)
                    misc_obj_idx += 1
                    asset_data_copy = asset.data.copy()
                    misc_obj = bm.object_from_data(misc_obj_name,
                            asset_data_copy)
                    misc_obj.location = blender_obj.location_as_array()
                    misc_obj.rotation_euler = blender_obj.rotation_as_array()
                    misc_obj.scale = blender_obj.scale_as_array()
                    misc_obj_list.append(misc_obj)

    except Exception as error:
        print('Error'+repr(error))
    return misc_obj_list

def make_cable_tray(room, asset_data):
    '''
    Returns a list of blender object
    Parameters
    ----------
        room (Room): An object containing room data
        asset data (blender object data array): blender object data
        representing a cable tray and a cable tray connector
    '''
    cable_tray_object_list  = []
    try:
        if(asset_data == None):
            raise ValueError('asset_data should contain blender object data')
        # check Tray and TrayConnector exist in resource
        tray_connector_asset_data = None 
        tray_asset_data = None 
        for asset in asset_data:
            if asset.name == 'TrayConnector':
                tray_connector_asset_data = asset.data
            if asset.name == 'Tray':
                tray_asset_data = asset.data
        if(not tray_connector_asset_data and not tray_asset_data):
            raise ValueError('asset_data should contain blender objects with name Tray and TrayConnector')

        for idx in range(4):
            if idx == 0:
                config = room.cable_tray_arrangement.get_wall_config_by_wall_index(idx)
                if(not config['Tray'] and not config['Connector']):
                    # exit early if no tray or connector
                    continue
                location = [
                           room.depth/2 - room.cable_tray_arrangement.y_offset, 
                           -room.width/2 + room.cable_tray_arrangement.x_offset, 
                           room.height - room.cable_tray_arrangement.z_offset,
                           ]
                # Connector
                if(config['Connector']):
                    tray_connector_name = 'TrayConnector_' + str(idx)
                    tray_connector_asset_data_copy = tray_connector_asset_data.copy()
                    tray_connector_obj = bm.object_from_data(tray_connector_name,
                            tray_connector_asset_data_copy)
                    tray_connector_obj.location = location
                    tray_connector_obj.rotation_euler = [0,0,0]
                    cable_tray_object_list.append(tray_connector_obj)

                #Tray
                if(config['Tray']):
                    tray_name = 'Tray_' + str(idx)
                    tray_copy = tray_asset_data.copy()
                    tray_obj = bm.object_from_data(tray_name, tray_copy)
                    me = tray_obj.data
                    me.name = tray_name
                    # increment = room depth + 0.2 (tray width) + y offset * 2 + 0.2 (connector)-1(initial size)
                    increment = room.depth - room.cable_tray_arrangement.y_offset*2- 0.2 - 1
                    bm.linear_stretch(me, 1, 0.9, increment)
                    uv.stretch_uv(me, 'UVMap', 1, 0.9, increment)
                    # hardcoding tray offset todo make it object attribute
                    location[0] -= 0.10
                    tray_obj.location = location
                    tray_obj.rotation_euler = [0,0,radians(90)] 
                    cable_tray_object_list.append(tray_obj)

            if idx == 1:
                config = room.cable_tray_arrangement.get_wall_config_by_wall_index(idx)
                if(not config['Tray'] and not config['Connector']):
                    # exit early if no tray or connector
                    continue
                location = [
                           room.depth/2 - room.cable_tray_arrangement.y_offset, 
                           room.width/2 - room.cable_tray_arrangement.x_offset, 
                           room.height - room.cable_tray_arrangement.z_offset,
                           ]

                # Connector
                if(config['Connector']):
                    tray_connector_name = 'TrayConnector_' + str(idx)
                    tray_connector_asset_data_copy = tray_connector_asset_data.copy()
                    tray_connector_obj = bm.object_from_data(tray_connector_name,
                            tray_connector_asset_data_copy)
                    tray_connector_obj.location = location
                    tray_connector_obj.rotation_euler = [0,0,radians(90)]
                    cable_tray_object_list.append(tray_connector_obj)

                #Tray
                if(config['Tray']):
                    tray_name = 'Tray_' + str(idx)
                    tray_copy = tray_asset_data.copy()
                    tray_obj = bm.object_from_data(tray_name, tray_copy)
                    me = tray_obj.data
                    me.name = tray_name
                    # increment = room width+ x offset * 2 + 0.2 (connector)-1(initial size)
                    increment = room.width- room.cable_tray_arrangement.x_offset*2- 0.2 - 1
                    bm.linear_stretch(me, 1, 0.9, increment)
                    uv.stretch_uv(me, 'UVMap', 1, 0.9, increment)
                    # hardcoding tray offset todo make it object attribute
                    location[1] -= 0.10
                    tray_obj.location = location
                    tray_obj.rotation_euler = [0,0,radians(180)] 
                    cable_tray_object_list.append(tray_obj)
                
            if idx == 2:
                config = room.cable_tray_arrangement.get_wall_config_by_wall_index(idx)
                if(not config['Tray'] and not config['Connector']):
                    # exit early if no tray or connector
                    continue 
                location = [
                           -room.depth/2 + room.cable_tray_arrangement.y_offset, 
                           room.width/2 - room.cable_tray_arrangement.x_offset, 
                           room.height - room.cable_tray_arrangement.z_offset,
                           ]

                # Connector
                if(config['Connector']):
                    tray_connector_name = 'TrayConnector_' + str(idx)
                    tray_connector_asset_data_copy = tray_connector_asset_data.copy()
                    tray_connector_obj = bm.object_from_data(tray_connector_name,
                            tray_connector_asset_data_copy)
                    tray_connector_obj.location = location
                    tray_connector_obj.rotation_euler = [0,0,radians(180)]
                    cable_tray_object_list.append(tray_connector_obj)

                #Tray
                if(config['Tray']):
                    tray_name = 'Tray_' + str(idx)
                    tray_copy = tray_asset_data.copy()
                    tray_obj = bm.object_from_data(tray_name, tray_copy)
                    me = tray_obj.data
                    me.name = tray_name
                    # increment = room depth + 0.2 (tray width) + y offset * 2 + 0.2 (connector)-1(initial size)
                    increment = room.depth - room.cable_tray_arrangement.y_offset*2- 0.2 - 1
                    bm.linear_stretch(me, 1, 0.9, increment)
                    uv.stretch_uv(me, 'UVMap', 1, 0.9, increment)
                    # hardcoding tray offset todo make it object attribute
                    location[0] += 0.10
                    tray_obj.location = location
                    tray_obj.rotation_euler = [0,0,radians(-90)] 
                    cable_tray_object_list.append(tray_obj)

            if idx == 3:
                config = room.cable_tray_arrangement.get_wall_config_by_wall_index(idx)
                if(not config['Tray'] and not config['Connector']):
                    # exit early if no tray or connector
                    continue
                location = [
                           -room.depth/2 + room.cable_tray_arrangement.y_offset, 
                           -room.width/2 + room.cable_tray_arrangement.x_offset, 
                           room.height - room.cable_tray_arrangement.z_offset,
                           ]

                # Connector
                if(config['Connector']):
                    tray_connector_name = 'TrayConnector_' + str(idx)
                    tray_connector_asset_data_copy = tray_connector_asset_data.copy()
                    tray_connector_obj = bm.object_from_data(tray_connector_name,
                            tray_connector_asset_data_copy)
                    tray_connector_obj.location = location
                    tray_connector_obj.rotation_euler = [0,0,radians(-90)]
                    cable_tray_object_list.append(tray_connector_obj)

                #Tray
                if(config['Tray']):
                    tray_name = 'Tray_' + str(idx)
                    tray_copy = tray_asset_data.copy()
                    tray_obj = bm.object_from_data(tray_name, tray_copy)
                    me = tray_obj.data
                    me.name = tray_name
                    # increment = room width+ x offset * 2 + 0.2 (connector)-1(initial size)
                    increment = room.width- room.cable_tray_arrangement.x_offset*2- 0.2 - 1
                    bm.linear_stretch(me, 1, 0.9, increment)
                    uv.stretch_uv(me, 'UVMap', 1, 0.9, increment)
                    # hardcoding tray offset todo make it object attribute
                    location[1] += 0.10
                    tray_obj.location = location
                    tray_obj.rotation_euler = [0,0,0] 
                    cable_tray_object_list.append(tray_obj)

    except Exception as error:
        print('Error'+repr(error))
    return cable_tray_object_list


def add_curtains(room):
    # add curtains
    # dpos = [[l/2-dp-dw/2,-w/2-t/2,0],[-l/2+dp+dw/2,w/2+t/2,0],[-l/2-t/2,-w/2+dp+dw/2,0],[l/2+t/2,w/2-dp-dw/2,0]]
    room_list = []
    if room.curtain_arrangement is not None:
        for idx, curtain in enumerate(room.curtain_arrangement.curtains):
           xs = []
           ys = [] 
           zs = []
           if curtain.wall_index == 0: 
               # def mesh_for_recboard(name,xs,ys,zs):
               xs = [curtain.position-curtain.width/2,curtain.position+curtain.width/2]
               ys = [-room.width/2+curtain.offset,-room.width/2+curtain.offset]
               zs = [0,curtain.height]
           elif curtain.wall_index == 1:
               xs = [curtain.position+curtain.width/2,curtain.position-curtain.width/2]
               ys = [room.width/2-curtain.offset,room.width/2-curtain.offset]
               zs = [0,curtain.height]

           elif curtain.wall_index == 2: 
               xs = [-room.length/2+curtain.offset, -room.length/2+curtain.offset]
               ys = [curtain.position+curtain.width/2,curtain.position-curtain.width/2]
               zs = [0,curtain.height]

           elif curtain.wall_index == 3: 
               xs = [room.length/2-curtain.offset, room.length/2-curtain.offset]
               ys = [curtain.position-curtain.width/2,curtain.position+curtain.width/2]
               zs = [0,curtain.height]

           object_name = 'curtain' + str(idx)
           rec_mesh = bm.mesh_for_vertical_plane(object_name, xs, ys, zs)
           rec_ob =  bm.object_from_data(
                                        rec_mesh.name,
                                        rec_mesh
                                        )
           room_list.append(rec_ob)
    return room_list
