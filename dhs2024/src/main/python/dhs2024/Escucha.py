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

#funciones ----------------------------------------------------------------------------------------------

    #para los argumentos necesitamos que haya una lista auxiliar donde ir agregandolos antes de iniciar el bloque de la funcion
    auxArgumentos = []
    auxArgumentosf = []
    aux = []
    auxNombreFuncion = ''
    banderaf = False
    banderap = False
    b = False

    #lista de ID inicializados pero sin ser usados
    idNoUsadosInicializados = []

# main --------------------------------------------------------------------------------------------------
    #def exitFmain(self, ctx: compiladoresParser.FmainContext):
     #   print("Funcion main")

#prototipo de funciones ----------------------------------------------------------------------------------------------
    def enterPrototipofunc(self, ctx: compiladoresParser.PrototipofuncContext):
        print('\n#### Prototipo de funcion')
        self.banderap = False
    
    def exitDeclargumentos(self, ctx:compiladoresParser.DeclaracionContext):
        if(self.banderap == False):
            tipoDeDato= ctx.getChild(0).getText()
            nombreVariable= ctx.getChild(1).getText()
            if (len(self.auxArgumentos) != 0):
                for i in self.auxArgumentos:
                    if i.nombre == nombreVariable:
                        print("-->ERROR SEMANTICO: Estas definiendo argumentos con el mismo nombre")
                        self.banderap = True
                        self.auxArgumentos.clear()
                        return
                #creamos esa variable para guardarla en la lista de argumentos
                argumento = Variable(nombreVariable,tipoDeDato,0,0)
                self.auxArgumentos.append(argumento)
            else: 
                argumento = Variable(nombreVariable,tipoDeDato,0,0)
                self.auxArgumentos.append(argumento)

    def exitPrototipofunc(self, ctx: compiladoresParser.PrototipofuncContext):
         if (self.banderap == False):
            nombreFuncion = ctx.getChild(1).getText()
            argumentos = self.auxArgumentos[:]

            #ya almacenamos la lista de argumentso, vaciamos la lista auxiliar
            self.auxArgumentos.clear()
            #print("Nombre de la funcion: " + nombreFuncion)

            if nombreFuncion == "main":
                print("ERROR: No declaramos main")
                return
            
            #buscamos si este nombre no le corresponde un ID
            busquedaGlobal = self.tablaDeSimbolos.buscarGlobal(nombreFuncion)
            if(busquedaGlobal == None):
                tipoDeDato =  ctx.getChild(0).getText()
                self.tablaDeSimbolos.addIdentificador(nombreFuncion,tipoDeDato,1,argumentos)#pongo 1 xq es funcion
                print("\nPrototipo de funcion '" +nombreFuncion + "' guardado con exito")
                
            else:
                print("-->ERROR SEMANTICO: Ya existe el prototipo de funcion con el nombre "+ nombreFuncion + "!")
    
# definicion de funciones y bloque ------------------------------------------------------------------------------------------------------------    
    def enterFunc(self, ctx: compiladoresParser.FuncContext):
        #en las funciones creamos el contexto al definirlas, para poder agregar sus argumentos al contexto
        print("\nInicializacion funcion")
        self.banderaf = False

    def exitNombrefuncion(self, ctx: compiladoresParser.NombrefuncionContext):
        #aca ya se el nombre de la funcion entonces lo uso para buscar sus argumentos
        funcion = self.tablaDeSimbolos.buscarGlobal(str(ctx.ID()))
        if funcion == None:
            print("ERROR: No existe el prototipo de la funcion " + ctx.ID().getText())
            self.banderaf = True
        else: 
            self.auxArgumentosf.clear()
            self.auxNombreFuncion = ctx.ID().getText()

    def exitFuncargumentos(self, ctx: compiladoresParser.FuncargumentosContext):
        if (self.banderaf == True):
            return 
        else:
            tipoDeDato= ctx.getChild(0).getText()
            nombreVariable= ctx.getChild(1).getText()
            #creamos esa variable para guardarla en la lista de argumentos
            argumento = Variable(nombreVariable,tipoDeDato,0,0)
            self.auxArgumentosf.append(argumento)
      
    def enterBloqueespecial(self, ctx:compiladoresParser.BloqueContext):
        print('\n***Entre a un CONTEXTO***')
        funcion = self.tablaDeSimbolos.buscarGlobal(self.auxNombreFuncion)
        argumentos = funcion.argumentos
        comp = True
        if (len(argumentos) == len(self.auxArgumentosf) and len(argumentos) != 0):
            i = 0
            while i<len(argumentos) and comp == True:
                if(not (argumentos[i].nombre == self.auxArgumentosf[i].nombre and
                   argumentos[i].tipoDato == self.auxArgumentosf[i].tipoDato)):
                    comp = False
                    print("-->ERROR SEMANTICO: Argumento de la funcion '" + self.auxNombreFuncion + "' no coincide con prototipo")
                    self.banderaf = True 
                    return 
                i += 1       
            print("Funcion '" + self.auxNombreFuncion + "' inicializada con exito")
            funcion.inicializado = 1
            contextoInicializado = Contexto(argumentos)
            self.tablaDeSimbolos.addContexto(contextoInicializado)   
        elif (len(argumentos) == 0):
            print("Funcion '" + self.auxNombreFuncion + "' inicializada con exito")
            funcion.inicializado = 1
            contextoInicializado = Contexto(argumentos)
            self.tablaDeSimbolos.addContexto(contextoInicializado)
        else:
            print("-->ERROR SEMANTICO: Revisar la cantidad de argumentos")

    def exitBloqueespecial(self, ctx:compiladoresParser.BloqueContext):
        if (self.banderaf == True):
            return 
        print('***Sali de un CONTEXTO de funcion***')
        #print('Cantidad de hijos: '+ str(ctx.getChildCount()))
        #print('TOQUENS: '+ ctx.getText())
        print("*" * 50 )

        #buscamos ids que hayan sido inicializados pero no usados
        #recorremos el contexto del cual vamos a salir
        for id in self.tablaDeSimbolos.contextos[-1].tabla:
            variable = self.tablaDeSimbolos.contextos[-1].traerVariable(id)

        #agregamos a la lista de variables no
            if variable.inicializado==1 and variable.usado==0:
                self.idNoUsadosInicializados.append(variable)

        print("En este contexto se encontro lo siguiente:")
        self.tablaDeSimbolos.contextos[-1].imprimirTabla()
        print("*" * 50 + "\n")
        self.tablaDeSimbolos.delContexto()

# llamada a funcion ---------------------------------------------------------------------------------
    def enterLlamadafunc(self, ctx: compiladoresParser.LlamadafuncContext):
        print("Llamada a funcion")
        self.aux.clear()
        self.b = False

    def exitNombre(self, ctx: compiladoresParser.NombreContext):
        nombre = ctx.getChild(0).getText()
        funcion = self.tablaDeSimbolos.buscarGlobal(nombre)
        if (funcion == None):
            print("-->ERROR SEMANTICO: No existe el prototitpo de la funcion '" + nombre + "'")
            self.b = True
        
    def exitLlamargumentos(self, ctx: compiladoresParser.LlamargumentosContext):
        id = ctx.getChild(0).getText()
        self.aux.append(id)

    def exitLlamadafunc(self, ctx: compiladoresParser.LlamadafuncContext):
        if self.b == False: 
            funcion = self.tablaDeSimbolos.buscarGlobal(ctx.getChild(0).getText())
            argumentosf = funcion.argumentos
            
            if len(argumentosf) == len(self.aux):
                counter = 0
                for i in self.aux:
                    local = self.tablaDeSimbolos.buscarLocal(i)
                    idf = argumentosf[counter]
                    tdf = idf.tipoDato
                    counter += 1
                    if local == None:
                        gobal = self.tablaDeSimbolos.buscarGlobal(i)
                        if gobal == None:
                            print("-->ERROR SEMANTICO: Estas queriendo pasar como argumento un ID no declarado")
                            self.b = True
                            break
                        else:
                            tipodedato = gobal.tipoDato
                            if(tipodedato != tdf): 
                                print("-->ERROR SEMANTICO: Estas queriendo pasar un " + str(tipodedato) + " cuando la funcion recibe un " + str(tdf))
                                self.b = True
                                break
                    else:        
                        tipodedato = local.tipoDato
                        if(tipodedato != tdf): 
                                print("-->ERROR SEMANTICO: Estas queriendo pasar un " + str(tipodedato) + " cuando la funcion recibe un " + str(tdf))
                                self.b = True
                                break
            else: 
                print("-->ERROR SEMANTICO: Estas pasando mas o menos argumentos de los debidos.")
                self.b = True

            if self.b == True:
                return
            else: 
                funcion.usado = 1
                print("LLamada a funcion '" + ctx.getChild(0).getText() + "' realizada con exito")

# for -----------------------------------------------------------------------------------------------
    def enterIfor(self, ctx: compiladoresParser.IforContext):
        print("\nSe detecto un bloque FOR")
    #iniciacion en el for

    def exitInit(self, ctx: compiladoresParser.InitContext):
        nombreVariable= ctx.getChild(1).getText()
        tipoDato= ctx.getChild(0).getText()
        variableInit = Variable(nombreVariable,tipoDato,1,0)
        #por como esta definido la iniciacion de un contexto, el primer argumento es si son lista de  args de funcion
        # su segundo argumento esta destinado a una sola variable
        contextoInicializado = Contexto(None, variableInit)
        self.tablaDeSimbolos.addContexto(contextoInicializado)
        print("Se agrego la variable '" + nombreVariable + "'al contexto del bloque FOR")

    #bloques de for
    def enterBloquefor(self, ctx: compiladoresParser.BloqueforContext):
        print('\n***Entre a un CONTEXTO FOR***')

    def exitBloquefor(self, ctx:compiladoresParser.BloqueforContext):
        print('***Sali de un CONTEXTO***')
        #print('Cantidad de hijos: '+ str(ctx.getChildCount()))
        #print('TOQUENS: '+ ctx.getText())
        print("*" * 50 )

        #buscamos ids que hayan sido inicializados pero no usados
        #recorremos el contexto del cual vamos a salir
        for id in self.tablaDeSimbolos.contextos[-1].tabla:
            variable = self.tablaDeSimbolos.contextos[-1].traerVariable(id)

        #agregamos a la lista de variables no
            if variable.inicializado==1 and variable.usado==0:
                self.idNoUsadosInicializados.append(variable)

        print("En este contexto se encontro lo siguiente:")
        self.tablaDeSimbolos.contextos[-1].imprimirTabla()
        print("*" * 50 + "\n")
        self.tablaDeSimbolos.delContexto()

#---------------------------------------------------------------------------------------------------------
    def enterBloque(self, ctx:compiladoresParser.BloqueContext):
        print('\n***Entre a un CONTEXTO***')
        contexto= Contexto()
        self.tablaDeSimbolos.addContexto(contexto)
        
    def exitBloque(self, ctx:compiladoresParser.BloqueContext):
        print('***Sali de un CONTEXTO***')
        #print('Cantidad de hijos: '+ str(ctx.getChildCount()))
        #print('TOQUENS: '+ ctx.getText())
        print("*" * 50 )
        print("En este contexto se encontro lo siguiente:")

        #buscamos ids que hayan sido inicializados pero no usados
        #recorremos el contexto del cual vamos a salir
        for id in self.tablaDeSimbolos.contextos[-1].tabla:
            variable = self.tablaDeSimbolos.contextos[-1].traerVariable(id)

        #agregamos a la lista de variables no
            if variable.inicializado==1 and variable.usado==0:
                self.idNoUsadosInicializados.append(variable)

        self.tablaDeSimbolos.contextos[-1].imprimirTabla()
        print("*" * 50 + "\n")
        self.tablaDeSimbolos.delContexto()

    def enterDeclaracion(self, ctx: compiladoresParser.DeclaracionContext):
        print("@@@ Declaracion")
    
    def exitDeclaracion(self, ctx:compiladoresParser.DeclaracionContext):
        tipoDeDato= ctx.getChild(0).getText()
        nombreVariable= ctx.getChild(1).getText()
    
        busquedaGlobal = self.tablaDeSimbolos.buscarGlobal(nombreVariable)
        busquedaLocal = self.tablaDeSimbolos.buscarLocal(nombreVariable)
    
        if busquedaGlobal == None and busquedaLocal == None :
            print("El nombre '" + nombreVariable +"' esta muy fachero, lo puedes usar")
            self.tablaDeSimbolos.addIdentificador(nombreVariable,tipoDeDato,0,None)

        else : 
            if busquedaGlobal != None :
                print("-->ERROR SEMANTICO: La variable '" + nombreVariable + "' ya fue declarada en el contexto global \n")

            else:
                print("-->ERROR SEMANTICO: La variable '" + nombreVariable + "' ya fue declarada en el contexto local \n")    

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
                print("-->ERROR SEMANTICO: Se desconoce el valor de '" + nombreVariable + "', debes declararlo primero !\n")
            else :
                print("Se inicializo la variable '" + nombreVariable +"'")
                busquedaGlobal.inicializado = 1

        else :
            #la encontro en el contexto global 
            print("Se inicializo la variable '" + nombreVariable +"'")
            busquedaLocal.inicializado = 1
                             
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
                if busquedaLocal.usado == 0:
                    busquedaLocal.usado = 1 
                    print(factorUsado.getText() + " ha sido  marcado como usado")

                if busquedaLocal.inicializado == 0 :
                    #marco a mi nombre de variable como usado
                    print("-->ERROR SEMANTICO: Estas queriendo usar una variable la cual no conozco el valor, debes inicializarla primero !")
            else : 
                #la busco global
                #print("La variable no existe localmente, la buscamos en el contexto global")
                busquedaGlobal = self.tablaDeSimbolos.buscarGlobal(factorUsado.getText())

                if busquedaGlobal != None :
                        #las encontre glbalmente
                        if busquedaGlobal.usado == 0:
                            busquedaGlobal.usado = 1
                            print(factorUsado.getText() + " ha sido  marcado como usado")

                        if busquedaGlobal.inicializado != 1 :
                            #variable no inicializada
                            print("-->ERROR SEMANTICO: Estas queriendo usar una variable la cual no conozco el valor, debes inicializarla primero !")
                else :
                    #no encontro por ningun lado
                    print("ERROR SEMANTICO: La variable " + factorUsado.getText() + " no fue declarada!")

    def exitPrograma(self, ctx:compiladoresParser.ProgramaContext):
        #
        print('Fin compilacion\n')
        print("*" * 50 )

        #buscamos ids que hayan sido inicializados pero no usados
        #recorremos el contexto del cual vamos a salir
        for id in self.tablaDeSimbolos.contextos[-1].tabla:
            variable = self.tablaDeSimbolos.contextos[-1].traerVariable(id)

        #agregamos a la lista de variables no
            if variable.inicializado==1 and variable.usado==0:
                self.idNoUsadosInicializados.append(variable)

        print("En el contexto global se encontro lo siguiente:")
        self.tablaDeSimbolos.contextos[-1].imprimirTabla()
        print("*" * 50 + "\n")
        print("-**-" * 25 + "\n")
        print("Identificadores inicializadas pero no usados:")
        for id in self.idNoUsadosInicializados:
            print(id)


