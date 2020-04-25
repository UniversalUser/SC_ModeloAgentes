# Modelo Agentes

## Individuo
El individuo será una instancia de la clase *Agent* del módulo **Mesa**. Dichos agentes pueden tener uno de los cuatro estados del modelo SEIR (suceptible, expuesto, infectado, recuperado). Cada individuo cuenta con atributos de interés:

* **De comportamiento**: *evitar_agentes* (moverse aleatoriamente evitando el contacto con otros agentes), *activar_cuarentena* (una vez infectado no sale de casa), *quedate_en_casa* (baja probabilidad de salir de casa), *prob_movimiento* (probabilidad de que cambie del nodo actual).
* **De la enfermedad**: pasos necesarios para infectarse y recuperarse.
* **Ante la enfermedad**: *prob_contagiar* (probabilidad de contagiar), *prob_infectarse* (probabilidad de adquirir el virus), *prob_recuperarse* (probabilidad de recuperarse de la infección. Los que no se recuperan mueren. TODAVÍA NO IMPLEMENTADO), *radio_de_infeccion* (radio alrededor del cual el agente puede infectar), *asintomatico* (si es asintomtico o no. TODAVÍA NO SE USA ESTE ATRIBUTO)

Como métodos solamente cuenta con 2:

* **step()**: Donde se programa el comportamiento de movimiento del individuo.
* **interactuar()**: Donde se programa el comportamiento de interacción del individuo.

## Ambiente
El ambiente contiene la clase **Ciudad** en la que se colocarán los agentes, donde estos se moverán e interactuarán. Los agentes se distribuyen en nodos que representan sus casas que pueden estar conectados a otros tipos de nodos (tiendas, ciudades, etc). Cada nodo tiene una gradilla interna donde los agentes pueden moverse libremente llamada **espacio**. Este espacio no es toroidal (para considerar el comportamiento del agente dentro de dicho espacio). La clase Ciudad tiene métodos para uso en la misma ciudad y sobre los agentes.
Los métodos para la ciudad son:

* **generarindividuos()**: Generar los individuos.
* **crear_hogares()**: Crear los hogares.
* **conectar_a_casas(nodo_id)**: Hacer las conexiones entre los nodos casas y los lugares.
* **crear_nodo(nodo_id, tipo, ocupantes = [], tamano = None)**: Crear cada nodo, asignarle un tipo y la cuadrícula (espacio) correspondiente.

Los métodos que funcionan sobre individuos son:

* **mover_en_espacio(ind, nueva_pos)**: Mueve al individuo en el espacio en el que se encuentra.
* **mover_en_nodos(ind, nuevo_nodo_id, pos = None)**: Mueve al individuo del nodo en el que se encuentra al nuevo nodo. Si no se especifica la posición, entonces se coloca al azar dentro del espacio del nuevo nodo.
* **obtener_contactos(individuo, r=0)**: Devuelve la lista de individuos que se encuentran dentro de un radio *r* en su espacio, excluyéndolo.
* **siguiente_paso_aleatorio(individuo, evitar_agentes = False)**: Movimiento aleatorio dentro del espacio en el que se encuentra el individuo. Este método no debería ser utilizado, el individuo debería tener un método que haga lo mismo. El paso se da en una unidad en las 8 direcciones adyacentes a la celda a la que se encuentra, considerando los límites del espcio. Si *evitar_agentes* es verdadero, entonces se moverá solamente si hay algún espacio disponible.
* **obtener_familia(ind)**: Devuelve una lista de los **ids** de los individuos que habitan su misma casa.


Otros métodos de utilidad son:

* **ajustar_posicion(posicion, espacio)**: Ajustar la posición de tal manera que se encuentre dentro del espacio en cuestión.
* **obtener_espacio()**: Obtener la instancia del espacio en el que se encuentra un individuo o que contiene un nodo. Al ser una instancia de **mesa.space.MultiGrid** se tiene acceso a sus métodos nativos.

### Inicialización

Para inicializar este objeto se debe proporcionar el *modelo* al que pertenece y la clase *agente* con la que creará a los individuos. La clase *agente* deberá tener, de preferencia, los atributos: *pos*, *casa_id* y *nodo_actual*. En caso de no tenerlos, la misma ciudad los creará, sin embargo puede generar dificultades en la lectura del código.
