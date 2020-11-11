from pysbs import context
from pysbs import batchtools
from pathlib import Path
import math



def map_render(sbsar_file,output,output_path,resol):
    batchtools.sbsrender_render(
                                sbsar_file,
                                output_path=output_path,
                                input_graph_output=output,
                                set_value=["$outputsize@{rx},{ry}".format(rx=resol[0],ry=resol[1])]).wait()


def sbsar_render(mats_path,sbsar_name,sbsar_type,resolution=[4096,4096],pars=None):
    px = int(math.log(int(resolution[0]), 2))
    py = int(math.log(int(resolution[1]), 2))
    sbsar_path = mats_path / sbsar_type
    output_path = str(sbsar_path / sbsar_name)
    sbsar_file = str(sbsar_path / sbsar_name) + '.sbsar'
    # default
    maps = ['basecolor', 'normal','specular','roughness','metallic','height']
    for m in maps:
        map_render(sbsar_file,m,output_path,[px,py])
        

#sbsar_render(mats_path,sbsar_name,sbsar_type,resolution=RESOLUTION)        