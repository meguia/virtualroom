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


def sbsar_render(sbsar_file,texture_path,name,channels,parameters=None):
    '''
    Renders all textures of sbsar file in sbs_path for channels given in list maps 
    with specified resolution and parameters passed in dictionary set_pars
    '''
    if parameters is None:
        parameters = sbsar_loadparam(str(sbsar_file))
    values = sbsar_getvalues(parameters) 
    # default
    with open(str(texture_path / 'parameters.json'),'w') as fp:
        json.dump(parameters,fp)
    for chan in channels:
        map_render(str(sbsar_file),chan,name,str(texture_path),values)
        

def sbsar_getvalues(param_dict):
    '''
    formats the array of parameters passed in values from the dictionary of parameters param_dict
    and the resolution
    '''
    values = []
    for key,value in param_dict.items():
        if type(value) is list:
            values.append( "" + key + "@" + ",".join(str(x) for x in value))
        else:    
            values.append( "" + key + "@" + str(value))
    return values 

def sbsar_loadparam(sbs_path,resolution=[10,10],graph_idx=0):
    '''
    creates the dictionary of parameters param_dict from the default values of sbsar file
    '''
    sbsarDoc = sbsarchive.SBSArchive(aContext,str(sbs_path))
    sbsarDoc.parseDoc()
    graphs = sbsarDoc.getSBSGraphList()
    inputs = graphs[graph_idx].getInputParameters()
    param_dict = {'$resolution':resolution}
    for inp in inputs:
        if inp.getGroup() is None:
            par_id = inp.mIdentifier
            default = inp.getDefaultValue()
            param_dict[par_id] = default
    return param_dict        



  