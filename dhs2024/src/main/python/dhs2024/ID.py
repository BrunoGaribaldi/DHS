from enum import Enum

class TipoDato(Enum):
    VOID = 0
    INT = 1
    FLOAT = 2
    BOOLEAN = 3 
    DOUBLE = 4
    CHAR = 5

class ID():
    def __init__(self, nombre, tipoDato, inicializado, usado):
        self.nombre = nombre
        self.inicializado = inicializado
        self.usado = usado
        if tipoDato == 'int':
            self.tipoDato = TipoDato.INT
        elif tipoDato == 'void':
            self.tipoDato = TipoDato.VOID
        elif tipoDato == 'float':
            self.tipoDato = TipoDato.FLOAT
        elif tipoDato == 'bool':
            self.tipoDato = TipoDato.BOOLEAN
        elif tipoDato == 'char':
            self.tipoDato = TipoDato.CHAR
        elif tipoDato == 'double':
            self.tipoDato = TipoDato.DOUBLE

    def setUsado(self):
        self.usado = 1