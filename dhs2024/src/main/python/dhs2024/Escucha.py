from antlr4 import TerminalNode
from compiladoresListener import compiladoresListener
from compiladoresParser import compiladoresParser
from TablaSimbolos import TablaSimbolos
from Contexto import Contexto
from ID import ID,TipoDato
from Funcion import Funcion
from Variable import Variable


#funcion auxiliar para comprobar tipos de datos
def isint(num):
    try:
        int(num)
        return True
    except ValueError:
        return False

class Escucha (compiladoresListener) :

    tablaDeSimbolos = TablaSimbolos()

#funciones ----------------------------------------------------------------------------------------------

    #algunos auxiliares necesarios
    auxArgumentos = []
    auxArgumentosf = []
    aux = []
    auxNombreFuncion = ''
    banderaf = False
    banderap = False
    b = False
    auxtipoDato = TipoDato("void")
    #lista de ID inicializados pero sin ser usados
    idNoUsadosInicializados = []

# main --------------------------------------------------------------------------------------------------
    #def exitFmain(self, ctx: compiladoresParser.FmainContext):
     #   print("Funcion main")

    def enterPrograma(self, ctx: compiladoresParser.ProgramaContext):
        print("Comienza la compilacion\n")

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
                        print("\n-->ERROR SEMANTICO: Estas definiendo argumentos con el mismo nombre\n")
                        self.banderap = True
                        self.auxArgumentos.clear()
                        return
                #creamos esa variable para guardarla en la lista de argumentos
                argumento = Variable(nombreVariable,tipoDeDato,1,0)
                self.auxArgumentos.append(argumento)
            else: 
                argumento = Variable(nombreVariable,tipoDeDato,1,0)
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
                print("\n-->ERROR SEMANTICO: Ya existe el prototipo de funcion con el nombre "+ nombreFuncion + "!\n")

        #chequeo de sintaxis
        if ctx.PYC() == None:
            print("\n-->ERROR SINTACTICO: Te olvidaste un punto y coma, no te preocupes, suele pasar!\n")
        if ctx.PA() == None:
            print("\n-->ERROR SINTACTICO: Te olvidaste el parentesis de apertura!\n")

    
# definicion de funciones y bloque ------------------------------------------------------------------------------------------------------------    
    def enterFunc(self, ctx: compiladoresParser.FuncContext):
        #en las funciones creamos el contexto al definirlas, para poder agregar sus argumentos al contexto
        print("\nInicializacion funcion")
        self.banderaf = False
    
    def exitNombrefuncion(self, ctx: compiladoresParser.NombrefuncionContext):
        #aca ya se el nombre de la funcion entonces lo uso para buscar sus argumentos
        funcion = self.tablaDeSimbolos.buscarGlobal(str(ctx.ID()))
        if funcion == None:
            print("\n-->ERROR: No existe el prototipo de la funcion " + ctx.ID().getText()+ "\n")
            self.banderaf = True
        else: 
            self.auxArgumentosf.clear()
            self.auxNombreFuncion = ctx.ID().getText()

    def exitTipodatofunc(self, ctx: compiladoresParser.TipodatofuncContext):
        if self.banderaf == False:
            self.auxtipoDato = TipoDato(ctx.getChild(0).getText())

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
        if (self.banderaf == True):
            return
                    
        funcion = self.tablaDeSimbolos.buscarGlobal(self.auxNombreFuncion)
        if (self.auxtipoDato != funcion.tipoDato):
            print("\n-->ERROR: Se esperaba un tipo de dato: " + str(funcion.tipoDato) + " y queres inicializar: " + str(self.auxtipoDato) + "\n")
            self.banderaf == True
            return
        
        print('\n***Contexto funcion***')
        argumentos = funcion.argumentos
        if (len(argumentos) == len(self.auxArgumentosf)):
            if(len(argumentos) != 0):
                i = 0

                while i<len(argumentos): #comprobamos que los argumentos sean lo mismo y esten en el mismo orden
                    if(not (argumentos[i].nombre == self.auxArgumentosf[i].nombre and
                    argumentos[i].tipoDato == self.auxArgumentosf[i].tipoDato)):
                        print("\n-->ERROR SEMANTICO: Argumento de la funcion '" + self.auxNombreFuncion + "' no coincide con prototipo\n")
                        self.banderaf = True 
                        return 
                    i += 1   

                print("Funcion '" + self.auxNombreFuncion + "' inicializada con exito")
                funcion.inicializado = 1
                contextoInicializado = Contexto(argumentos)
                self.tablaDeSimbolos.addContexto(contextoInicializado) 
            else:
                print("Funcion '" + self.auxNombreFuncion + "' inicializada con exito")
                funcion.inicializado = 1
                contextoInicializado = Contexto(argumentos)
                self.tablaDeSimbolos.addContexto(contextoInicializado)    
        else:
            print("-->ERROR SEMANTICO: Revisar la cantidad de argumentos")
            self.banderaf = True

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
            print("\n-->ERROR SEMANTICO: No existe el prototitpo de la funcion '" + nombre + "'\n")
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
                            print("\n-->ERROR SEMANTICO: Estas queriendo pasar como argumento un ID no declarado\n")
                            self.b = True
                            break
                        else:
                            tipodedato = gobal.tipoDato
                            if(tipodedato != tdf): 
                                print("\n-->ERROR SEMANTICO: Estas queriendo pasar un " + str(tipodedato) + " cuando la funcion recibe un " + str(tdf) + "\n")
                                self.b = True
                                break
                            gobal.usado = 1
                    else:        
                        tipodedato = local.tipoDato
                        if(tipodedato != tdf): 
                                print("\n-->ERROR SEMANTICO: Estas queriendo pasar un " + str(tipodedato) + " cuando la funcion recibe un " + str(tdf) + "\n")
                                self.b = True
                                break
                        local.usado = 1
            else: 
                print("\n-->ERROR SEMANTICO: Estas pasando mas o menos argumentos de los debidos.\n")
                self.b = True

            if self.b == True:
                return
            else: 
                funcion.usado = 1
                print("LLamada a funcion '" + ctx.getChild(0).getText() + "' realizada con exito")

        #chequeo de sintaxis 
        if ctx.PYC() == None:
            print("\n-->ERROR SINTACTICO: Te olvidaste un punto y coma, no te preocupes, suele pasar!\n")
        

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
        print('\n\n***Entre a un CONTEXTO FOR***')

    def exitBloquefor(self, ctx:compiladoresParser.BloqueforContext):
        print('\n***Sali de un CONTEXTO***')
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
        print('\n\n***Entre a un CONTEXTO***')
        contexto= Contexto()
        self.tablaDeSimbolos.addContexto(contexto)
        
    def exitBloque(self, ctx:compiladoresParser.BloqueContext):
        print('\n***Sali de un CONTEXTO***')
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
        print("\n@@@ Declaracion")
    
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
                print("\n-->ERROR SEMANTICO: La variable '" + nombreVariable + "' ya fue declarada en el contexto global \n")

            else:
                print("\n-->ERROR SEMANTICO: La variable '" + nombreVariable + "' ya fue declarada en el contexto local \n")

    def enterAsignacion(self, ctx: compiladoresParser.AsignacionContext):
        print("\n ### ASIGNACION ###")

    def exitAsignacion(self, ctx: compiladoresParser.AsignacionContext):
        nombreVariable= ctx.getChild(0).getText()
        busquedaLocal = self.tablaDeSimbolos.buscarLocal(nombreVariable)

        
        #buscamos si la variable fue declarada localmente
        if busquedaLocal == None :

            #no la encontro entonces la busco localmente
            busquedaGlobal = self.tablaDeSimbolos.buscarGlobal(nombreVariable)

            if busquedaGlobal == None :
                #entonces no la encontro en ningun lado
                print("\n-->ERROR SEMANTICO: Se desconoce el valor de '" + nombreVariable + "', debes declararlo primero !\n")
            else :
                #verificamos si todos los tipos de datos son correctos
                tipoDatoVariable = busquedaGlobal.tipoDato.value
                listaID = []
                cadenaTokens = ctx.getChild(2).getText()
                for simbolos in ['+', '-', '/', '*', '||', '&&']:
                    cadenaTokens = cadenaTokens.replace(simbolos, ' ')
        
                factores = cadenaTokens.split()  # Dividir por espacios
                #aca separamos en dos listas, uno para los numeros otro para los ID
                for f in factores:
                
                    #si la variable es un entero y le llega un flotante
                    if tipoDatoVariable == 'int' and not isint(f):
                        print("\n-->ERROR SEMANTICO en la asignacion de '" + nombreVariable + "':"+ f + " no es un entero\n" )

                    #si la variable espera un flotante y le llega un enrero
                    elif tipoDatoVariable == 'float' and isint(f):
                        print("\n-->ERROR SEMANTICO en la asignacion de '" + nombreVariable + "':"+ f + " no es un flotante\n" )

                    
                    elif f.isalpha():
                        listaID.append(f)

            #verificacion de tipos de datos de IDS
                for id in listaID:
                    variableEncontrada = self.tablaDeSimbolos.buscarGeneral(id)
                    if variableEncontrada != None:
                        if variableEncontrada.tipoDato.value != tipoDatoVariable:
                        #tipos de variable no coinciden
                            print("\n-->ERROR SEMANTICO en la asignacion de '" + nombreVariable + "': La variable '" + variableEncontrada.nombre + "'(" + variableEncontrada.tipoDato.value + ") no es un " + tipoDatoVariable+ "\n")
            
                print("Se inicializo la variable '" + nombreVariable +"'")
                busquedaGlobal.inicializado = 1

        else :
            #la encontro en el contexto local 
            tipoDatoVariable = busquedaLocal.tipoDato.value
            listaID = []
            cadenaTokens = ctx.getChild(2).getText()
            for simbolos in ['+', '-', '/', '*', '||', '&&']:
                cadenaTokens = cadenaTokens.replace(simbolos, ' ')
        
            factores = cadenaTokens.split()  # Dividir por espacios
            #aca separamos en dos listas, uno para los numeros otro para los ID
            for f in factores:
                
                #si la variable es un entero y le llega un flotante
                if tipoDatoVariable == 'int' and not isint(f):
                    print("\n-->ERROR SEMANTICO en la asignacion de '" + nombreVariable + "':"+ f + " no es un entero\n" )

                #si la variable espera un flotante y le llega un enrero
                elif tipoDatoVariable == 'float' and isint(f):
                    print("\n-->ERROR SEMANTICO en la asignacion de '" + nombreVariable + "':"+ f + " no es un flotante\n" )

                    
                elif f.isalpha():
                    listaID.append(f)
                
            



            #verificacion de tipos de datos de IDS
            for id in listaID:
                variableEncontrada = self.tablaDeSimbolos.buscarGeneral(id)
                if variableEncontrada != None:
                    if variableEncontrada.tipoDato.value != tipoDatoVariable:
                        #tipos de variable no coinciden
                        print("\n-->ERROR SEMANTICO en la asignacion de '" + nombreVariable + "': La variable '" + variableEncontrada.nombre + "'(" + variableEncontrada.tipoDato.value + ") no es un " + tipoDatoVariable+ "\n")
                
          
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
                    print("\n-->ERROR SEMANTICO: Estas queriendo usar una variable la cual no conozco el valor, debes inicializarla primero !\n")
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
                            print("\n-->ERROR SEMANTICO: Estas queriendo usar una variable la cual no conozco el valor, debes inicializarla primero !\n")
                else :
                    #no encontro por ningun lado
                    print("\n-->ERROR SEMANTICO: La variable " + factorUsado.getText() + " no fue declarada!\n")



#-----------------------------------------------------------------------------------------------------------
#chequeo de sintaxis
    def exitInstruccion(self, ctx: compiladoresParser.InstruccionContext):
        if ctx.declaracion()!= None or ctx.asignacion()!= None:
            if ctx.PYC() == None:
                print("\n-->ERROR SINTACTICO: Te olvidaste un punto y coma, no te preocupes, suele pasar!\n")

    def exitIfor(self, ctx: compiladoresParser.IforContext):
        if ctx.PA() == None:
            print("\n-->ERROR DE SINTAXIS: No se ha encontrado el parentesis de apertura del for\n")

    def exitIif(self, ctx: compiladoresParser.IifContext):
        if ctx.PA() == None:
            print("\n-->ERROR DE SINTAXIS: No se ha encontrado el parentesis de apertura del if\n")
    
    def exitFunc(self, ctx: compiladoresParser.FuncContext):
        if ctx.PA() == None:
            print("\n-->ERROR DE SINTAXIS: No se ha encontrado el parentesis de apertura de la funcion\n")
    
    
    def exitPrograma(self, ctx:compiladoresParser.ProgramaContext):
  
        print('Fin compilacion\n')
        print("*" * 50 )

         #buscamos ids que hayan sido inicializados pero no usados en el contexto global
         #recorremos el contexto del cual vamos a salir
        for id in self.tablaDeSimbolos.contextos[0].tabla:
            variable = self.tablaDeSimbolos.contextos[0].traerVariable(id)

         #agregamos a la lista de variables no
            if variable.inicializado==1 and variable.usado==0:
                self.idNoUsadosInicializados.append(variable)

        print("En el contexto global se encontro lo siguiente:")
        self.tablaDeSimbolos.contextos[-1].imprimirTabla()
        print("*" * 50 + "\n")
        print("-**-" * 25 + "")
        print("Identificadores inicializadas pero no usados:")
        for id in self.idNoUsadosInicializados:
            print(id)


#-----------------------------------------------------------------------------------------------------------
#chequeo de sintaxis
    # def exitInstruccion(self, ctx: compiladoresParser.InstruccionContext):
    #     if ctx.declaracion()!= None:
    #         print("hola")

    # def exitIfor(self, ctx: compiladoresParser.IforContext):
    #     if ctx.PC() == None:
    #         print("\n-->ERROR DE SINTAXIS: No se ha encontrado el parentesis de cierre del for\n")
    
    
