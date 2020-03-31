# SC_ModeloAgentes

## Ambiente
 El ambiente es la ciudad en la que se colocarán los agentes. La ciudad tiene 4 métodos principales
    * Generar los individuos (ciudad.generarindividuos())
    * Crear los hogares (ciudad.crear_hogares())
    * Hacer las conexiones entre los nodos casas y los lugares (ciudad.conectaracasas(nodoid))
    * Mover los individuos a nodos específicos (ciudad.mover_individuo(ind, nodoid))

El modelo es el que crea la ciudad y deberá tener el atributo modelo.ciudad, así el agente podrá interactuar directamente con la ciudad, por ejemplo para mover un individuo dentro de la ciudad.
