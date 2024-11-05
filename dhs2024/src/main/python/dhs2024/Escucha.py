from antlr4 import TerminalNode
from compiladoresListener import compiladoresListener
from compiladoresParser import compiladoresParser
from TablaSimbolos import TablaSimbolos
from Contexto import Contexto
from ID import ID,TipoDato
from Funcion import Funcion
from Variable import Variable
from ErrorSemantico import ErrorSemantico

#funcion auxiliar para comprobar tipos de datos
def isint(num):
    numero = float(num)
    return str(numero).endswith('.0')


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
    auxreturn = ''
    #lista de ID inicializados pero sin ser usados
    idNoUsadosInicializados = []

    #lista de errores semanticos
    erroresSemanticos = []

    #para la declaracion continua de variables por coma
    listaCrearVariablesAux = []

    #lista para asignacion
    listaIdAsinacion = []
    listanumerosAsignacion = []

    #tipo de dato para lista de declaracion + asignaciones
    tipoDatoDeclasignacion = 0

    #archivos donde mostramos las salidas
    archivoErroresSemanticos = open("./output/erroresSemanticos.txt", "w")
    archivoSalida = open("./output/salida.txt", "w")


# main --------------------------------------------------------------------------------------------------
    #def exitFmain(self, ctx: compiladoresParser.FmainContext):
     #   print("Funcion main")

    def enterPrograma(self, ctx: compiladoresParser.ProgramaContext):
        print("\n" + "*" * 30 + "COMIENZA LA COMPILACION" + "*" * 30 + "\n" )

#prototipo de funciones ----------------------------------------------------------------------------------------------
    def enterPrototipofunc(self, ctx: compiladoresParser.PrototipofuncContext):
        print('\n --- Prototipo de funcion ---')
        self.banderap = False
        self.auxArgumentos.clear()
    
    def exitDeclargumentos(self, ctx:compiladoresParser.DeclaracionContext):
        if(self.banderap == False):
            tipoDeDato= ctx.getChild(0).getText()
            nombreVariable= ctx.getChild(1).getText()
            if (len(self.auxArgumentos) != 0):
                for i in self.auxArgumentos:
                    if i.nombre == nombreVariable:
                        #print("\n-->ERROR SEMANTICO: Estas definiendo argumentos con el mismo nombre\n")
                        #error argumentos con mismo nombre
                        self.erroresSemanticos.append(ErrorSemantico(ctx.start.line,"Argumentos repetidos","Estas definiendo argumentos con el mismo nombre"))
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
                self.erroresSemanticos.append(ErrorSemantico(ctx.start.line,"ERROR: Semantico", "No declaramos main" + nombreFuncion))
                return
            
            #buscamos si este nombre no le corresponde un ID
            busquedaGlobal = self.tablaDeSimbolos.buscarGlobal(nombreFuncion)
            if(busquedaGlobal == None):
                tipoDeDato =  ctx.getChild(0).getText()
                self.tablaDeSimbolos.addIdentificador(nombreFuncion,tipoDeDato,1,argumentos)#pongo 1 xq es funcion
                print("\nPrototipo de funcion '" +nombreFuncion + "' guardado con exito")
                
            else:
                #print("\n-->ERROR SEMANTICO, DOBLE DECLARACION DEL MISMO IDENTIFICADOR: Ya existe el prototipo de funcion con el nombre "+ nombreFuncion + "!\n")
                self.erroresSemanticos.append(ErrorSemantico(ctx.start.line,"Doble declaracion del mismo identificador","Ya existe el prototipo de funcion con el nombre" + nombreFuncion))


        
    
# definicion de funciones y bloque ------------------------------------------------------------------------------------------------------------    
    def enterFunc(self, ctx: compiladoresParser.FuncContext):
        #en las funciones creamos el contexto al definirlas, para poder agregar sus argumentos al contexto
        print("\n--- Inicializacion funcion ---")
        self.banderaf = False
    
    def exitNombrefuncion(self, ctx: compiladoresParser.NombrefuncionContext):
        #aca ya se el nombre de la funcion entonces lo uso para buscar sus argumentos
        if (str(ctx.ID()) == 'main'):
            self.auxArgumentosf.clear()
            self.auxNombreFuncion = ctx.ID().getText()
            return
        
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
        if self.auxNombreFuncion == 'main':
            if self.auxtipoDato == TipoDato('int'):
                if len(self.auxArgumentosf) == 0: #vamos a suponer que main no recibe argumentos
                    self.tablaDeSimbolos.addIdentificador('main',self.auxtipoDato,1,self.auxArgumentosf)
                    contextoInicializado = Contexto(self.auxArgumentosf)
                    self.tablaDeSimbolos.addContexto(contextoInicializado)
                    return
                else: 
                    print('NO le pasamos argumentos al main')
                    self.banderaf = True
                    return
            else:
                print('Solo puede retornar un tipo de dato int')
                self.banderaf = True
                return
            
        funcion = self.tablaDeSimbolos.buscarGlobal(self.auxNombreFuncion)
        if (self.auxtipoDato != funcion.tipoDato):
            #print("\n-->ERROR: Se esperaba un tipo de dato: " + str(funcion.tipoDato) + " y queres inicializar: " + str(self.auxtipoDato) + "\n")
            self.erroresSemanticos.append(ErrorSemantico(ctx.start.line,"Error de tipo de dato","Se esperaba un tipo de dato: " + str(funcion.tipoDato) + " y queres inicializar: " + str(self.auxtipoDato)))
            self.banderaf = True
            return
        
        print('\n--- Contexto funcion ---')
        argumentos = funcion.argumentos
        if (len(argumentos) == len(self.auxArgumentosf)):
            if(len(argumentos) != 0):
                i = 0

                while i<len(argumentos): #comprobamos que los argumentos sean lo mismo y esten en el mismo orden
                    if(not (argumentos[i].nombre == self.auxArgumentosf[i].nombre and
                    argumentos[i].tipoDato == self.auxArgumentosf[i].tipoDato)):
                        #print("\n-->ERROR SEMANTICO: Argumento de la funcion '" + self.auxNombreFuncion + "' no coincide con prototipo\n")
                        self.erroresSemanticos.append(ErrorSemantico(ctx.start.line,"Argumentos de la funcion no coinciden","Se esperaba un tipo de dato: " + "Argumento de la funcion '" + self.auxNombreFuncion + "' no coincide con prototipo"))

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
            #print("-->ERROR SEMANTICO: Revisar la cantidad de argumentos")
            self.erroresSemanticos.append(ErrorSemantico(ctx.start.line,"Cantidad de argumentos","Revisar la cantidad de argumentos"))

            self.banderaf = True

    def exitBloqueespecial(self, ctx:compiladoresParser.BloqueContext):
        if (self.banderaf == True):
            return 
        print('\n--- Sali de un CONTEXTO de funcion ---')
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

        #impresion en archivo
        self.archivoSalida.write("-" * 50 + "\n")
        self.archivoSalida.write("En el contexto iniciado en la linea " + str(ctx.start.line) +" se encontro lo siguiente:\n")
        self.tablaDeSimbolos.contextos[-1].imprimirTablaArchivo(self.archivoSalida)

        self.tablaDeSimbolos.delContexto()

# llamada a funcion ---------------------------------------------------------------------------------
    def enterLlamadafunc(self, ctx: compiladoresParser.LlamadafuncContext):
        print("--- Llamada a funcion ---")
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

# return funciones -----------------------------------------------------------------------------------
    def exitReturn(self, ctx: compiladoresParser.ReturnContext):

        funcion = self.tablaDeSimbolos.buscarGlobal(self.auxNombreFuncion)

        if (funcion == None):
            print("ERROR: Estoy llamando a un return fuera del contexto de una funcion")
            return
        tipodeDato = funcion.tipoDato
        if (ctx.ID() != None):
            variable = self.tablaDeSimbolos.buscarLocal(ctx.ID().getText())
            if variable == None: 
                print("ERROR: No podemos retornar una variable no declarada")
            else: 
                if tipodeDato != variable.tipoDato:
                    print("ERROR: El tipo de dato de la variable y de la funcion deben ser el mismo")    

        if (ctx.NUMERO() != None):
            if tipodeDato != TipoDato('int'):
                print("ERROR: El tipo de dato del numero y de la funcion deben ser el mismo")

        if (ctx.NUMEROFLOAT() != None):
            if tipodeDato != TipoDato('float'):
                print("ERROR: El tipo de dato del numero y de la funcion deben ser el mismo")
        
        if (ctx.LETRACHAR() != None):
            if tipodeDato != TipoDato('char'):
                print("ERROR: El tipo de dato del numero y de la funcion deben ser el mismo")        

# for -----------------------------------------------------------------------------------------------
    def enterIfor(self, ctx: compiladoresParser.IforContext):
        print("\n--- Bloque for ---")
    #iniciacion en el for

    def exitInit(self, ctx: compiladoresParser.InitContext):
        nombreVariable= ctx.getChild(1).getText()
        tipoDato= ctx.getChild(0).getText()
        variableInit = Variable(nombreVariable,tipoDato,1,0)
        #print("variable init:" + str(variableInit))
        #por como esta definido la iniciacion de un contexto, el primer argumento es si son lista de  args de funcion
        # su segundo argumento esta destinado a una sola variable
        self.tablaDeSimbolos.contextos[-1].tabla.update({variableInit.nombre:variableInit})
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
        print('\n--- Entre a un CONTEXTO ---')
        contexto= Contexto()
        self.tablaDeSimbolos.addContexto(contexto)
        
    def exitBloque(self, ctx:compiladoresParser.BloqueContext):
        print('\n--- Sali de un CONTEXTO ---')
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


        #impresion en archivo
        self.archivoSalida.write("-" * 50 + "\n")
        self.archivoSalida.write("En el contexto iniciado en la linea " + str(ctx.start.line) +" se encontro lo siguiente:\n")
        self.tablaDeSimbolos.contextos[-1].imprimirTablaArchivo(self.archivoSalida)

        self.tablaDeSimbolos.delContexto()

    def enterDeclaracion(self, ctx: compiladoresParser.DeclaracionContext):
        print("\n--- Declaracion ---")
            
    def exitDeclaracion(self, ctx:compiladoresParser.DeclaracionContext):
        tipoDeDato= ctx.getChild(0).getText()
        nombreVariable= ctx.getChild(1).getText()
    
        busquedaContexto = self.tablaDeSimbolos.buscarEnMiContexto(nombreVariable)

        if busquedaContexto == None:
            self.tablaDeSimbolos.addIdentificador(nombreVariable,tipoDeDato,0,None)
        
        else:
            self.erroresSemanticos.append(ErrorSemantico(ctx.start.line,"Declaracion del mismo identificador","La variable '" + nombreVariable + "' ya fue declarada en el contexto local"))

        #lo hablamos con el profe y para la declaracion solamente se mira al contexto en el que estamos
        #es decir, se puede declarar en un contexto una variable la cual fue declarada en otro contexto
       

    def exitDeclid(self, ctx: compiladoresParser.DeclidContext):
        #chequeo que declid no sea landa
        #declid es el prima de declaraciones
        if ctx.getChildCount() > 0 :
                self.listaCrearVariablesAux.append(ctx.getChild(1).getText())

    def exitDeclaraciones(self, ctx: compiladoresParser.DeclaracionesContext):
        #print(ctx.declaracion().ID().getText())
        #extraemos el tipo de dato
        tipoDato = ctx.declaracion().tipodato().getText()
        
        #por defecto ya hay dos variables a crear: la primera y la segunda
        self.listaCrearVariablesAux.append(ctx.declaracion().getChild(1).getText())
        self.listaCrearVariablesAux.append(ctx.ID().getText())

        for nombre in self.listaCrearVariablesAux:
                #print(nombre)
                self.tablaDeSimbolos.addIdentificador(nombre,tipoDato,0,None)
        
        self.listaCrearVariablesAux.clear()


    def exitDeclasignaciontipo(self, ctx: compiladoresParser.DeclasignaciontipoContext):
        self.tipoDatoDeclasignacion = ctx.getChild(0).getText()


    def exitDeclasignaciones(self, ctx: compiladoresParser.DeclasignacionesContext):
        self.tipoDatoDeclasignacion = 0

    def exitDasignacion(self, ctx: compiladoresParser.DasignacionContext):
         #creacion de variable
        tipoDeDato= self.tipoDatoDeclasignacion
        nombreVariable= ctx.getChild(0).getText()
    
        busquedaContexto = self.tablaDeSimbolos.buscarEnMiContexto(nombreVariable)

        if busquedaContexto == None:
            self.tablaDeSimbolos.addIdentificador(nombreVariable,tipoDeDato,0,None,1)
        
        else:
            self.erroresSemanticos.append(ErrorSemantico(ctx.start.line,"Declaracion del mismo identificador","La variable '" + nombreVariable + "' ya fue declarada en el contexto local"))

        #chequeo los id tengan el mismo dato
        for id in self.listaIdAsinacion:
            #todos los id que traigo ya existen, debido a que si no lo hubiese enocntrado ya hubiese tirado un error en factor
            if id.tipoDato.value != tipoDeDato :
                self.erroresSemanticos.append(ErrorSemantico(ctx.start.line,"Tipos de datos incompatibles en la asignacion","TIPOS DE DATOS INCOMPATIBLES en la asignacion de '" + nombreVariable + "': La variable '" + id.nombre + "'(" + id.tipoDato.value + ") no es un " + tipoDeDato))
            
            #chequeo de los numeros
        for numero in self.listanumerosAsignacion:
                
            if tipoDeDato == 'int' and not isint(numero):
                self.erroresSemanticos.append(ErrorSemantico(ctx.start.line,"Tipos de datos incompatibles en la asignacion","TIPOS DE DATOS INCOMPATIBLES en la asignacion de '" + nombreVariable + "':"+ numero + " no es un entero"))

            elif tipoDeDato == 'float' and isint(numero):
                self.erroresSemanticos.append(ErrorSemantico(ctx.start.line,"Tipos de datos incompatibles en la asignacion","TIPOS DE DATOS INCOMPATIBLES en la asignacion de '" + nombreVariable + "':"+ numero + " no es un flotante"))

            elif tipoDeDato == 'char' and numero.isdigit():
                self.erroresSemanticos.append(ErrorSemantico(ctx.start.line,"Tipos de datos incompatibles en la asignacion","TIPOS DE DATOS INCOMPATIBLES en la asignacion de '" + nombreVariable + "':"+ numero + " no es un char"))

        self.listaIdAsinacion.clear()
        self.listanumerosAsignacion.clear()
        

    
        

    def exitDeclasign(self, ctx: compiladoresParser.DeclasignContext):
        #creacion de variable
        tipoDeDato= ctx.getChild(0).getText()
        nombreVariable= ctx.getChild(1).getText()
    
        busquedaContexto = self.tablaDeSimbolos.buscarEnMiContexto(nombreVariable)

        if busquedaContexto == None:
            self.tablaDeSimbolos.addIdentificador(nombreVariable,tipoDeDato,0,None,1)
        
        else:
            self.erroresSemanticos.append(ErrorSemantico(ctx.start.line,"Declaracion del mismo identificador","La variable '" + nombreVariable + "' ya fue declarada en el contexto local"))

        
        # #asignacion
        # if "'" == ctx.getChild(3).getText():
        #     #estqmos en un char
        #     if len(ctx.getChild(4).getText()) > 1:
        #         #print(ctx.getText() + "-->ERROR SEMANTICO, No puedes asignar un STRING a un CHAR")
        #         self.erroresSemanticos.append(ErrorSemantico(ctx.start.line,"Incorrecta asignacion de un char","No puedes asignar un STRING a un CHAR"))
        #         return 
            
          
        #chequeo los id tengan el mismo dato
        
        for id in self.listaIdAsinacion:
            #todos los id que traigo ya existen, debido a que si no lo hubiese enocntrado ya hubiese tirado un error en factor
            if id.tipoDato.value != tipoDeDato :
                self.erroresSemanticos.append(ErrorSemantico(ctx.start.line,"Tipos de datos incompatibles en la asignacion","TIPOS DE DATOS INCOMPATIBLES en la asignacion de '" + nombreVariable + "': La variable '" + id.nombre + "'(" + id.tipoDato.value + ") no es un " + tipoDeDato))
            
            #chequeo de los numeros
        for numero in self.listanumerosAsignacion:
                
            if tipoDeDato == 'int' and not isint(numero):
                self.erroresSemanticos.append(ErrorSemantico(ctx.start.line,"Tipos de datos incompatibles en la asignacion","TIPOS DE DATOS INCOMPATIBLES en la asignacion de '" + nombreVariable + "':"+ numero + " no es un entero"))

            elif tipoDeDato == 'float' and isint(numero):
                self.erroresSemanticos.append(ErrorSemantico(ctx.start.line,"Tipos de datos incompatibles en la asignacion","TIPOS DE DATOS INCOMPATIBLES en la asignacion de '" + nombreVariable + "':"+ numero + " no es un flotante"))

            elif tipoDeDato == 'char' and numero.isdigit():
                self.erroresSemanticos.append(ErrorSemantico(ctx.start.line,"Tipos de datos incompatibles en la asignacion","TIPOS DE DATOS INCOMPATIBLES en la asignacion de '" + nombreVariable + "':"+ numero + " no es un char"))

        self.listaIdAsinacion.clear()
        self.listanumerosAsignacion.clear()
        



    def enterAsignacion(self, ctx: compiladoresParser.AsignacionContext):
        print("\n--- Asignacion ---")

    def exitAsignacion(self, ctx: compiladoresParser.AsignacionContext):
        #quiero ver si asigno un CHAR
        llamada = ctx.llamadafunc()
        if (llamada != None):
            nombre = llamada.nombre().getText()
            funcion = self.tablaDeSimbolos.buscarGlobal(nombre)
            if (funcion != None):
                tipodeDato = funcion.tipoDato
                var = ctx.getChild(0).getText()
                var = self.tablaDeSimbolos.buscarGeneral(var)
                if var != None: 
                    tipodatovar = var.tipoDato
                    if (tipodatovar != tipodeDato):
                        print('ERROR: El tipo de dato que retorna la funcion es distinto al tipo de dato de la variable')
                        return
                    else:
                        print("inicializacion correcta con prototipo")
                        var.inicializado = 1
                        return
            else:
                print('ERROR: No existe prototipo de funcion, no podemos inicializar')
                return

        if "'" == ctx.getChild(2).getText():
            #estqmos en un char
            if len(ctx.getChild(3).getText()) > 1:
                #print(ctx.getText() + "-->ERROR SEMANTICO, No puedes asignar un STRING a un CHAR")
                self.erroresSemanticos.append(ErrorSemantico(ctx.start.line,"Incorrecta asignacion de un char","No puedes asignar un STRING a un CHAR"))
                return 
            
          
        nombreVariable= ctx.getChild(0).getText()
        #busqueda general busca desde local hacia global
        busqueda = self.tablaDeSimbolos.buscarGeneral(nombreVariable)

        if busqueda == None:
            #no la encontro en ningun lado
            self.erroresSemanticos.append(ErrorSemantico(ctx.start.line,"Uso de un identificador sin inicializar","Se desconoce el valor de '" + nombreVariable + "', debes declararlo primero"))
            pass
            
        else:
            tipoDato = busqueda.tipoDato.value
            #chequeo los id tengan el mismo dato
            for id in self.listaIdAsinacion:
                #todos los id que traigo ya existen, debido a que si no lo hubiese enocntrado ya hubiese tirado un error en factor
                if id.tipoDato.value != tipoDato :
                    self.erroresSemanticos.append(ErrorSemantico(ctx.start.line,"Tipos de datos incompatibles en la asignacion","TIPOS DE DATOS INCOMPATIBLES en la asignacion de '" + nombreVariable + "': La variable '" + id.nombre + "'(" + id.tipoDato.value + ") no es un " + tipoDato))
            
            #chequeo de los numeros
            for numero in self.listanumerosAsignacion:
                
                if tipoDato == 'int' and not isint(numero):
                    self.erroresSemanticos.append(ErrorSemantico(ctx.start.line,"Tipos de datos incompatibles en la asignacion","TIPOS DE DATOS INCOMPATIBLES en la asignacion de '" + nombreVariable + "':"+ numero + " no es un entero"))

                elif tipoDato == 'float' and isint(numero):
                    self.erroresSemanticos.append(ErrorSemantico(ctx.start.line,"Tipos de datos incompatibles en la asignacion","TIPOS DE DATOS INCOMPATIBLES en la asignacion de '" + nombreVariable + "':"+ numero + " no es un flotante"))

                elif tipoDato == 'char' and numero.isdigit():
                    self.erroresSemanticos.append(ErrorSemantico(ctx.start.line,"Tipos de datos incompatibles en la asignacion","TIPOS DE DATOS INCOMPATIBLES en la asignacion de '" + nombreVariable + "':"+ numero + " no es un char"))

            busqueda.inicializado = 1
            self.listaIdAsinacion.clear()
            self.listanumerosAsignacion.clear()
                             
    def exitFactor(self, ctx: compiladoresParser.FactorContext):
        
        #factores pueden tener 3 valores : numero - ID - (opal)
        #al hacer ctx.ID() solo traes ID , son los que me interesan para marcar su uso
        factorUsado = ctx.ID()
        if factorUsado != None :
            #significa que ingrese un identificador
            busqueda = self.tablaDeSimbolos.buscarGeneral(factorUsado.getText())

            if busqueda == None:
                #busqueda general busca desde local hacia global
                self.erroresSemanticos.append(ErrorSemantico(ctx.start.line,"Uso de identificador sin declarar","La variable " + factorUsado.getText() + " no fue declarada"))
                return

            else:
                self.listaIdAsinacion.append(busqueda)

                if busqueda.inicializado == 0 :
                    #marco a mi nombre de variable como usado
                    #print("\n-->ERROR SEMANTICO, USO DE UN IDENTIFICADOR SIN INICIALIZAR: Estas queriendo usar una variable la cual no conozco el valor, debes inicializarla primero !\n")
                    self.erroresSemanticos.append(ErrorSemantico(ctx.start.line,"Uso de identificador sin inicializar","Estas queriendo usar una variable la cual no conozco el valor, debes inicializarla primero "))

                elif busqueda.usado == 0:
                    busqueda.usado = 1 
                    print(factorUsado.getText() + " ha sido  marcado como usado")
    
            
        if ctx.NUMERO() != None:
            self.listanumerosAsignacion.append(ctx.NUMERO().getText())
        
        if ctx.NUMEROFLOAT() != None:
            self.listanumerosAsignacion.append(ctx.NUMEROFLOAT().getText())
        
      
        


#---- cuando se usa opal, los factores se agregan a la lista auxiliar, si se llama a opal de algun lado que no sea para asignacion, hay que vaciar esta lista
    def exitIfor(self, ctx: compiladoresParser.IforContext):
        self.listaIdAsinacion.clear()
        self.listanumerosAsignacion.clear()
        
    def exitIwhile(self, ctx: compiladoresParser.IwhileContext):
        self.listaIdAsinacion.clear()
        self.listanumerosAsignacion.clear()

    def exitIif(self, ctx: compiladoresParser.IifContext):
        self.listaIdAsinacion.clear()
        self.listanumerosAsignacion.clear()

#-----------------------------------------------------------------------------------------------------------

    
    def exitPrograma(self, ctx:compiladoresParser.ProgramaContext):
  
        print("\n" + "*" * 30 + "FIN DE LA COMPILACION" + "*" * 30 + "\n" )


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
        print("--" * 25)
        print("Identificadores inicializadas pero no usados:")
        for id in self.idNoUsadosInicializados:
            print(id)

        #impresion en archivo de variables en contexto
        self.archivoSalida.write("\n" + "-" * 50 + "\n")
        self.archivoSalida.write("En el contexto global se encontro lo siguiente:\n")
        self.tablaDeSimbolos.contextos[-1].imprimirTablaArchivo(self.archivoSalida)

        #impresion de variables no usadas pero inicializadas
        self.archivoSalida.write("\n" + "--" * 25 + "\n")
        self.archivoSalida.write("Identificadores inicializadas pero no usados:\n")
        for id in self.idNoUsadosInicializados:
            self.archivoSalida.write(str(id) + "\n")

        #impresion de errores en archivo
        self.archivoErroresSemanticos.write("\n--- Errores semanticos ---\n")
        if len(self.erroresSemanticos) > 0:
            for error in self.erroresSemanticos:
                self.archivoErroresSemanticos.write("-" * 50 + "\n")
                self.archivoErroresSemanticos.write(str(error))
        
        else :
            self.archivoErroresSemanticos.write("Tu codigo no tiene errores semanticos!")





#-----------------------------------------------------------------------------------------------------------
#chequeo de sintaxis
    # def exitInstruccion(self, ctx: compiladoresParser.InstruccionContext):
    #     if ctx.declaracion()!= None:
    #         print("hola")

    # def exitIfor(self, ctx: compiladoresParser.IforContext):
    #     if ctx.PC() == None:
    #         print("\n-->ERROR DE SINTAXIS: No se ha encontrado el parentesis de cierre del for\n")
    
    
