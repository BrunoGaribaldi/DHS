from Contexto import Contexto
from ID import ID
from Variable import Variable
from Funcion import Funcion
class TablaSimbolos(object):

    #para hacerla SINGLETON
    __instance= None
     
    contextos=[]   
    

    #para hacerla SINGLETON
    def __new__(cls):
        if TablaSimbolos.__instance is None:
            TablaSimbolos.__instance = object.__new__(cls)
        return TablaSimbolos.__instance
    
    def __init__(self) :
        contextoGlobal= Contexto()
        self.contextos.append(contextoGlobal)

    def addContexto(self,contexto):
        self.contextos.append(contexto) 

    def delContexto(self):
        self.contextos.pop()

    def addIdentificador(self,nombre,tipoDato,tipoID,argumentos):
        contexto=self.contextos[-1]
        if(tipoID == 0): #variable
            id = Variable(nombre,tipoDato,0,0)
        else:            #funcion
            id = Funcion(nombre,tipoDato,0,0,argumentos)
                    
        contexto.tabla.update({nombre:id})


    def buscarLocal(self, nombre):
        return self.contextos[-1].traerVariable(nombre)
        
    
    def buscarGlobal(self, nombre):
        return self.contextos[0].traerVariable(nombre)
    
    #en ocasiones solo quiero buscar el identificador, sin saber donde esta
    def buscarGeneral(self,nombre):
        resultadoLocal = self.buscarLocal(nombre)

        if resultadoLocal != None:
            return resultadoLocal
        else:
            if self.buscarGlobal(nombre) != None:
                return self.buscarGlobal(nombre)
            else :
                #no lo encontro en ningun lado:
                return None
        
    

