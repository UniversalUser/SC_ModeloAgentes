#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 19:34:59 2020

@author: carlos
"""
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

##IMPORTANTE: Se requiere el módulo tornado con versión 4.5.3
from mesa import Model
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.datacollection import DataCollector
from mesa.time import RandomActivation


#Algunas constantes
SUCEPTIBLE = 0
EXPUESTO = 1
INFECTADO = 2
RECUPERADO = 3

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


def dibujar_agente(agent):
    color = 'green'
    radio = 0.8
    layer = 0

    if agent.salud == EXPUESTO:
        color = 'orange'
        radio = 0.6
        layer = 1
    elif agent.salud == INFECTADO:
        color = 'red'
        radio = 0.4
        layer = 2
    elif agent.salud == RECUPERADO:
        color = 'black'
        radio = 0.2
        layer = 3

    portrayal = {"Shape": "circle",
                 "Color": color,
                 "Filled": "true",
                 "Layer": layer,
                 "r": radio}
    return portrayal


malla = CanvasGrid(dibujar_agente, 25, 25, 800, 800)
grafico = ChartModule([{'Label': 'Suceptibles',
                        'Color': 'Green'},
                     {'Label': 'Expuestos',
                        'Color': 'Orange'},
                     {'Label': 'Infectados',
                        'Color': 'Red'},
                     {'Label': 'Recuperados',
                        'Color': 'Black'}],
                    data_collector_name = 'datacollector')

argumentos_modelo ={"N":20000, "city_object": Ciudad, 
                    "agent_object": Individuo}

server = ModularServer(Modelo,
                       [malla, grafico],
                       "Modelo",
                       argumentos_modelo)

server.port = 8521
server.launch()