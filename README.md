# SC_ModeloAgentes

## Ambiente
El ambiente es la ciudad en la que se colocarán los agentes, donde estos se moverán e interactuarán. Tiene métodos para uso en la misma ciudad y sobre los agentes. 
Los métodos para la ciudad son:

* **generarindividuos()**: Generar los individuos.
* **crear_hogares()**: Crear los hogares.
* **conectar_a_casas(nodo_id)**: Hacer las conexiones entre los nodos casas y los lugares.
* **crear_nodo(\*args)**: Crear cada nodo, asignarle un tipo y la cuadrícula (espacio) correspondiente.


Los métodos que funcionan sobre individuos son:

* **mover_en_espacio(individuo, nueva_posición)**: Mover los individuos dentro de un espacio.
* **mover_en_nodos(individuo, nuevo_nodo_id)**: Mover los individuos entre dos nodos. Se colocará al individuo en la posición [0,0] del espacio del nuevo nodo.
* **contactos(individuo)**: Devolver los individuos que se encuentran en la misma posicioń que el individuo en cuestión, incluyéndolo.
* **siguiente_paso_aleatorio(individuo)**Movimiento aleatorio dentro del espacio en el que se encuentra el individuo. Este método no debería ser utilizado, el individuo debería tener un método que haga lo mismo. El paso se da en una unidad en 8 direcciones.

Otros métodos de utilidad son:

* **ajustar_posicion(posicion, espacio)**: Ajustar la posición a un espacio determinado.
* **obtener_espacio()**: Obtener la instancia del espacio en el que se encuentra un individuo o que contiene un nodo. Al ser una instancia de **mesa.space.MultiGrid** se tiene acceso a sus propios métodos.

### Inicialización

Para inicializar este objeto se debe proporcionar (inicialmente) el modelo al que pertenece y la clase *agente* con la que creará a los individuos. La clase *agente* deberá tener, de preferencia, los atributos: *pos*, *casa_id* y *nodo_actual*. En caso de no tenerlos, la misma ciudad los creará, sin embargo puede generar dificultades en la lectura del código.
