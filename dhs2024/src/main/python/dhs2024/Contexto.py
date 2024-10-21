from ID import TipoDato, ID
from Funcion import Funcion
from Variable import Variable

class Contexto():
    #funcion1 = Funcion('func' , TipoDatoFuncion.INT.name, True , True, [1,2,3])
    #print(funcion1.__getattribute__('argumentos'))
    tabla = dict()


    def __init__(self): 
        self.tabla = {}
    
    def traerVariable(self,nombre):
         if nombre in self.tabla:
              return nombre
         
         else:
              return None
         
    def traerID(self,nombre):
        if self.traerVariable != None:
            return self.tabla.get(nombre) 
    


    def imprimirTabla(self):
        print(self.tabla)