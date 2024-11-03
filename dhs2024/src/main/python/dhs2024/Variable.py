from typing import Any
from ID import ID
from ID import TipoDato

class Variable(ID):
    def __init__(self, nombre, tipoDato, inicializado, usado):
        super().__init__(nombre, tipoDato, inicializado, usado)
        self.tipo = "variable"
    
    def __str__(self):
         return("ID:"+self.nombre+"\tTipo:Variable \t"+str(self.tipoDato)+"\tInicializado:"+str(self.inicializado)+"\t Usado:"+str(self.usado))
