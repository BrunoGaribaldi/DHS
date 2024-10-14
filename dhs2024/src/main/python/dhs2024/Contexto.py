from ID import Funcion, Variable, TipoDato, ID

class Contexto():
    #funcion1 = Funcion('func' , TipoDatoFuncion.INT.name, True , True, [1,2,3])
    #print(funcion1.__getattribute__('argumentos'))
    tabla = dict()
    def __init__(self): 
        self.tabla = {}
    
