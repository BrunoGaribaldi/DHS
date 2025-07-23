from compiladoresVisitor import compiladoresVisitor
from compiladoresParser import compiladoresParser


class VarTemporal:
    contador = -1
    def __init__(self):
        self.nombre = "t" + self.contador
        self.contador = self.contador + 1
        self.proxOp = "" 
        self.prim = 0
class Walker (compiladoresVisitor):

    # tres instrucciones
    contadorVarTemporales = 0
    variablesTemporales = []
    operador = []
    varAAsignar = ''
    
    #etiquetas
    etiquetas = []
    contadorEtiquetas = 0
    
    #archivo
    archivoCodigoIntermedio = open("./output/codigoIntermedio.txt", "w")

    
    def visitPrograma(self, ctx: compiladoresParser.ProgramaContext):
        return super().visitPrograma(ctx)
      

    def visitDeclasign(self, ctx):
        self.varAAsignar = ctx.getChild(1).getText()
        print(self.varAAsignar)
        if len(ctx.getChild(3).getText()) != 1:
            return self.visitOpal(ctx.getChild(2))
        else:
            print(ctx.getText())
    
        return super().visitDeclasign(ctx)
    
    def visitAsignacion(self, ctx):
        self.varAAsignar = ctx.getChild(0).getText()
        print(self.varAAsignar)
        
        if ctx.llamadafunc(): #estoy en una funcion
           self.visitLlamadafunc(ctx.getChild(2))
        else:
            if len(ctx.getChild(2).getText()) != 1:
                self.visitOpal(ctx.getChild(2))
                #print(self.variablesTemporales)
                var = self.variablesTemporales.pop()
            
                print(ctx.getChild(0).getText() + ' = ' + var)
                self.archivoCodigoIntermedio.write(ctx.getChild(0).getText() + ' = ' + var + '\n \n')
            else:
                self.archivoCodigoIntermedio.write(ctx.getText()+ '\n \n')      
                print(ctx.getText())
    
    
    def visitFunc(self, ctx):
        labelFuncion = 'l' + str(self.contadorEtiquetas)
        dirRetorno = 't' + str(self.contadorVarTemporales)
        self.contadorEtiquetas = self.contadorEtiquetas + 1
        self.contadorVarTemporales = self.contadorVarTemporales + 1
        
         
        self.archivoCodigoIntermedio.write('label ' + labelFuncion + '\n')
        self.archivoCodigoIntermedio.write('pop ' + dirRetorno + '\n') #direccion de retorno, me llega l1 pero yo lo nombro t0
        
        #voy a argumentos para que escriban pop ...
        self.visitArgumentosf(ctx.getChild(3))
        self.visitBloqueespecial(ctx.getChild(5)) #visito las instrucciones
        
        #pusheamos a la pila la variable de retorno
        self.archivoCodigoIntermedio.write('push t' + str(self.contadorVarTemporales - 1) + '\n')
        self.archivoCodigoIntermedio.write('jump ' + dirRetorno + '\n') #saltoa direccion de retorno
                        
    
    def visitArgumentosf(self, ctx):
        if ctx.getChildCount() != 0: #puede no tener argumentos
            self.visitFuncargumentos(ctx.getChild(0)) #siempre va a tener un argumetno, lo visito
            if ctx.getChildCount() > 1:
                self.visitArgumentosf(ctx.getChild(2)) #si tiene mas, hago una especie de recursividad
            
            
    
    def visitFuncargumentos(self, ctx):
        self.archivoCodigoIntermedio.write('pop ' + ctx.getChild(1).getText() + '\n')
        
        
    def visitIif(self, ctx):
        print('Entre a if')
        self.visitOpal(ctx.getChild(2))
        # t0 = x > 1
        varComp = self.variablesTemporales.pop() #tiene el t0
        #creamos la etiqueta donde va a saltar
        #self.etiquetas.append('l' + str(self.contadorEtiquetas))
        etiqSaltar = "l" + str(self.contadorEtiquetas)  #si no hay else
        etiqSaltarElse = "l" + str(self.contadorEtiquetas + 1)  #si  hay else
        
        if ctx.getChildCount() > 5: #hay else
            self.archivoCodigoIntermedio.write("ifntjmp " + varComp + ", " + etiqSaltarElse + '\n')
            print("ifntjmp " + varComp + ", " + etiqSaltar)
        
        else:
            self.archivoCodigoIntermedio.write("ifntjmp " + varComp + ", " + etiqSaltar + '\n')
            print("ifntjmp " + varComp + ", " + etiqSaltar)
            
            
          
        self.contadorEtiquetas = self.contadorEtiquetas + 1 
        self.visitInstruccion(ctx.getChild(4))
        if ctx.getChildCount() > 5: #hay un else
            
            self.archivoCodigoIntermedio.write("jmp " + etiqSaltar+ '\n')     
            print("jmp " + etiqSaltarElse) #ya entro al if, escapo dl else
            
            self.archivoCodigoIntermedio.write('label '+ etiqSaltarElse+ '\n')     
            print('label '+ etiqSaltar)
            
            self.visitInstruccion(ctx.getChild(6))
        
            
        self.archivoCodigoIntermedio.write('label '+ etiqSaltar+ '\n')     
        print('label '+ etiqSaltar) #seria como el fin del bloque del if
        
        self.contadorEtiquetas = self.contadorEtiquetas + 1
        


    def visitIfor(self, ctx):
        #for ( i = 0 ; i< x ; i = i + 1 ) y = z * x;

        self.visitAsignacion(ctx.getChild(2)) #visito i = 0
        labelEvalCond = 'l' + str(self.contadorEtiquetas) #label en el que evaluo si x < 0
        
        self.archivoCodigoIntermedio.write('label ' + labelEvalCond+ '\n')
        print('label ' + labelEvalCond)
        
        self.contadorEtiquetas = self.contadorEtiquetas + 1
        labelFinFor = 'l' + str(self.contadorEtiquetas) #cuando salga del for me vot aca
        self.visitCond(ctx.getChild(4)) #entro a la condicion
        
        #sies falso salto al fin del dor
        self.archivoCodigoIntermedio.write('ifntjmp t' + str(self.contadorVarTemporales - 1) + ', l' + str(self.contadorEtiquetas)+ '\n')
        print('ifntjmp t' + str(self.contadorVarTemporales - 1) + ', l' + str(self.contadorEtiquetas))
        
        self.visitInstruccion(ctx.getChild(8)) #visito el bloque
        self.visitIter(ctx.getChild(6)) #una vez finalizaod el bloque incremento i por ejemolo
        
        self.archivoCodigoIntermedio.write('jmp ' + labelEvalCond + '\n')
        print('jmp ' + labelEvalCond)
        
        self.archivoCodigoIntermedio.write('label ' + labelFinFor + '\n')
        print('label ' + labelFinFor)
        
        self.contadorEtiquetas = self.contadorEtiquetas + 1
        
             
    
    def visitOpal(self, ctx):
        print("visitando opal de la variable " + self.varAAsignar)
        return self.visitTermino1(ctx.getChild(0))

    def visitTermino1(self, ctx):
        print("visitando termino 1 de la variable " + self.varAAsignar)
        return self.visitTermino2(ctx.getChild(0))

    def visitTermino2(self, ctx):
        print("visitando termino 2 de la variable " + self.varAAsignar)
        return self.visitTermino3(ctx.getChild(0))
    

    def visitTermino3(self, ctx):
        print("visitando termino 3 de la variable " + self.varAAsignar)
        
        #mayormente no hay comparaciones, por eso me fijo antes de irme
        ops = ("==", ">",">=", "<", "<=")
        if not any(op in ctx.getText() for op in ops):
            return self.visitTermino4(ctx.getChild(0))
        else:
            #me llega esto x > 5
            if ctx.getChild(1).getChild(1).getChild(1).getChildCount() == 0:
                
                self.archivoCodigoIntermedio.write("t" + str(self.contadorVarTemporales) + " = "+ ctx.getText()+ '\n')      
                print("t" + str(self.contadorVarTemporales) + " = "+ ctx.getText())
                
                self.variablesTemporales.append("t" + str(self.contadorVarTemporales)) #hago el append para que salte despues
                self.contadorVarTemporales =+ 1
                return
    
    #prueba

   
    def visitTermino4(self, ctx):
        print('parte termino 4')
        
        #primer caso, me llega x = 2 + 3
        if len(ctx.getText()) == 3 and ('+' in ctx.getText() or '-' in ctx.getText()) and len(self.operador) == 0: #x = 5 + 6 -> solamente en estos casos
            
            self.archivoCodigoIntermedio.write("t" + str(self.contadorVarTemporales) + " = "+ ctx.getText()+ '\n')      
            print("t" + str(self.contadorVarTemporales) + " = "+ ctx.getText())
            
            
            self.variablesTemporales.append("t" + str(self.contadorVarTemporales)) #hago el append para que salte despues
            self.contadorVarTemporales = self.contadorVarTemporales + 1
            return
        
        #caso base 
        
        if len(self.operador) != 0 and ctx.getChild(0).getChild(1) == 0:  #x = 5 + 7 - (8)-> esto seria
            varTemp = self.variablesTemporales.pop() #saco la variabler anterior, en este caso t0
            operador = self.operador.pop() #el operador que le agregue en el coso muldiv
            
            self.archivoCodigoIntermedio.write("t" + str(self.contadorVarTemporales) + " = "+ varTemp + operador + ctx.getChild(0).getText()+ '\n')      
            print("t" + str(self.contadorVarTemporales) + " = "+ varTemp + operador + ctx.getChild(0).getText()) #t1 = t0 - 7
            
            if ctx.getChild(1).getChildCount() != 0:
                self.variablesTemporales.append("t" + str(self.contadorVarTemporales)) #appendeo t0
                self.contadorVarTemporales = self.contadorVarTemporales + 1 #no appendeo ninguna variable, solo sumo
                self.visitPartesumaresta(ctx.getChild(1)) #x = 5 * 6 (+ 1)-> le paso esta parte
                return
            
            self.variablesTemporales.append("t" + str(self.contadorVarTemporales)) #hago el append para que salte despues
            self.contadorVarTemporales = self.contadorVarTemporales + 1 #no appendeo ninguna variable, solo sumo

        else:
            #parte multiplicacion de terminos
            #lado izquierdo sin multpilciacion pero derecho si por ejemplo x = 1 + 2*3
            if ctx.getChild(0).getChild(1).getChildCount() == 0 and ('*' in ctx.getChild(1).getText() or '/' in ctx.getChild(1).getText()): #
                print(ctx.getChild(1).getChild(1).getText())
                
                print("t" + str(self.contadorVarTemporales) + " = "+ctx.getChild(0).getText()) #t1 = 1
                self.archivoCodigoIntermedio.write("t" + str(self.contadorVarTemporales) + " = "+ctx.getChild(0).getText() + '\n') #t1 = 1
                
                self.variablesTemporales.append("t" + str(self.contadorVarTemporales)) #appendeo t0
                self.contadorVarTemporales = self.contadorVarTemporales + 1 #no appendeo ninguna variable, solo sumo
                
                self.visitPartesumaresta(ctx.getChild(1))
                return
            if ctx.getChild(0).getChild(1).getChildCount() != 0 : #si hay alguna multiplicacion visito esto
                print(ctx.getChild(0).getText())
                self.visitTermino5(ctx.getChild(0))
                if ctx.getChild(1).getChildCount() != 0: 
                    
                    #antes de visitar quiero ver si no tengo que imprimir una suma de variables anteriores
                    if len(self.operador) != 0 and len(self.variablesTemporales) > 1 :
                        segNum = self.variablesTemporales.pop()
                        primNum = self.variablesTemporales.pop()
                        op = self.operador.pop()
                        
                        self.archivoCodigoIntermedio.write("t" + str(self.contadorVarTemporales) + " = "+ primNum + op + segNum+ '\n')      
                        print("t" + str(self.contadorVarTemporales) + " = "+ primNum + op + segNum ) #t0 = 4+5
                
                        self.variablesTemporales.append("t" + str(self.contadorVarTemporales)) #appendeo t0
                        self.contadorVarTemporales = self.contadorVarTemporales +1  
            
                    self.visitPartesumaresta(ctx.getChild(1)) #ejemplo x = 5 *7 (+ 1) -> esto le paso 
                else:
                    if len(self.operador) != 0 and len(self.variablesTemporales) > 1 : #si ya hay algunas variables antes
                        segNum = self.variablesTemporales.pop()
                        primNum = self.variablesTemporales.pop()
                        op = self.operador.pop()
                       
                        self.archivoCodigoIntermedio.write("t" + str(self.contadorVarTemporales) + " = "+ primNum + op + segNum+ '\n')      
                        print("t" + str(self.contadorVarTemporales) + " = "+ primNum + op + segNum ) #t0 = 4+5
                
            
                        self.variablesTemporales.append("t" + str(self.contadorVarTemporales)) #appendeo t0
                        self.contadorVarTemporales = self.contadorVarTemporales +1  
            
                    
                    
                    
        #para partir la suma
        #segundo caso, x = 2 + 6 + 5 + ...
            else:
                if len(self.operador) != 0 :  #x = 5 + 7 - (8)-> esto seria
                    varTemp = self.variablesTemporales.pop() #saco la variabler anterior, en este caso t0
                    operador = self.operador.pop() #el operador que le agregue en el coso muldiv
                    
                    
                    self.archivoCodigoIntermedio.write("t" + str(self.contadorVarTemporales) + " = "+ varTemp + operador + ctx.getChild(0).getText()+ '\n')      
                    print("t" + str(self.contadorVarTemporales) + " = "+ varTemp + operador + ctx.getChild(0).getText()) #t1 = t0 - 7
            
                    self.variablesTemporales.append("t" + str(self.contadorVarTemporales)) #appendeo t0

                    if ctx.getChild(1).getChildCount() != 0:
                        self.variablesTemporales.append("t" + str(self.contadorVarTemporales)) #appendeo t0
                        self.contadorVarTemporales = self.contadorVarTemporales + 1 #no appendeo ninguna variable, solo sumo
                        self.visitPartesumaresta(ctx.getChild(1)) #x = 5 * 6 (+ 1)-> le paso esta parte
                        return
                    self.contadorVarTemporales = self.contadorVarTemporales + 1 #no appendeo ninguna variable, solo sumo
                    return

                if ctx.getChild(1).getChildCount() != 0:
                    # x = (4 + 5) ->esto queiro partir + 7
                    op = ctx.getChild(1).getChild(0).getText()
                    primNum = ctx.getChild(0).getText()
                    segNum = ctx.getChild(1).getChild(1).getChild(0).getText()
                    
                    self.archivoCodigoIntermedio.write("t" + str(self.contadorVarTemporales) + " = "+ primNum + op + segNum + '\n')      
                    print("t" + str(self.contadorVarTemporales) + " = "+ primNum + op + segNum ) #t0 = 4+5
                
                    self.variablesTemporales.append("t" + str(self.contadorVarTemporales)) #appendeo t0
                    self.contadorVarTemporales = self.contadorVarTemporales +1  
            
                    self.visitPartesumaresta(ctx.getChild(1).getChild(1).getChild(1)) #x = 5 * 6 (+ 1)-> le paso esta parte
                
                
         

    def visitPartesumaresta(self, ctx):
        print("Visitando la parte de suma resta")
        self.operador.append(ctx.getChild(0).getText())  #le paso arriba el operador de suma para que recuerde que operacion esta haciendo
        #print(ctx.getText())
        self.visitTermino4(ctx.getChild(1))  #visito el que termino de la derecha
        
        return None

    
    def visitTermino5(self, ctx):
        print('parte termino 5')

        print(len(ctx.getText()))
        if len(ctx.getText()) == 3 and '*' not in self.operador and '/' not in self.operador : #x = ( 5 * 6 ) -> primera vez
            print("primer caso")
            
            self.archivoCodigoIntermedio.write("t" + str(self.contadorVarTemporales) + " = "+ ctx.getText()+ '\n' )      
            print("t" + str(self.contadorVarTemporales) + " = "+ ctx.getText())
            
            self.variablesTemporales.append("t" + str(self.contadorVarTemporales)) #lo anado a la pila porque despues a esto lo multiplico por 7
            self.contadorVarTemporales = self.contadorVarTemporales +1
            return
        if ctx.getChild(1).getChildCount() == 0 and len(self.operador)!=0:  #x = 5 * 7 * (8)-> esto seria, como el caso base ponele
            if self.operador[-1] == '*' or self.operador[-1] == '/':
                varTemp = self.variablesTemporales.pop() #saco la variabler anterior, en este caso t0
                operador = self.operador.pop() #el operador que le agregue en el coso muldiv
                
                self.archivoCodigoIntermedio.write("t" + str(self.contadorVarTemporales) + " = "+ varTemp + operador + ctx.getChild(0).getText()+ '\n')      
                print("t" + str(self.contadorVarTemporales) + " = "+ varTemp + operador + ctx.getChild(0).getText()) #t1 = t0*7
                
                if len(ctx.getChild(1).getText()) >=2: #x = 5 * 8 * 7
                    self.variablesTemporales.append("t" + str(self.contadorVarTemporales)) 
                    self.contadorVarTemporales = self.contadorVarTemporales + 1
                    self.visitPartemuldivmod(ctx.getChild(1)) #x = 5 * 6 (* 1 * 8)-> parte mul
                else:
                    self.variablesTemporales.append("t" + str(self.contadorVarTemporales)) 
                    self.contadorVarTemporales = self.contadorVarTemporales + 1 #no appendeo ninguna variable, solo sumo
        else:    
            if len(ctx.getChild(1).getText()) > 2: #x = 5 * 8 * 7
                if len(self.operador) == 0 or self.operador[-1] == '+' or self.operador[-1] == '-': #primera vuelta
                    op = ctx.getChild(1).getChild(0).getText() #*
                    primNum = ctx.getChild(0).getText() #5
                    segNum = ctx.getChild(1).getChild(1).getChild(0).getText() #8
                    # siempre va a ser distinto en la primera parte porque hay que partir en 3 primero

                    self.archivoCodigoIntermedio.write("t" + str(self.contadorVarTemporales) + " = "+ primNum + op + segNum+ '\n')      
                    print("t" + str(self.contadorVarTemporales) + " = "+ primNum + op + segNum ) #t0 = 5*8
                    
                    self.variablesTemporales.append("t" + str(self.contadorVarTemporales)) #lo anado a la pila porque despues a esto lo multiplico por 7
                    self.contadorVarTemporales =self.contadorVarTemporales + 1
                    self.visitPartemuldivmod(ctx.getChild(1).getChild(1).getChild(1)) #x = 5 * 8 (* 7)-> parte mul
                else:
                    self.visitPartemuldivmod(ctx.getChild(1)) #x = 5 * 6 (* 1 * 8)-> parte mul
            
        return
            
    
    def visitPartemuldivmod(self, ctx):
        print("Visitando la parte de muldiv")
        #print(ctx.getText())
        self.operador.append(ctx.getChild(0).getText())  #le paso arriba el operador de suma para que recuerde que operacion esta haciendo
        self.visitTermino5(ctx.getChild(1))  #visito el que termino de la derecha
        
        return None      
            

        

    
    
    """
    def visitTerminal(self, node):
        print("Token " + node.getText())
        return super().visitTerminal(node)
    
    
    def visitBloque(self, ctx: compiladoresParser.BloqueContext):
        print("nuevo contexto")
        print(ctx.getText())
        return super().visitInstrucciones(ctx.getChild(1))
    
    def visitPrograma(self, ctx: compiladoresParser.ProgramaContext):
        print("=" *20)
        print("comienza a caminar")
        return super().visitPrograma(ctx)
    
    #def visitAsignacion(self, ctx: compiladoresParser.AsignacionContext):
     #   print (ctx.getChild(0).getText() + " - " + ctx.getChild(1).getText())
      #  return None

    # def visitAsign (self, ctx: compiladoresParser.DeclaracionContext):
    #     print (ctx.getChild(0).getText() + " - " + ctx.getChild(1).getText())
    #     return None
    
    def visitTermino5(self, ctx):
        print(ctx.getText())
        #print("t"+str(self.contadorVarTemporales) + "="+ctx.getText())
        #self.variablesTemporales.append(self.contadorVarTemporales)
        #self.contadorVarTemporales = self.contadorVarTemporales + 1
        #return super().visitTermino5(ctx)

    def visitTermino4(self, ctx):
        #print(ctx.getText())
        return super().visitTermino4(ctx)
      
   
    def visitPartemuldivmod(self, ctx):
        print("Aca se esta multiplicando/dividiendo " + ctx.getText())
        return super().visitPartemuldivmod(ctx)

    def visitPartesumaresta(self, ctx):
        print("Aca se esta sumando/restando " + ctx.getText())
        return super().visitPartesumaresta(ctx)
     
    def visitBloque(self, ctx: compiladoresParser.BloqueContext):
        print("nuevo contexto")
        print(ctx.getText())
        return super().visitInstrucciones(ctx.getChild(1))
        """
    
    