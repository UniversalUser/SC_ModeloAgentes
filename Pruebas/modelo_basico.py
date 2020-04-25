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
from individuo import Individuo_2

##IMPORTANTE: Se requiere el módulo tornado con versión 4.5.3
from mesa import Model
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation
from random import choices, seed
from math import sqrt
seed(920204)

class Modelo(Model):
    #Algunas constantes
    SUCEPTIBLE = 0
    EXPUESTO = 1
    INFECTADO = 2
    RECUPERADO = 3
    salud_to_str={0:'Suceptible', 1:'Expuesto', 2:'Infectado', 3:'Recuperado'}
    pp_dia = 1 ## Son los pasos dados por dia simulado
    def __init__(self, N, city_object, agent_object, ind_attrs):
        super().__init__()
        self.num_ind = N
        self.city_object = city_object
        self.agent_object = agent_object
        self.ind_attrs = ind_attrs
        self.schedule = RandomActivation(self)
        self.generar_espacio()
        self.n_paso = 0
        
        ## Se define el grid que se representará en la 
        self.grid = self.ciudad.nodes['ciudad']['espacio']
        self.datacollector = DataCollector(
            model_reporters = {'Suceptibles': self.conteo_func(self.SUCEPTIBLE),
                               'Expuestos': self.conteo_func(self.EXPUESTO),
                               'Infectados': self.conteo_func(self.INFECTADO),
                               'Recuperados': self.conteo_func(self.RECUPERADO)})
        self.conteo_instantaneo = [N,0,0,0]
    
    def generar_espacio(self):
        self.ciudad = self.city_object(self, self.agent_object)
        
        for ind in self.ciudad.generar_individuos(self.ind_attrs):
            self.schedule.add(ind)
        
        #Se crea el espacio donde estarán los individuos
        self.ciudad.crear_nodo('ciudad', tipo='ciudad',
                               ocupantes = self.ciudad.agentes_a_asignar,
                               tamano=10)#int(sqrt(self.num_ind)+5))
        
        #Se planta un infectado en la simulación
        for ind in choices(self.schedule.agents, k = 3):
            ind.salud = self.INFECTADO
            ind.asintomatico = False      

    
    def step(self):
        self.momento = self.n_paso % self.pp_dia #es el momento del dia
        self.conteo()
        self.datacollector.collect(self)
        self.schedule.step()
        self.n_paso += 1

    
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


def dibujar_agente(agent):
    color = 'green'
    radio = 1
    layer = 0

    if agent.salud == agent.model.EXPUESTO:
        color = 'orange'
        radio = 0.8
        layer = 1
    elif agent.asintomatico and agent.salud == agent.model.INFECTADO:
        color = 'blue' 
        radio = 0.4
        layer = 3
    elif agent.salud == agent.model.INFECTADO:
        color = 'red' 
        radio = 0.6
        layer = 2
    elif agent.salud == agent.model.RECUPERADO:
        color = 'black'
        radio = 0.2
        layer = 4

    portrayal = {"Shape": "circle",
                 "Color": color,
                 "Filled": "true",
                 "Layer": layer,
                 "r": radio,
                 #'text': agent.unique_id,
                 #'text_color': 'black'
                 }
    return portrayal



n_agentes = 20
attrs_individuos = {
                    'evitar_agentes': True,
                    'evitar_sintomaticos': False,
                    'distancia_paso': 1,
                    'activar_cuarentena': False,
                    'quedate_en_casa': False,
                    'prob_contagiar': 0.5,
                    'prob_infectarse': 0.8,
                    'radio_de_infeccion': 1
                    }


tamano = int(sqrt(n_agentes)+5)
malla = CanvasGrid(dibujar_agente, 10, 10 , 600, 600)
grafico = ChartModule([{'Label': 'Suceptibles',
                        'Color': 'Green'},
                     {'Label': 'Expuestos',
                        'Color': 'Orange'},
                     {'Label': 'Infectados',
                        'Color': 'Red'},
                     {'Label': 'Recuperados',
                        'Color': 'Black'}],
                    data_collector_name = 'datacollector')

argumentos_modelo ={"N":n_agentes, "city_object": Ciudad, 
                    "agent_object": Individuo_2,
                    "ind_attrs": attrs_individuos}

server = ModularServer(Modelo,
                       [malla, grafico],
                       "Modelo",
                       argumentos_modelo)

server.port = 8521
server.launch()