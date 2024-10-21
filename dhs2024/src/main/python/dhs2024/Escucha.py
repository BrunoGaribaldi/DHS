from antlr4 import TerminalNode
from compiladoresListener import compiladoresListener
from compiladoresParser import compiladoresParser
from TablaSimbolos import TablaSimbolos
from Contexto import Contexto
from ID import ID

class Escucha (compiladoresListener) :

    tablaDeSimbolos = TablaSimbolos()

    def enterBloque(self, ctx:compiladoresParser.BloqueContext): # Entro a contexto
        contexto= Contexto()
        self.tablaDeSimbolos.addContexto(contexto)

    def exitBloque(self, ctx:compiladoresParser.BloqueContext):# Salgo de contexto
        print("Simbolos de este contexto:")
        self.tablaDeSimbolos.contextos[-1].imprimirTabla()
        print("=" *20 + "\n")
        self.tablaDeSimbolos.delContexto()

    def enterDeclaracion(self, ctx:compiladoresParser.DeclaracionContext):
        print('#### declaracion')

    def exitDeclaracion(self, ctx:compiladoresParser.DeclaracionContext):
        tipoDeDato= ctx.getChild(0).getText()
        nombreVariable= ctx.getChild(1).getText()
        busquedaglobal = self.tablaDeSimbolos.buscarGlobal(nombreVariable)
        busquedalocal = self.tablaDeSimbolos.buscarLocal(nombreVariable)
        if(busquedaglobal != 1 and busquedalocal != 1): #acordate que 1 era si se podia usar global
            self.tablaDeSimbolos.addIdentificador(nombreVariable,tipoDeDato)
        else: 
            if (busquedaglobal == 1):
                print('esta siendo usada globalmente')
            if (busquedalocal == 1):
                print('esta siendo usada globalmente')

    def enterPrototipofunc(self, ctx: compiladoresParser.PrototipofuncContext):
        print('#### Prototipo de funcion')
    
    def exitPrototipofunc(self, ctx: compiladoresParser.PrototipofuncContext):
        tipoDeDato =  ctx.getChild(0).getText()
        nombreFuncion = ctx.getChild(1).getText()
        argumentos = ctx.getChild(3).getText()
        lista = argumentos.split(',')
        listaargumentos = list()
        for args in lista: 
            if args.startswith('int'):
                tipo = 'int'
                nom = args[3:]
            elif args.startswith('float'):
                tipo = 'float'
                nom = args[5:]
            elif args.startswith('double'):
                tipo = 'double'
                nom = args[6:]
            elif args.startswith('char'):
                tipo = 'char'
                nom = args[4:]
            elif args.startswith('bool'):
                tipo = 'boolean'
                nom = args[4:]
            listaargumentos.append((nom,tipo))

            vistos = set()
            repetidos = set()
            for tupla in listaargumentos:
                elemento = tupla[0] 
                if elemento in vistos:
                    repetidos.add(elemento)  # Si ya está en 'vistos', agregarlo a 'repetidos'
                else:
                    vistos.add(elemento)  # Si no está en 'vistos', agregarlo
            if len(repetidos) == 0:
                print ('todo ok no hay variables repetidos')
            busquedaglobal = self.tablaDeSimbolos.buscarGlobal(nombreFuncion)
            if(busquedaglobal != 1):
                self.tablaDeSimbolos.addIdentificador(nombreFuncion,tipoDeDato,0,listaargumentos)

        #busquedaglobal = self.tablaDeSimbolos.buscarGlobal(nombreFuncion)





