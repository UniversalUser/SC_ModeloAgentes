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
from mesa import Model
from mesa.time import RandomActivation


#Algunas constantes
SUCEPTIBLE = 0
EXPUESTO = 1
INFECTADO = 2
RECUPERADO = 3
salud_to_str={0:'Suceptible', 1:'Expuesto', 2:'Infectado', 3:'Recuperado'}

class Modelo(Model):
    def __init__(self, N, city_object, agent_object):
        self.num_ind = N
        self.city_object = city_object
        self.agent_object = agent_object
        self.schedule = RandomActivation(self)
        self.crearciudad()
    
    def crearciudad(self):
        self.ciudad = self.city_object(self, self.agent_object)
        for ind in self.ciudad.generarindividuos():
            self.schedule.add(ind)
        
        #Se planta un infectado en la simulación
        self.schedule.agents[0].salud = INFECTADO
        
        #Se crean las casas distribuyendo los individuos
        self.ciudad.crear_hogares()
        
        #Se agrega una tienda a la ciudad y se conecta con todas las casas
        self.ciudad.crear_nodo('aurrera', tipo='tienda', tamano=2)
        self.ciudad.conectar_a_casas('aurrera')
    
    def step(self):
        self.schedule.step()

    
    def conteo(self):
        #Una función para contar los casos actuales en la ciudad
        datos = [0,0,0,0]
        for a in self.schedule.agents:
            datos[a.salud] += 1
        return datos


import numpy as np
import matplotlib.pyplot as plt
m = Modelo(1000, Ciudad, Individuo)
#nx.draw(m.ciudad)
historico = []
for i in range(200):
    m.step()
    conteo = m.conteo()
    historico.append(conteo)

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