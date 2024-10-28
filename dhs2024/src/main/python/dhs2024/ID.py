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


