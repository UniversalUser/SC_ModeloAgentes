#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 10:47:42 2020

@author: carlos
"""
import numpy as np
import matplotlib.pyplot as plt
from networkx import Graph
import networkx as nx
from mesa import Agent, Model
from mesa.time import BaseScheduler, RandomActivation
from random import gauss, random, sample, choice


#Algunas constantes
SUCEPTIBLE = 0
EXPUESTO = 1
INFECTADO = 2
RECUPERADO = 3
salud_to_str={0:'Suceptible', 1:'Expuesto', 2:'Infectado', 3:'Recuperado'}
    

class Ciudad(Graph):
    """
    La ciudad es la que se encargará de generar los nodos que representen
    lugares de la ciudad como casas, centros comerciales, iglesias, o lo que sea.
    Tiene 4 métodos:
        * Generar los individuos
        * Crear los hogares
        * Hacer las conexiones entre los nodos casas y los lugares
        * Mover los individuos a nodos específicos
    La ciudad está representada como un grafo.
    """
    def __init__(self, model, agent_object):
        super().__init__()
        self.agent_object = agent_object
        self.model = model
        self.p_matrimonio = 0.8
        self.promedio_hijos = 2
        self.casasids = []
        self.lugaresids = []
        self.agentes_a_asignar = []
    
    def generarindividuos(self):
        """
        Considerando el porcentaje de hombres y mujeres en la población, y la
        distribución de las edades en la población (considerando una distribución
        normal) se procede a generar la población.
        """
        porcentaje_hombres = 0.49
        individuos = []
        for i in range(self.model.num_ind):
            if random() <= porcentaje_hombres:
                sexo = 'h'
            else:
                sexo = 'm'
            edad = gauss(25,20)
            if edad < 0:
                edad = 0
            elif edad > 80:
                edad = 80
            individuos.append(self.agent_object(i,
                                        self.model, 
                                        edad,
                                        sexo)
                              )
        self.agentes_a_asignar = individuos
        return individuos
    
    def crear_hogares(self):
        """
        Consideranco la probabilidad de que en una casa exista un matrimonio, 
        y el promedio de hijos menores a 23 años en cada casa, se asignan
        individuos a cada nodo hogar.
        Se consideran personas solteras con y sin hijos.
        """
        #Se generan las listas con cada tipo de individuos a repartir
        hombres = [ind for ind in self.agentes_a_asignar if ind.sexo == 'h' and ind.edad>=23]
        mujeres = [ind for ind in self.agentes_a_asignar if ind.sexo == 'm' and ind.edad>=23]
        hijos = [ind for ind in self.agentes_a_asignar if ind.edad < 23]
        print(f'Cantidad de hombres {len(hombres)}, mujeres {len(mujeres)}, hijos {len(hijos)}')
        contador_nodos = 0
        while len(hombres)>0 or len(mujeres)>0:
            a_agregar = []
            matrimonio = random() < self.p_matrimonio
            ##Se asignan primero los jefes de familia (hombre y/o mujer)
            if len(hombres)*len(mujeres)>0 and matrimonio:
                a_agregar.append(hombres.pop())
                a_agregar.append(mujeres.pop())
            else:
                seleccion = sample([hombres, mujeres], 2)
                if len(seleccion[0])>0:
                    a_agregar.append(seleccion[0].pop())
                else:
                    a_agregar.append(seleccion[1].pop())
            
            ##Se asignan los hijos a cada casa
            n_hijos = abs(int(gauss(self.promedio_hijos, 0.5)))
            while len(hijos)>0 and n_hijos>0:
                a_agregar.append(hijos.pop())
                n_hijos-=1
            
            print(f'En la casa {contador_nodos} hay {len(a_agregar)} personas. Matrimonio : {matrimonio}')
            for i in a_agregar:
                i.casa_id = contador_nodos
                i.nodo_actual = contador_nodos
            
            ##Se procede a crear el nodo correspondiente
            self.add_node(contador_nodos, tipo = 'casa',
                          habitantes = [ind.unique_id for ind in a_agregar],
                          ocupantes = a_agregar)
            self.casasids.append(contador_nodos)
            contador_nodos += 1
        
        ##Si sobran hijos, entonces se agregan al azar a todos los nodos
        while len(hijos) > 0:
            hijo = hijos.pop()
            idcasa = choice(list(self.nodes))
            print(f'Se agrega un hijo a la casa {idcasa}... ', end='')
            self.nodes[idcasa]['habitantes'].append(hijo.unique_id)
            self.nodes[idcasa]['ocupantes'].append(hijo)
            hijo.casa_id = idcasa
            hijo.nodo_actual = idcasa
            print('Agregado')
        
    def conectaracasas(self, nid):
        for i in list(self.nodes):
            if self.nodes[i]['tipo']=='casa':
                self.add_edge(nid,i)
    
    def mover_individuo(self, ind, nuevonodo_id):
        self.nodes[ind.nodo_actual]['ocupantes'].remove(ind)
        self.nodes[nuevonodo_id]['ocupantes'].append(ind)
        ind.nodo_actual = nuevonodo_id
            

class Individuo(Agent):
    
    def __init__(self, unique_id, model, edad, sexo):
        super().__init__(unique_id, model)
        self.salud = SUCEPTIBLE
        self.sexo = sexo
        self.edad = edad
        self.pasos_infectado=0
        self.casa_id = None
        self.nodo_actual = None
        self.R0 = 6
        self.pasos_para_infectar = 15
        self.pasos_para_recuperarse = 8

    def step(self):
        moverse = random() < 0.5
        if moverse:
            if self.model.ciudad.nodes[self.nodo_actual]['tipo'] == 'casa':
                self.model.ciudad.mover_individuo(self, 2000)
            else:
                self.model.ciudad.mover_individuo(self, self.casa_id)
        
        self.interactuar()
        
        ## Se revisa la evolución de su salud
        if self.salud == EXPUESTO:
            self.pasos_infectado += 1
            if self.pasos_infectado > self.pasos_para_infectar:
                self.salud = INFECTADO
        elif self.salud == INFECTADO:
            self.pasos_infectado += 1
            if self.pasos_infectado>self.pasos_para_infectar + self.pasos_para_recuperarse:
                self.salud = RECUPERADO
    
    def interactuar(self):
        ## Se selecciona un número de agentes por contagiar de entre los que
        ## se encuentran en su mismo nodo, solamente si está infectado
        contactos = self.model.ciudad.nodes[self.nodo_actual]['ocupantes']
        por_contagiar = self.R0//2
        prob_contagio = .8
        if self.salud == INFECTADO:
            for a in sample(contactos, min(por_contagiar, len(contactos))):
                if a.salud == SUCEPTIBLE and random() < prob_contagio:
                    a.salud = EXPUESTO

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
        self.ciudad.add_node(2000, tipo='tienda',
                             habitantes = None, ocupantes = [])
        self.ciudad.conectaracasas(2000)
    
    def step(self):
        self.schedule.step()

    
    def conteo(self):
        #Una función para contar los casos actuales en la ciudad
        datos = [0,0,0,0]
        for a in self.schedule.agents:
            datos[a.salud] += 1
        return datos



if __name__=='__main__':
    m = Modelo(1000, Ciudad, Individuo)
    nx.draw(m.ciudad)
    historico = []
    for i in range(100):
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