# SC_ModeloAgentes

## Ambiente
 El ambiente es la ciudad en la que se colocarán los agentes, donde estos se moverán e interactuarán. Tiene métodos para uso en la misma ciudad y sobre los agentes. 

 Los métodos para la ciudad son:

    * Generar los individuos **(ciudad.generarindividuos())**.
    * Crear los hogares **(ciudad.crear_hogares())**.
    * Hacer las conexiones entre los nodos casas y los lugares **(ciudad.conectar_a_casas(nodo_id))**.
    * Crear cada nodo, asignarle un tipo y la cuadrícula (espacio) correspondiente **(crear_nodo(*args))**.

Los métodos que funcionan sobre individuos son:

    * Mover los individuos dentro de un espacio **(ciudad.mover_en_espacio(individuo, nueva_posición))**.
    * Mover los individuos entre dos nodos. Se colocará al individuo en la posición [0,0] del espacio del nuevo nodo **(ciudad.mover_en_nodos(individuo, nuevo_nodo_id))**.
    * Devolver los individuos que se encuentran en la misma posicioń que el individuo en cuestión, incluyéndolo **(ciudad.contactos(individuo))**.
    * Movimiento aleatorio dentro del espacio en el que se encuentra el individuo. Este método no debería ser utilizado, el individuo debería tener un método que haga lo mismo. El paso se da en una unidad en 8 direcciones **(ciudad.siguiente_paso_aleatorio(individuo))**.

Otros métodos de utilidad son:

	* Ajustar la posición a un espacio determinado **(ciudad.ajustar_posicion(posicion, espacio))**.
	* Obtener la instancia del espacio en el que se encuentra un individuo o que contiene un nodo. Al ser una instancia de **mesa.space.MultiGrid** se tiene acceso a sus propios métodos **(ciudad.obtener_espacio())**.

### Inicialización

Para inicializar este objeto se debe proporcionar (inicialmente) el modelo al que pertenece y la clase *agente* con la que creará a los individuos. La clase *agente* deberá tener, de preferencia, los atributos: *pos*, *casa_id* y *nodo_actual*. En caso de no tenerlos, la misma ciudad los creará, sin embargo puede generar dificultades en la lectura del código.
