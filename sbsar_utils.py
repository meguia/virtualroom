from pysbs import context, sbsarchive, batchtools
import json
import math

aContext = context.Context()

def map_render(sbsar_file,output,sbs_name,out_path,values):
    '''
    Renders texture in channel output 'out_path/sbs_name_output.png' from sbsar_file
    using parameters and options passed in values
    '''
    print('Rendering channel {} of texture {} with values {}'.format(output,sbs_name,values))
    batchtools.sbsrender_render(
        sbsar_file,
        output_path=out_path,
        output_name='_'.join([sbs_name,output]),
        input_graph_output=output,
        no_report=True,
        set_value=values
    ).wait()


def sbsar_render(sbs_path,sbs_name,channels,resolution=[512,512],set_pars=None):
    '''
    Renders all textures of sbsar file in sbs_path for channels given in list maps 
    with specified resolution and parameters passed in dictionary set_pars
    '''
    px = int(math.log(int(resolution[0]), 2))
    py = int(math.log(int(resolution[1]), 2))
    out_path = str(sbs_path)
    sbsar_file = out_path + '.sbsar'
    param_dict = sbsar_loadparam(str(sbsar_file))
    if set_pars is not None:
        for key,value in set_pars.items():
            if key in param_dict:
                param_dict[key]=value
    values = sbsar_getvalues(param_dict,resolution=[px,py]) 
    # default
    with open(str(sbs_path / 'parameters.json'),'w') as fp:
        json.dump(param_dict,fp)
    for chan in channels:
        map_render(sbsar_file,chan,sbs_name,out_path,values)
        

def sbsar_getvalues(param_dict,resolution=[10,10]):
    '''
    formats the array of parameters passed in values from the dictionary of parameters param_dict
    and the resolution
    '''
    values = []
    values.append("$outputsize@" + str(resolution[0]) + "," +  str(resolution[1]))
    for key,value in param_dict.items():
        values.append( "" + key + "@" + str(value))
    print(values)
    return values 

def sbsar_loadparam(sbs_path,graph_idx=0):
    '''
    creates the dictionary of parameters param_dict from the default values of sbsar file
    '''
    sbsarDoc = sbsarchive.SBSArchive(aContext,str(sbs_path))
    sbsarDoc.parseDoc()
    graphs = sbsarDoc.getSBSGraphList()
    inputs = graphs[graph_idx].getInputParameters()
    param_dict = {}
    for inp in inputs:
        if inp.getGroup() is None:
            par_id = inp.mIdentifier
            default = inp.getDefaultValue()
            param_dict[par_id] = default
    return param_dict        

    
def sbsar_getparam(sbs_path):
    '''
    Return dictionary with default parameters of sbsar file in sbs_path
    '''
    out_path = str(sbs_path)
    sbsar_file = out_path + '.sbsar'
    param_dict = sbsar_loadparam(str(sbsar_file))
    return param_dict


  