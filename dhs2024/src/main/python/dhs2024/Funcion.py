from typing import Any
from ID import ID
from ID import TipoDato

class Funcion(ID):

    #args = list()
    argumentos = []

    def __init__(self, nombre, tipoDato, inicializado, usado, argumentos):
        super().__init__(nombre, tipoDato, inicializado, usado)
        self.argumentos = argumentos

        print("Funcion '" + self.nombre + "' devuelve " + str(self.tipoDato) + " y tiene los siguientes argumentos :\n")
        for argumento in self.argumentos:
            print(argumento)
        #self.tipo = "funcion"

    def __str__(self):
        return("ID: \t"+self.nombre+"\t"+str(self.tipoDato)+"\tInicializado:"+str(self.inicializado)+ "\t Usado:"+str(self.usado))
