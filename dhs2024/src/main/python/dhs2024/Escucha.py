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
    
    # def argumentosALista (self, argumentos):
    #     lista = list()
    #     if not argumentos: #la cadena esta vacia, no tiene argumentos
    #         return lista
    #     else:
    #         lista = argumentos.split(',')
    #         listaArgumentos = list()
    #         for args in lista: 
    #             if args.startswith('int'):
    #                 tipo = TipoDato.INT
    #                 nom = args[3:]
    #             elif args.startswith('float'):
    #                 tipo = TipoDato.FLOAT
    #                 nom = args[5:]
    #             elif args.startswith('double'):
    #                 tipo = TipoDato.DOUBLE
    #                 nom = args[6:]
    #             elif args.startswith('char'):
    #                 tipo = TipoDato.CHAR
    #                 nom = args[4:]
    #             elif args.startswith('bool'):
    #                 tipo = TipoDato.BOOLEAN
    #                 nom = args[4:]
    #             listaArgumentos.append((nom,tipo))

    #         vistos = set()
    #         repetidos = set()
    #         for tupla in listaArgumentos:
    #             elemento = tupla[0] 
    #             if elemento in vistos:
    #                 repetidos.add(elemento)  # Si ya está en 'vistos', agregarlo a 'repetidos'
    #             else:
    #                 vistos.add(elemento)  # Si no está en 'vistos', agregarlo
    #         if len(repetidos) == 0: #todo ok no hay argumentos repetidos
    #             return listaArgumentos
    #         else:
    #             print("tenes las siguientes variables repetidas: " + str(repetidos))
    #             return None

    # def tipoDatoAEnum (self, tipoDato):
    #     if tipoDato == 'int':
    #         return TipoDato.INT
    #     elif tipoDato == 'void':
    #         return TipoDato.VOID
    #     elif tipoDato == 'float':
    #         return TipoDato.FLOAT
    #     elif tipoDato == 'bool':
    #         return TipoDato.BOOLEAN
    #     elif tipoDato == 'char':
    #         return TipoDato.CHAR
    #     elif tipoDato == 'double':
    #         return TipoDato.DOUBLE

    # def enterPrototipofunc(self, ctx: compiladoresParser.PrototipofuncContext):
    #     print('#### Prototipo de funcion')
    
    # def exitPrototipofunc(self, ctx: compiladoresParser.PrototipofuncContext):
    #     nombreFuncion = ctx.getChild(1).getText()
    #     print("\n Nombre de la funcion: " + nombreFuncion)
    #     if nombreFuncion == "main":
    #         print("no declaramos main")
    #         return
    #     busquedaglobal = self.tablaDeSimbolos.buscarGlobal(nombreFuncion)
    #     if(busquedaglobal != 1):
    #         tipoDeDato =  ctx.getChild(0).getText()
    #         argumentos = ctx.getChild(3).getText()
    #         listaArgumentos = self.argumentosALista(argumentos)

    #         if listaArgumentos == None:
    #             print("No podemos agregar la funcion.")
    #             return
    #         elif len(listaArgumentos) != 0:
    #             print("lista argumentos")
    #             for l in listaArgumentos:
    #                 print(l)
    #         else: 
    #             print("Lista de argumentos vacia")  
                
    #         self.tablaDeSimbolos.addIdentificador(nombreFuncion,tipoDeDato,1,listaArgumentos)#pongo 1 xq es funcion
    #         print("\n Agregado!")
    #     else:
    #         print("Ya tenes declarada una funcion con ese nombre")

    # def enterFunc(self, ctx: compiladoresParser.FuncContext):
    #     print("!!!!!!Funcion")
    #     contexto = Contexto()
    #     self.tablaDeSimbolos.addContexto(contexto)
   
    # def exitFunc(self, ctx: compiladoresParser.FuncContext):
    #     nombreFuncion = ctx.getChild(1).getText()
    #     if nombreFuncion == "main": 
    #         print('ver que hacer con MAIN')
    #     buscarGlobal = self.tablaDeSimbolos.buscarGlobal(nombreFuncion)
    #     if buscarGlobal == 1: #yo necesito que en el contexto global exista la funcion declarada
    #         print("La funcion esta en uso")
    #         tipodeDato = ctx.getChild(0).getText()
    #         tipodeDato = self.tipoDatoAEnum(tipodeDato)
    #         args = ctx.getChild(3).getText()
    #         IDfunc = self.tablaDeSimbolos.getGlobal(nombreFuncion)
    #         IDfunc.setInicializado()
    #         print("Inicializado: " + str(IDfunc.__getattribute__("inicializado")))#mostramos que esta en 1
    #         if IDfunc.__getattribute__("tipoDato") != tipodeDato or IDfunc.__getattribute__("argumentos") != self.argumentosALista(args):
    #             print("los argumentos que tenemos en la declaracion no son los mismos q que los que tenemos en la definicion o el tipo de dato es distinto")
    #             self.tablaDeSimbolos.delContexto()
    #     else: 
    #         print("Estas queriendo definir una funcion que no declaraste")

    # def exitNombre(self, ctx: compiladoresParser.NombreContext):
    #     print
    
    # def exitArgumentos(self, ctx: compiladoresParser.ArgumentosContext):
       # print()
    
    def enterBloque(self, ctx:compiladoresParser.BloqueContext):
        print('***Entre a un CONTEXTO***')
        contexto= Contexto()
        self.tablaDeSimbolos.addContexto(contexto)
        
    def exitBloque(self, ctx:compiladoresParser.BloqueContext):
        print('***Sali de un CONTEXTO***')
        #print('Cantidad de hijos: '+ str(ctx.getChildCount()))
        #print('TOQUENS: '+ ctx.getText())
        print("*" * 50 )
        print("En este contexto se encontro lo siguiente:")
        self.tablaDeSimbolos.contextos[-1].imprimirTabla()
        print("*" * 50 + "\n")
        self.tablaDeSimbolos.delContexto()

    def enterDeclaracion(self, ctx: compiladoresParser.DeclaracionContext):
        print("@@@ declaracion")
    
    def exitDeclaracion(self, ctx:compiladoresParser.DeclaracionContext):
        tipoDeDato= ctx.getChild(0).getText()
        nombreVariable= ctx.getChild(1).getText()
    
        busquedaGlobal = self.tablaDeSimbolos.buscarGlobal(nombreVariable)
        busquedaLocal = self.tablaDeSimbolos.buscarLocal(nombreVariable)
    
        if busquedaGlobal == None and busquedaLocal == None :
            print('"'+nombreVariable+'"'+"Puede utilizar ese nombre de variable")
            self.tablaDeSimbolos.addIdentificador(nombreVariable,tipoDeDato,0,None)

        else : 
            if busquedaGlobal != None :
                print('ERROR: "' + nombreVariable +'"La varibale esta siendo usada globalmente \n')

            else:
                print('ERROR: "' + nombreVariable +'" La varibale esta siendo usada localmete \n')    

    def enterAsignacion(self, ctx: compiladoresParser.AsignacionContext):
        print("\n ### ASIGNACION ###")

    def exitAsignacion(self, ctx: compiladoresParser.AsignacionContext):
        nombreVariable= ctx.getChild(0).getText()
        busquedaLocal = self.tablaDeSimbolos.buscarLocal(nombreVariable)

        #buscamos si la variable fue declarada globalmente
        if busquedaLocal == None :

            #no la encontro entonces la busco localmente
            busquedaGlobal = self.tablaDeSimbolos.buscarGlobal(nombreVariable)

            if busquedaGlobal == None :
                #entonces no la encontro en ningun lado
                print("ERROR:" + nombreVariable + " tenes que declararla primero !\n")
            else :
                print("La variable esta inicializada globalmente '" + nombreVariable +"'")
                busquedaLocal.inicializado = 1

        else :
            #la encontro en el contexto global 
            print("La variable esta incializada localmente '" + nombreVariable +"'")
            busquedaGlobal.inicializado = 1           
                     
    def exitFactor(self, ctx: compiladoresParser.FactorContext):
        #factores pueden tener 3 valores : numero - ID - (opal)
        #al hacer ctx.ID() solo traes ID , son los que me interesan para marcar su uso
        factorUsado = ctx.ID()
        if factorUsado != None :
            #significa que ingrese un identificador
            busquedaLocal = self.tablaDeSimbolos.buscarLocal(factorUsado.getText())

            if busquedaLocal != None :
                #encontre el identificador de variable localmente
                #tengo que asegurarme si esta variable ya fue inicializada!
                busquedaLocal.usado = 1 
                print(factorUsado.getText() + " ha sido  marcado como usado")
                if busquedaLocal.inicializado != 1 :
                    #marco a mi nombre de variable como usado
                    print("WARNING: Estas queriendo usar una variable la cual no conozco el valor, debes inicializarla primero !")
            else : 
                #la busco global
                print("La variable no existe localmente, la buscamos en el contexto global")
                busquedaGlobal = self.tablaDeSimbolos.buscarGlobal(factorUsado.getText())

                if busquedaGlobal != None :
                        #las encontre glbalmente
                        busquedaGlobal.usado = 1
                        print(factorUsado.getText() + " ha sido  marcado como usado")
                        if busquedaGlobal.inicializado != 1 :
                            #variable no inicializada
                            print("WARNING: Estas queriendo usar una variable la cual no conozco el valor, debes inicializarla primero !")
                else :
                    #no encontro por ningun lado
                    print("ERROR: La variable " + factorUsado.getText() + " no fue declarada!")





