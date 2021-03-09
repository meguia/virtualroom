
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

# BORRA LO ANTERIOR 
cu.clear()
cu.clear_act()
cylinder = bm.cylinder('Tube', r=0.05, h=1.5, rot=[0.0, radians(90.0), 0.0], pos = [-0.75,0,0])

bpy.context.scene.collection.objects.link( bpy.data.objects['Tube'] )

instance =  bpy.context.scene.objects.get('Tube')
old_type = bpy.context.area.type
bpy.context.area.type = 'VIEW_3D'
bpy.context.view_layer.objects.active = instance
bpy.context.object.data.use_mirror_y = True
instance.select_set(True)
bpy.ops.object.editmode_toggle()
def view3d_find( return_area = False ):
    # returns first 3d view, normally we get from context
    for area in bpy.context.window.screen.areas:
        if area.type == 'VIEW_3D':
            v3d = area.spaces[0]
            rv3d = v3d.region_3d
            for region in area.regions:
                if region.type == 'WINDOW':
                    if return_area: return region, rv3d, v3d, area
                    return region, rv3d, v3d
    return None, None

region, rv3d, v3d, area = view3d_find(True)

override = {
    'scene'  : bpy.context.scene,
    'region' : region,
    'area'   : area,
    'space'  : v3d
}

_MESH_OT_loopcut = {
    "number_cuts"           : 1,
    "smoothness"            : 0,     
    "falloff"               : 'INVERSE_SQUARE',  # Was 'INVERSE_SQUARE' that does not exist
    "edge_index"            : 1,
    "mesh_select_mode_init" : (True, False, False),
    "object_index" : 0
}

_TRANSFORM_OT_edge_slide = {
    "value"           : 0.0,
    "mirror"          : False, 
    "snap"            : False,
    "snap_target"     : 'CLOSEST',
    "snap_point"      : (0, 0, 0),
    "snap_align"      : False,
    "snap_normal"     : (0, 0, 0),
    "correct_uv"      : False,
    "release_confirm" : False,
    "use_accurate"    : False
}

# First loopcut cylinder right end

_TRANSFORM_OT_edge_slide['value'] = -0.90
bpy.ops.mesh.loopcut_slide(override, MESH_OT_loopcut = _MESH_OT_loopcut, TRANSFORM_OT_edge_slide = _TRANSFORM_OT_edge_slide)

# Second loopcut close to right tube end

_TRANSFORM_OT_edge_slide['value'] = 0.95
bpy.ops.mesh.loopcut_slide(override, MESH_OT_loopcut = _MESH_OT_loopcut, TRANSFORM_OT_edge_slide = _TRANSFORM_OT_edge_slide)

# Third loopcut cylinder left end

_MESH_OT_loopcut['edge_index'] = 48
_TRANSFORM_OT_edge_slide['value'] = 0.90
bpy.ops.mesh.loopcut_slide(override, MESH_OT_loopcut = _MESH_OT_loopcut, TRANSFORM_OT_edge_slide = _TRANSFORM_OT_edge_slide)

# Fourth loopcut close to cylinder left end

_MESH_OT_loopcut['edge_index'] = 120 
_TRANSFORM_OT_edge_slide['value'] = -0.95
bpy.ops.mesh.loopcut_slide(override, MESH_OT_loopcut = _MESH_OT_loopcut, TRANSFORM_OT_edge_slide = _TRANSFORM_OT_edge_slide)

bpy.ops.object.editmode_toggle()
bpy.context.area.type = old_type