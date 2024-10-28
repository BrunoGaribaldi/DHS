from Contexto import Contexto
from ID import ID
from Variable import Variable
from Funcion import Funcion
class TablaSimbolos():

    contextos = list()

    def __init__(self):
        contextoGlobal = Contexto()
        self.contextos.append(contextoGlobal)

    def addContexto(self,contexto):
        self.contextos.append(contexto)
    
    def delContexto(self): 
        self.contextos.pop()

    def addIdentificador(self,nombre,tipoDato,tipoID,argumentos): #tipo ID es cero entonces es variable
        contexto = self.contextos[-1]
        if(tipoID == 0): #variable
            id = Variable(nombre,tipoDato,1,0)
        else:            #funcion
            id = Funcion(nombre,tipoDato,0,0,argumentos)

        contexto.tabla.update({nombre:id})
    
    def buscarLocal(self,nombre): #si no lo encuentra retorna none, sino retorna el objeto, 
        return self.contextos[-1].traerVariable(nombre)
    
    def buscarGlobal(self, nombre): #retorna 0 si no existe, objeto si si
        self.contextos[0].traerVariable(nombre)
  
