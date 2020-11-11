# virtualroom
Virtual Room using Blender > Substance > Unreal Engine

## TODO

- Speaker tiene que tener incorporado como atributo el elemnto de la libreria de donde lee el mesh (Genelec.blend)
- Spot deberia incorporar los atributos que ahora estan en un diccionario
- Scales es ahora un atributo de la sala no de los materiales, en realidad cada elemento (wall, floor, ceil) deberia tener asociada su propia escala de UV, y luego modificar room utils para que la aplique
- Los materiales deberian referenciarse solo por su nombre y la categoria a la que pertenecen (Wood, Plaster, etc) como atributo, y con esa categoria y el nombre del material se arma la ruta hacia las texturas. 
