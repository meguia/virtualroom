import bpy
import sys
from pathlib import Path
from math import radians,sin,cos,pi
homedir = Path.home() 
thisdir = homedir / 'virtualroom' 
savedir = homedir / 'Renders'
utildir = homedir / 'blender_utils'
libdir = thisdir / 'lib'

sys.path.append(str(utildir))   
import blender_methods as bm
import clear_utils as cu

cu.clear()

col_obj = bm.iscol('Mesh')
bm.link_col(col_obj)

filepath = homedir / 'virtualroom' / 'lib' / 'Sources.blend'

with bpy.data.libraries.load(str(filepath)) as (data_from, data_to):
    try:
        data_to.objects = [name for name in data_from.objects]
    except UnicodeDecodeError as exc:
        print(exc)   

# esto es del json
stand_name='Floor_Stand'
speaker_name='Genelec'
room_speaker_height = 1.40
#speaker_array = [[1,0,180], [-1,0,0],[0,1,-90], [0,-1,90]]
r = 3
N = 12
speaker_array = [[r*cos(2*pi*a/N), r*sin(2*pi*a/N), 2*pi*a/N-pi] for a in range(N)]
        

# va en virtualroom       
print('Imported ', str(list(data_to.objects)))
pie_data = bpy.data.objects[stand_name].data
speaker_data = bpy.data.objects[speaker_name].data
if stand_name is 'Plate_Stand':
    speaker_height = bpy.data.objects[stand_name].location[2]
elif stand_name is 'Floor_Stand':
    pie2_data = bpy.data.objects[stand_name+'2'].data    
    speaker_height = room_speaker_height 

# en room utils 
# make_speaker_array(room,speaker_data,[pie_data,pie_data2],speaker_height)
# devuelve object_list

object_list = []
for idx, p in enumerate(speaker_array):
    print(speaker_array)
    stand_name_ob = stand_name + '_' + str(idx)
    #pie = bpy.data.objects.new(stand_name_ob, pie_data)
    pie = bm.object_from_data(stand_name_ob, pie_data)
    pie.location = [p[0], p[1], speaker_height]
    pie.rotation_euler = [0,0,p[2]]
    object_list.append(pie)
    if stand_name is 'Floor_Stand':
        stand_name_ob = stand_name + '_' + str(idx) + '_2'
        #pie2 = bpy.data.objects.new(stand_name_ob, pie2_data)
        pie2 = bm.object_from_data(stand_name_ob, pie2_data)
        pie2.location = [p[0], p[1], 0]
        pie2.rotation_euler = [0,0,p[2]]
        object_list.append(pie2)    
    speaker_name_ob = speaker_name + '_' + str(idx)
    #speaker = bpy.data.objects.new(speaker_name_ob, speaker_data)
    speaker = bm.object_from_data(speaker_name_ob, speaker_data)
    speaker.location = [p[0], p[1], speaker_height]
    speaker.rotation_euler = [0,0,p[2]]
    object_list.append(speaker)
bm.list_link(object_list, col_obj)        