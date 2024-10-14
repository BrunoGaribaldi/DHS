from enum import Enum

class TipoDato(Enum):
    VOID = 0
    INT = 1
    FLOAT = 2
    BOOLEAN = 3 
    DOUBLE = 4
    CHAR = 5

class ID():
    def __init__(self, nombre, tipoDato: TipoDato, inicializado, usado):
        self.nombre = nombre
        self.tipoDato = tipoDato
        self.inicializado = inicializado
        self.usado = usado

class Funcion(ID):
    def __init__(self, nombre, tipoDato: TipoDato, inicializado, usado,argumentos: list):
        super().__init__(nombre, tipoDato, inicializado, usado)
        self.argumentos = argumentos

class Variable(ID):
    def __init__(self, nombre, tipoDato: TipoDato, inicializado, usado):
        super().__init__(nombre, tipoDato, inicializado, usado)
