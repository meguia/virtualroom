from pysbs import context
from pysbs import batchtools
from pathlib import Path
import math

aContext = context.Context()

def map_render(sbsar_file,output,sbs_name,out_path,values):
    batchtools.sbsrender_render(
        sbsar_file,
        output_path=out_path,
        output_name='_'.join([sbs_name,output]),
        input_graph_output=output,
        no_report=True,
        set_value=values
    ).wait()


def sbsar_render(sbs_path,sbs_name,maps,resolution=[1024,1024],pars=None):
    px = int(math.log(int(resolution[0]), 2))
    py = int(math.log(int(resolution[1]), 2))
    out_path = str(sbs_path)
    sbsar_file = out_path + '.sbsar'
    param_dict = {}
    values = sbsar_getparam(param_dict,resolution=[px,py]) 
    print(values)
    # default
    for m in maps:
        map_render(sbsar_file,m,sbs_name,out_path,values)
        

def sbsar_getparam(param_dict,resolution=[10,10]):
    values = []
    values.append("$outputsize@" + str(resolution[0]) + "," +  str(resolution[1]))
    for key,value in param_dict.items():
        values.append( "" + key + "@" + value)
    return values   