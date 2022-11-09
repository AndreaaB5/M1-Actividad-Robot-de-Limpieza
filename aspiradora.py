import numpy as np
import pandas as pd
from mesa import Agent, Model
from mesa.datacollection import DataCollector
from mesa.space import MultiGrid
from mesa.time import SimultaneousActivation


class Loseta(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.next_state = None
        self.sucia = 0

class Aspiradora(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.next_state = None
        self.pasos = 0
        self.limpias = 0
    
    def step(self):
        self.move()
        self.limpia()
        self.pasos += 1
        
    

    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False
        )
        
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)
    
    def limpia(self):
        
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        Loseta = cellmates[0]
        if(type(Loseta) != type(self)):
            if(Loseta.sucia == 1):
                Loseta.sucia = 0
                self.limpias += 1


    def advance(self):
        self.live = self.next_state
            
class AspirarModel(Model):
    def __init__(self, width, height):
        self.num_agents =  50
        self.grid = MultiGrid(width, height, True)
        self.schedule = SimultaneousActivation(self)
        self.running = True 
        
        for (content, x, y) in self.grid.coord_iter():
            c = Loseta((x+2, y+2), self)
            self.grid.place_agent(c, (x, y))
            self.schedule.add(c)
        for i in range(self.num_agents):
            a = Aspiradora((1, i+1), self)
            self.grid.place_agent(a, (1, 1)) 
            self.schedule.add(a)

##
        
        porcentaje = 10
        area = self.grid.width*self.grid.height
        numLosetas = (area * porcentaje)//100
        print("Losetas:",numLosetas)
        print("Agentes totales:",self.schedule.get_agent_count())

        
        for i in range(numLosetas):
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            c = self.grid[x][y]
            c[0].sucia=1
        
    
    def step(self):
        self.schedule.step()
        
        