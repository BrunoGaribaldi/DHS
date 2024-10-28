from typing import Any
from ID import ID
from ID import TipoDato

class Funcion(ID):

    args = list()


    def __init__(self, nombre, tipoDato, inicializado, usado,argumentos: list):
        super().__init__(nombre, tipoDato, inicializado, usado)
        self.argumentos = argumentos
        self.tipo = "funcion"


    def __getattribute__(self, name: str) -> Any:
        return super().__getattribute__(name)

    def setInicializado(self):
        return super().setInicializado()
    
    def setUsado(self):
        return super().setUsado()