from mesa import Model
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation



class Visualizador():
    def __init__(self, figsize = (5,5)):
        plt.ion()
        self.fig, self.ax = plt.subplots(figsize = figsize)

    def show(self, img, title = '', **kargs):
        self.vis = self.ax.imshow(img, **kargs)
        self.ax.set_title(title)
        plt.colorbar(self.vis)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def update(self, img, title = ''):
        self.vis.set_data(img)
        self.ax.set_title(title)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()



class Modelo(Model):
    #Algunas constantes
    SUCEPTIBLE = 0
    EXPUESTO = 1
    INFECTADO = 2
    RECUPERADO = 3
    salud_to_str={0:'Suceptible', 1:'Expuesto', 2:'Infectado', 3:'Recuperado'}
    def __init__(self, N, city_object, agent_object):
        super().__init__()
        self.num_ind = N
        self.city_object = city_object
        self.agent_object = agent_object
        self.schedule = RandomActivation(self)
        self.crearciudad()
        self.grid = self.ciudad.nodes['aurrera']['espacio']
        self.datacollector = DataCollector(
            model_reporters = {'Suceptibles': self.conteo_func(self.SUCEPTIBLE),
                               'Expuestos': self.conteo_func(self.EXPUESTO),
                               'Infectados': self.conteo_func(self.INFECTADO),
                               'Recuperados': self.conteo_func(self.RECUPERADO)})
        self.conteo_instantaneo = [N,0,0,0]
    
    def crearciudad(self):
        self.ciudad = self.city_object(self, self.agent_object)
        for ind in self.ciudad.generarindividuos():
            self.schedule.add(ind)
        
        #Se planta un infectado en la simulación
        self.schedule.agents[0].salud = self.INFECTADO
        
        #Se crean las casas distribuyendo los individuos
        self.ciudad.crear_hogares()
        
        #Se agrega una tienda a la ciudad y se conecta con todas las casas
        self.ciudad.crear_nodo('aurrera', tipo='tienda', tamano=25)
        self.ciudad.conectar_a_casas('aurrera')
    
    def step(self):
        self.conteo()
        self.datacollector.collect(self)
        self.schedule.step()

    
    def conteo(self):
        #Una función para contar los casos actuales en la ciudad
        self.conteo_instantaneo = [0,0,0,0]
        for a in self.schedule.agents:
            self.conteo_instantaneo[a.salud] += 1
        return self.conteo_instantaneo

    def conteo_func(self, tipo):
        def contar(modelo):
            return modelo.conteo_instantaneo[tipo]
        return contar

if __name__=='__main__':
    ##Se agregan las rutas a los módulos a utilizar
    import sys
    import os
    _root = os.path.abspath('../')
    _paths = [os.path.join(_root, 'Ambiente'),
              os.path.join(_root, 'Individuos')]
    for p in _paths:
        if p not in sys.path:
            sys.path.append(p)
    
    
    from ambiente import Ciudad
    from individuo import Individuo
    
    import numpy as np
    import matplotlib.pyplot as plt
    import networkx as nx
    from matplotlib.colors import Colormap
    from time import sleep
    n_individuos = 2000
    m = Modelo(n_individuos, Ciudad, Individuo)
    #fig, ax = plt.subplots(figsize = (20,20))
    #nx.draw(m.ciudad, ax = ax)
    
    vis = Visualizador()
    conteo_espacio, _total = m.ciudad.ver_espacio(0)
    vis.show(conteo_espacio, vmin = 0, vmax = 5, cmap = plt.get_cmap('jet'))
    historico = []
    for i in range(10):
        m.step()
        conteo = m.conteo()
        historico.append(conteo)
        conteo_espacio, _total = m.ciudad.ver_espacio(0)
        #print(i, conteo_espacio)
        vis.update(conteo_espacio, f'Paso {i+1}')
        #sleep(1)
    
    historico = np.array(historico)
    fig, ax = plt.subplots()
    ax.plot(historico[:,0], label = 'Suceptibles')
    ax.plot(historico[:,1], label = 'Expuestos')
    ax.plot(historico[:,2], label = 'Infectados')
    ax.plot(historico[:,3], label = 'Recuperados')
    ax.set_xlabel('Iteraciones')
    ax.set_ylabel('Población')
    ax.set_title('Simulación del avance de una infección')
    ax.legend()
    plt.show()