from pysbs import context
from pysbs import batchtools
from pathlib import Path
import math



def map_render(sbsar_file,output,sbs_name,output_path,resol):
    batchtools.sbsrender_render(
                                sbsar_file,
                                output_path=output_path,
                                output_name='_'.join([sbs_name,output]),
                                input_graph_output=output,
                                set_value=["$outputsize@{rx},{ry}".format(rx=resol[0],ry=resol[1])]).wait()


def sbsar_render(sbs_path,sbs_name,resolution=[1024,1024],pars=None):
    px = int(math.log(int(resolution[0]), 2))
    py = int(math.log(int(resolution[1]), 2))
    output_path = str(sbs_path)
    sbsar_file = output_path + '.sbsar'
    # default
    maps = ['basecolor', 'normal','specular','roughness','metallic','height']
    for m in maps:
        map_render(sbsar_file,m,sbs_name,output_path,[px,py])
        

   