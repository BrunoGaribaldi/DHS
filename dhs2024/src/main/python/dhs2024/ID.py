from enum import Enum

class TipoDato(Enum):
    VOID = "void"
    INT = "int"
    FLOAT = "float"
    BOOLEAN = "bool" 
    DOUBLE = "double"
    CHAR = "char"

class ID():
    def __init__(self, nombre, tipoDato, inicializado, usado):
        self.nombre = nombre
        self.inicializado = inicializado
        self.usado = usado
        self.tipoDato = TipoDato(tipoDato)

    def __str__(self):
        return("ID: \t"+self.nombre+"\t"+str(self.tipoDato)+"\tInicializado:"+str(self.inicializado)+ "\t Usado:"+str(self.usado))


