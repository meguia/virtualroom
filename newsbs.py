import requests
import http.server
import http.client
import bpy

scn = bpy.data.scenes["Scene"]
preferences =  bpy.context.preferences.addons["Substance3DInBlender"].preferences

FORMATS_DICT = {
    "tga": {"label": "Targa", "ext": ".tga", "bitdepth": ["8"]},
    "exr": {"label": "Open Exr", "ext": ".exr", "bitdepth": ["32"]},
    "bmp": {"label": "Bitmap", "ext": ".bmp", "bitdepth": ["8"]},
    "png": {"label": "PNG", "ext": ".png", "bitdepth": ["16"]},
    "jpg": {"label": "JPEG", "ext": ".jpg", "bitdepth": ["32"]},
    "hdr": {"label": "HDR", "ext": ".hdr", "bitdepth": ["32"]},
    "tiff": {"label": "Tiff", "ext": ".tiff", "bitdepth": ["16"]}
}

class SBSAR():
    def __init__(self, json_obj):
        self.id = json_obj["id"]
        self.name = json_obj["name"]
        self.filename = json_obj["filename"]
        self.filepath = json_obj["filepath"]
        self.graphs = []

        for _idx, _graph in enumerate(json_obj["graphs"]):
            _new_graph = SBS_Graph(_idx, _graph)
            self.graphs.append(_new_graph)

    def to_json(self):
        _obj = {
            "id": self.id,
            "name": self.name,
            "filename": self.filename,
            "filepath": self.filepath,
            "graphs": []
        }

        for _graph in self.graphs:
            _obj["graphs"].append(_graph.to_json())
        return _obj



SRE_HOST = "http://127.0.0.1"
SRE_PORT = 41646
SRE_VERSION = "v1"
SRE_URI = "{}:{}/{}".format(SRE_HOST, SRE_PORT, SRE_VERSION)
output_size = preferences.resolution.get()
normal_format =  preferences.normal_format
shader_outputs = getattr(scn,preferences.shader_presets[int(preferences.shader_preset_list)].outputs_class_name)
shader_outputs.shader_preset.outputs

unique_name = 'concrete_raw_gray'
filename = 'concrete_raw_gray.sbsar'
filepath =  preferences.path_library + filename

server_uri = "{}:{}".format(SRE_HOST, SRE_PORT)
data = {"path": filepath,"renderCallback": server_uri,"format": "tga"}
endpoint = "{}/sbsar".format(SRE_URI)

session = requests.Session()

respost = session.post(url=endpoint, json=data, timeout=10)
respost_json = respost.json()
id =  respost_json['id']


loaded_sbsar=scn.loaded_sbsars.add()
loaded_sbsar.initialize(id,unique_name,filename,filepath)

r = session.get(url ="{}/sbsar/{}/parameters".format(SRE_URI, id), timeout=10)
parms = r.json()['parameters']
r = session.get(url = "{}/sbsar/{}/outputs".format(SRE_URI, id), timeout=10)
outputs = r.json()['outputs']
r = session.get(url = "{}/sbsar/{}/graphsinfo".format(SRE_URI, id), timeout=10)
graphs= r.json()['graphsinfo']
r = session.get(url = "{}/sbsar/{}/presets".format(SRE_URI, id), timeout=10)
presets = r.json()['presets']
r = session.get(url = "{}/sbsar/{}/embeddedpresets".format(SRE_URI, id), timeout=10)
embedded_presets = r.json()['embeddedpresets']

sbsar_json = {"id": id,  "name": unique_name,"filename": filename,"filepath": filepath,"graphs": []}

for graph_idx, item in enumerate(graphs):
    default_preset = presets[str(graph_idx)]
    mat_name = "{}".format(unique_name).replace(" ", "_")
    class_name = "{}".format(id)
    graph = {"index": graph_idx,"id": item["id"],"name": item["label"],"mat_name": mat_name,
    "parms_class_name": "SUBSTANCE_SGP_{}".format(class_name),"outputs_class_name": "SUBSTANCE_SGO_{}".format(class_name),
    "parms": {},"parms_groups": {},"outputs": {},"presets": []}

    for parm in parms:
        if parm["graphID"] == graph["id"]:
            graph["parms"][parm["identifier"]] = {"id": parm["id"],"identifier": parm["identifier"], "label": parm["label"],
            "graphID": parm["graphID"],"graphIDX": graph_idx,"visibleIf": parm["visibleIf"],"type": parm["type"],
            "guiWidget": parm["guiWidget"],"guiGroup": parm["guiGroup"] if len(parm["guiGroup"]) > 0 else "General",
            "guiDescription": parm["guiDescription"],"userTag": parm["userTag"], "useCache": parm["useCache"],
            "showAsPin": parm["showAsPin"], "isHeavyDuty": parm["isHeavyDuty"], "guiVisibleIf": parm["guiVisibleIf"],
            "channelUse": parm["channelUse"] if "channelUse" in parm else None, 
            "defaultValue": parm["defaultValue"] if "defaultValue" in parm else "",
            "value": parm["value"] if "value" in parm else "",
            "maxValue": parm["maxValue"] if "maxValue" in parm else None,
            "minValue": parm["minValue"] if "minValue" in parm else None,
            "labelFalse": parm["labelFalse"] if "labelFalse" in parm else None,
            "labelTrue": parm["labelTrue"] if "labelTrue" in parm else None,
            "sliderClamp": parm["sliderClamp"] if "sliderClamp" in parm else None,
            "sliderStep": parm["sliderStep"] if "sliderStep" in parm else None,
            "enumValues": []}

     graph["parms"]["$outputsize"]["value"] = default_outputsize
     graph["parms"]["$outputsize"]["defaultValue"] = default_outputsize    

    for output in outputs:
        if output["graphID"] == graph["id"]:
            shader_id = None
            channel_use = output["defaultChannelUse"]
            if channel_use in shader_outputs.shader_preset.outputs:
               shader_id =  shader_outputs.shader_preset.outputs[channel_use].id
            key = channel_use
            graph["outputs"][key] = {"id": output["id"],"identifier": output["identifier"],"label": output["label"],
            "group": output["group"], "graphID": output["graphID"], "graphIDX": graph_idx, "format": output["format"],
            "enabled": output["enabled"], "defaultChannelUse": channel_use, "channelUseSpecified": output["channelUseSpecified"],
            "channelUse": output["channelUse"], "guiVisibleIf": output["guiVisibleIf"], "mipmaps": output["mipmaps"],
            "outputGuiType": output["outputGuiType"],"resultFormat": output["resultFormat"],"type": output["type"],
            "userTag": output["userTag"]}
            if shader_id is not None:
                graph["outputs"][key]["shader_enabled"] = getattr(shader_outputs,shader_id + "_enabled")
                graph["outputs"][key]["shader_colorspace"] = getattr(shader_outputs,shader_id + "_colorspace")
                format = getattr(shader_outputs, shader_id + "_format")
                bitdepth = getattr(shader_outputs, shader_id + "_bitdepth")
                graph["outputs"][key]["shader_format"] = format
                graph["outputs"][key]["shader_bitdepth"] = bitdepth # OJO o 0???
            else:
                value_enabled = len(shader_outputs.shader_preset.outputs.keys()) == 0
                graph["outputs"][key]["shader_enabled"] = value_enabled
                graph["outputs"][key]["shader_colorspace"] = preferences.output_default_colorspace
                format = preferences.output_default_format
                graph["outputs"][key]["shader_format"] = format
                graph["outputs"][key]["shader_bitdepth"] = 0 # ojo o default bitdepth
    graph["presets"].append({"label": "Default","value": default_preset,"embedded": True,"icon": "LOCKED"})
    graph["presets"].append({"label": "Custom","value": default_preset,"embedded": False,"icon": "UNLOCKED"})
    for preset in embedded_presets[graph["id"]]:
        graph["presets"].append({"label": preset["label"],"embedded": True,"icon": "LOCKED","value": preset["value"]})
    sbsar_json["graphs"].append(graph)


# listo el yeison

            
               
               
spg1=bpy.data.scenes["Scene"]['SUBSTANCE_SGP_B82B0FF3-9EE5-4C1C-ACF0-BD13399E11B5']
spg1['density'] = 0.8
 





# para modificar
pp = scn['SUBSTANCE_SGP_' + id]
pp['contrast'] = 0.2


