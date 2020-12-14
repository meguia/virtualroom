# virtualroom
Virtual Room using Blender > Substance > Unreal Engine

## TODO

- &#10003; Speaker tiene que tener incorporado como atributo el elemnto de la libreria de donde lee el mesh (Genelec.blend)
- &#10003; Spot deberia incorporar los atributos que ahora estan en un diccionario
- &#10003; Scales es ahora un atributo de la sala no de los materiales, en realidad cada elemento (wall, floor, ceil) deberia tener asociada su propia escala de UV, y luego modificar room utils para que la aplique
- &#10003;Los materiales deberian referenciarse solo por su nombre y la categoria a la que pertenecen (Wood, Plaster, etc) como atributo, y con esa categoria y el nombre del material se arma la ruta hacia las texturas*. 
- La escala de los mapas UV deberia depender de las dimensiones en metros de los elementos, para que las texturas no se estiren, ahora estan fijas, habria que agregar la escala del objeto como atributo del elemento
- las luces simetricas deberian definirse con un unico set de parametros
- ver ajustes de iluminacion global como ambient occlusion
 
