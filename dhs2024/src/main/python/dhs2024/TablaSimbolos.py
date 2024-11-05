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

    def addIdentificador(self,nombre,tipoDato,tipoID,argumentos, inicializado = 0):
        contexto=self.contextos[-1]
        if(tipoID == 0): #variable
            id = Variable(nombre,tipoDato,inicializado,0)
        else:            #funcion
            id = Funcion(nombre,tipoDato,0,0,argumentos)
                    
        contexto.tabla.update({nombre:id})


    def buscarLocal(self, nombre):

        #return self.contextos[-1].traerVariable(nombre)
        #arranco a buscar desde el ultimo
        numContexto = len(self.contextos)
        contador = numContexto - 1 
         #si esto da 1 tengo solamente el contexto global
        if numContexto == 1:
            return None
        else:
             #lo recorremos la reves
             #range(start,stop(sin incluir), salto)
            for i in range(contador, 0, -1 ):
                retorno = self.contextos[i].traerVariable(nombre)
                 #encontro algo
                if retorno != None:
                    return retorno
            
            #si llego aca noo retorno nada:
            return None
            
        

    def buscarEnMiContexto(self,nombre):
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
        
    

