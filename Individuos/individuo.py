#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from mesa import Agent
from random import random, sample

#Algunas constantes
SUCEPTIBLE = 0
EXPUESTO = 1
INFECTADO = 2
RECUPERADO = 3
salud_to_str={0:'Suceptible', 1:'Expuesto', 2:'Infectado', 3:'Recuperado'}

class Individuo(Agent):
    
    def __init__(self, unique_id, model, edad, sexo):
        super().__init__(unique_id, model)
        self.ciudad = self.model.ciudad
        self.pos = None
        self.salud = SUCEPTIBLE
        self.sexo = sexo
        self.edad = edad
        self.pasos_infectado=0
        self.casa_id = None
        self.nodo_actual = None
        self.R0 = 6 # Índice de reproducción de la enfermedad entre individuos.
        self.pasos_para_infectar = 15
        self.pasos_para_recuperarse = 8
        self.asintomatico = False  # transmite, sin sintomas, no esta en cuarentena y su movilidad es regular. pend.
        self.en_cuarentena = 0 # 1: reduce movilidad, 2: aislamiento total.
        self.diagnosticado = False  # Se sabe que tiene la enfermedad y debe de estar en cuarentena. pend.
        self.politica_encasa = False
        self.politica_higiene = 0.0 # porcentaje de reduccion de la probalidad de contagio.
        self.mortalidad_apriori = 0.05 # pend.

    def step(self):
        if self.salud == SUCEPTIBLE or self.salud == EXPUESTO:

          if self.politica_encasa:
            habitantes=len(self.ciudad.nodes[self.casa_id]['habitantes'])
            moverse_entre_nodos = random() < (1/habitantes)
          else:
            moverse_entre_nodos = random() < 0.01

          if moverse_entre_nodos:
              if self.ciudad.nodes[self.nodo_actual]['tipo'] == 'casa':
                  self.ciudad.mover_en_nodos(self, 'aurrera')
              else:
                  self.ciudad.mover_en_nodos(self, self.casa_id)
          else:
              self.ciudad.siguiente_paso_aleatorio(self)

        elif self.salud == INFECTADO:

          moverse_entre_nodos = random() < 0.25

          if moverse_entre_nodos and not self.en_cuarentena==2:
              if self.ciudad.nodes[self.nodo_actual]['tipo'] == 'casa':
                  self.ciudad.mover_en_nodos(self, 'aurrera')
              else:
                  self.ciudad.mover_en_nodos(self, self.casa_id)
          else:
              self.ciudad.siguiente_paso_aleatorio(self)

        elif self.salud == RECUPERADO:

          moverse_entre_nodos = random() < 0.5

          if moverse_entre_nodos and not self.en_cuarentena==2:
              if self.ciudad.nodes[self.nodo_actual]['tipo'] == 'casa':
                  self.ciudad.mover_en_nodos(self, 'aurrera')
              else:
                  self.ciudad.mover_en_nodos(self, self.casa_id)
          else:
              self.ciudad.siguiente_paso_aleatorio(self)

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
        x, y = self.pos
        contactos = self.model.ciudad.nodes[self.nodo_actual]['espacio'][x][y]
        por_contagiar = self.R0//2
        prob_contagio = .8*(1-self.politica_higiene)
        if self.salud == INFECTADO and not self.en_cuarentena == 2:
            for a in sample(contactos, min(por_contagiar, len(contactos))):
                if a.salud == SUCEPTIBLE and random() < prob_contagio:
                    a.salud = EXPUESTO


##----------------------------------------------------------------------------


class Individuo_basico(Agent):
    
    def __init__(self, unique_id, model, edad, sexo):
        super().__init__(unique_id, model)
        self.ciudad = self.model.ciudad
        self.pos = None
        self.salud = SUCEPTIBLE
        self.sexo = sexo
        self.edad = edad
        self.pasos_infectado=0
        self.casa_id = None
        self.nodo_actual = None
        self.R0 = 10
        self.pasos_para_infectar = 10
        self.pasos_para_recuperarse = 5

    def step(self):
        moverse_entre_nodos = random() < 0.005
        if moverse_entre_nodos:
            if self.ciudad.nodes[self.nodo_actual]['tipo'] == 'casa':
                self.ciudad.mover_en_nodos(self, 'aurrera')
            else:
                self.ciudad.mover_en_nodos(self, self.casa_id)
        else:
            #if self.nodo_actual=='aurrera':
            #    print(f'Ind {self.unique_id} da paso aleatorio')
            self.ciudad.siguiente_paso_aleatorio(self)
            
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
        x, y = self.pos
        contactos = self.model.ciudad.nodes[self.nodo_actual]['espacio'][x][y]
        por_contagiar = self.R0
        prob_contagio = .8
        if self.salud == INFECTADO:
            for a in sample(contactos, min(por_contagiar, len(contactos))):
                if a.salud == SUCEPTIBLE and random() < prob_contagio:
                    a.salud = EXPUESTO