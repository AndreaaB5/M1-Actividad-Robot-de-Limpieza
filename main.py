from aspiradora import *
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

listaLosetasLimpias = []
def agent_portrayal(agent):

    
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "red",
                 "r": 0.5}
    if(type(agent) == Aspiradora):
        portrayal["Color"] = "red"
        portrayal["Layer"] = 0
        if(agent.pasos == 20):
            listaLosetasLimpias.append(agent.limpias)
            
    if(type(agent) == Loseta):
        if(agent.sucia == 1):
            portrayal["Color"] = "blue"
            portrayal["Layer"] = 0
        else:
            portrayal["Color"] = "grey" 
            portrayal["Layer"] = 1
            portrayal["r"] = 0.1
    
    return portrayal


ancho = 50
alto = 25
grid = CanvasGrid(agent_portrayal, ancho, alto, 750, 750)
server = ModularServer(AspirarModel,
                       [grid],
                       "Trafic Model",
                       {"width":ancho, "height":alto})


server.port = 8521 
server.launch()