from antlr4 import TerminalNode
from compiladoresListener import compiladoresListener
from compiladoresParser import compiladoresParser
from TablaSimbolos import TablaSimbolos
from Contexto import Contexto
from ID import ID,TipoDato
from Funcion import Funcion
from Variable import Variable


class Escucha (compiladoresListener) :

    tablaDeSimbolos = TablaSimbolos()

    def argumentosALista (self, argumentos):
        lista = argumentos.split(',')
        listaArgumentos = list()
        for args in lista: 
            if args.startswith('int'):
                tipo = TipoDato.INT
                nom = args[3:]
            elif args.startswith('float'):
                tipo = TipoDato.FLOAT
                nom = args[5:]
            elif args.startswith('double'):
                tipo = TipoDato.DOUBLE
                nom = args[6:]
            elif args.startswith('char'):
                tipo = TipoDato.CHAR
                nom = args[4:]
            elif args.startswith('bool'):
                tipo = TipoDato.BOOLEAN
                nom = args[4:]
            listaArgumentos.append((nom,tipo))

        vistos = set()
        repetidos = set()
        for tupla in listaArgumentos:
            elemento = tupla[0] 
        if elemento in vistos:
            repetidos.add(elemento)  # Si ya está en 'vistos', agregarlo a 'repetidos'
        else:
            vistos.add(elemento)  # Si no está en 'vistos', agregarlo
        if len(repetidos) == 0: #todo ok no hay argumentos repetidos
            return listaArgumentos

    def tipoDatoAEnum (self, tipoDato):
        if tipoDato == 'int':
            return TipoDato.INT
        elif tipoDato == 'void':
            return TipoDato.VOID
        elif tipoDato == 'float':
            return TipoDato.FLOAT
        elif tipoDato == 'bool':
            return TipoDato.BOOLEAN
        elif tipoDato == 'char':
            return TipoDato.CHAR
        elif tipoDato == 'double':
            return TipoDato.DOUBLE

    def enterPrototipofunc(self, ctx: compiladoresParser.PrototipofuncContext):
        print('#### Prototipo de funcion')
    
    def exitPrototipofunc(self, ctx: compiladoresParser.PrototipofuncContext):
        nombreFuncion = ctx.getChild(1).getText()
        print("\n Nombre de la funcion: " + nombreFuncion)
        busquedaglobal = self.tablaDeSimbolos.buscarGlobal(nombreFuncion)
        if(busquedaglobal != 1):
            tipoDeDato =  ctx.getChild(0).getText()
            argumentos = ctx.getChild(3).getText()
            listaArgumentos = self.argumentosALista(argumentos)
            if listaArgumentos != 1:
                print("lista argumentos")
                for l in listaArgumentos:
                    print(l)
                    self.tablaDeSimbolos.addIdentificador(nombreFuncion,tipoDeDato,1,listaArgumentos)#pongo 1 xq es funcion
                print("\n Agregado!")
        else:
            print("Ya tenes declarada una funcion con ese nombre")

    def enterFunc(self, ctx: compiladoresParser.FuncContext):
        print("!!!!!!Funcion")
        contexto = Contexto()
        self.tablaDeSimbolos.addContexto(contexto)
   
    def exitFunc(self, ctx: compiladoresParser.FuncContext):
        nombreFuncion = ctx.getChild(1).getText()
        buscarGlobal = self.tablaDeSimbolos.buscarGlobal(nombreFuncion)
        if buscarGlobal == 1: #yo necesito que en el contexto global exista la funcion declarada
            print("La funcion esta en uso")
            tipodeDato = ctx.getChild(0).getText()
            tipodeDato = self.tipoDatoAEnum(tipodeDato)
            args = ctx.getChild(3).getText()
            IDfunc = self.tablaDeSimbolos.getGlobal(nombreFuncion)
            IDfunc.setUsado()
            print(IDfunc.__getattribute__("usado"))
            if IDfunc.__getattribute__("tipoDato") != tipodeDato or IDfunc.__getattribute__("argumentos") != self.argumentosALista(args):
                print("los argumentos que tenemos en la declaracion no son los mismos q que los que tenemos en la definicion o el tipo de dato es distinto")
                self.tablaDeSimbolos.delContexto()
        else: 
            print("Estas queriendo definir una funcion que no declaraste")
  # def enterBloque(self, ctx:compiladoresParser.BloqueContext): # Entro a contexto
    #     contexto= Contexto()
    #     self.tablaDeSimbolos.addContexto(contexto)

    # def exitBloque(self, ctx:compiladoresParser.BloqueContext):# Salgo de contexto
    #     print("Simbolos de este contexto:")
    #     self.tablaDeSimbolos.contextos[-1].imprimirTabla()
    #     print("=" *20 + "\n")
    #     self.tablaDeSimbolos.delContexto()

    # def enterDeclaracion(self, ctx:compiladoresParser.DeclaracionContext):
    #    print('#### declaracion')

    # def exitDeclaracion(self, ctx:compiladoresParser.DeclaracionContext):
    #     tipoDeDato= ctx.getChild(0).getText()
    #     nombreVariable= ctx.getChild(1).getText()
    #     busquedaglobal = self.tablaDeSimbolos.buscarGlobal(nombreVariable)
    #     busquedalocal = self.tablaDeSimbolos.buscarLocal(nombreVariable)
    #     if(busquedaglobal != 1 and busquedalocal != 1): #acordate que 1 era si se podia usar global
    #         self.tablaDeSimbolos.addIdentificador(nombreVariable,tipoDeDato)
    #     else: 
    #         if (busquedaglobal == 1):
    #             print('esta siendo usada globalmente')
    #         if (busquedalocal == 1):
    #             print('esta siendo usada globalmente')




