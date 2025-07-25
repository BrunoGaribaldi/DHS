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
    operadorSumaResta = []
    operadorMulDiv = []
    varAAsignar = ''
    
    #etiquetas
    etiquetasFunciones = {} #va a ser un diccionario, almacena el nombre de variable  y la dir de label
    contadorEtiquetas = 0
    
    #funciones
    argumentosFunciones = []
    varRetorno = []
    
    #archivo
    archivoCodigoIntermedio = open("./output/codigoIntermedio.txt", "w")
    archivoCodigoIntermedioComentarios = open("./output/codigoIntermedioComentarios.txt", "w")

    
    def visitPrograma(self, ctx: compiladoresParser.ProgramaContext):
        return super().visitPrograma(ctx)
      
    def visitReturn(self, ctx):
        super().visitReturn(ctx)
        self.varRetorno.append(ctx.getChild(1).getText())
    
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
        self.archivoCodigoIntermedioComentarios.write('\n--- Asignacion variable ' + ctx.getChild(0).getText() +  ' linea ' + str(ctx.start.line) + ' ---\n')

        if ctx.llamadafunc(): #estoy en una funcion
           self.visitLlamadafunc(ctx.getChild(2))
           
           self.archivoCodigoIntermedio.write('pop ' + ctx.getChild(0).getText() + '\n')
           self.archivoCodigoIntermedioComentarios.write('pop ' + ctx.getChild(0).getText() + '\n \n')
        else:
            opl = ctx.getChild(2)
            parterelacion= opl.getChild(0).getChild(0).getChild(0).getChild(1)
            partesumaresta = opl.getChild(0).getChild(0).getChild(0).getChild(0).getChild(1)
            partemuldiv = opl.getChild(0).getChild(0).getChild(0).getChild(0).getChild(0).getChild(1)
            if parterelacion.getChildCount() == 0 and partesumaresta.getChildCount() == 0 and partemuldiv.getChildCount() == 0 :
                self.archivoCodigoIntermedio.write(ctx.getText()+ '\n')      
                self.archivoCodigoIntermedioComentarios.write(ctx.getText()+ '\n')      
                print(ctx.getText())
    
            
            else:
                self.visitOpal(ctx.getChild(2))
                #print(self.variablesTemporales)
                
                if len(self.variablesTemporales) > 1 and len(self.operadorSumaResta) != 0: #por ahi cuando hay sumas de terminos quedan por sumar 
                    var = self.variablesTemporales.pop()
                    primVar = self.variablesTemporales.pop()
                    op = self.operadorSumaResta.pop()
                    
                    self.archivoCodigoIntermedioComentarios.write("t" + str(self.contadorVarTemporales) + " = "+ primVar + ' ' + op + ' '  + var + '\n')      
                    self.archivoCodigoIntermedio.write("t" + str(self.contadorVarTemporales) + " = "+ primVar + ' ' + op + ' '  + var + '\n')      
                    
                    print("t" + str(self.contadorVarTemporales) + " = "+ primVar+ ' ' + op  + ' ' + var )
                
                    self.variablesTemporales.append("t" + str(self.contadorVarTemporales)) #hago el append para que salte despues
                    self.contadorVarTemporales = self.contadorVarTemporales + 1    
                
                var = self.variablesTemporales.pop()    
                print(ctx.getChild(0).getText() + ' = ' + var)
                self.archivoCodigoIntermedioComentarios.write(ctx.getChild(0).getText() + ' = ' + var + '\n \n')
                self.archivoCodigoIntermedio.write(ctx.getChild(0).getText() + ' = ' + var + '\n')
                
            """ if len(ctx.getChild(2).getText()) != 1:
                self.visitOpal(ctx.getChild(2))
                #print(self.variablesTemporales)
                
                if len(self.variablesTemporales) > 1 and len(self.operadorSumaResta) != 0: #por ahi cuando hay sumas de terminos quedan por sumar 
                    var = self.variablesTemporales.pop()
                    primVar = self.variablesTemporales.pop()
                    op = self.operadorSumaResta.pop()
                    
                    self.archivoCodigoIntermedioComentarios.write("t" + str(self.contadorVarTemporales) + " = "+ primVar + ' ' + op + ' '  + var + '\n')      
                    self.archivoCodigoIntermedio.write("t" + str(self.contadorVarTemporales) + " = "+ primVar + ' ' + op + ' '  + var + '\n')      
                    
                    print("t" + str(self.contadorVarTemporales) + " = "+ primVar+ ' ' + op  + ' ' + var )
                
                    self.variablesTemporales.append("t" + str(self.contadorVarTemporales)) #hago el append para que salte despues
                    self.contadorVarTemporales = self.contadorVarTemporales + 1    
                
                var = self.variablesTemporales.pop()    
                print(ctx.getChild(0).getText() + ' = ' + var)
                self.archivoCodigoIntermedioComentarios.write(ctx.getChild(0).getText() + ' = ' + var + '\n \n')
                self.archivoCodigoIntermedio.write(ctx.getChild(0).getText() + ' = ' + var + '\n')
                
            
            else:
                self.archivoCodigoIntermedio.write(ctx.getText()+ '\n')      
                self.archivoCodigoIntermedioComentarios.write(ctx.getText()+ '\n')      
                print(ctx.getText())
     """
    
    def visitFunc(self, ctx):
        labelFuncion = ctx.getChild(1).getText()
        dirRetorno = 't' + str(self.contadorVarTemporales)
        self.contadorEtiquetas = self.contadorEtiquetas + 1
        self.contadorVarTemporales = self.contadorVarTemporales + 1
        
         
        self.archivoCodigoIntermedioComentarios.write('\n--- Funcion --- \n') 
        
        self.archivoCodigoIntermedioComentarios.write('label ' + labelFuncion + '\n')
        self.archivoCodigoIntermedio.write('label ' + labelFuncion + '\n')
        
        
        self.archivoCodigoIntermedioComentarios.write('pop ' + dirRetorno + '\n') #direccion de retorno, me llega l1 pero yo lo nombro t0
        self.archivoCodigoIntermedio.write('pop ' + dirRetorno + '\n') #direccion de retorno, me llega l1 pero yo lo nombro t0
        
        
        #voy a argumentos para que escriban pop ...
        self.visitArgumentosf(ctx.getChild(3))
        
        #argumentosenorden
        while self.argumentosFunciones:
            arg = self.argumentosFunciones.pop()
            self.archivoCodigoIntermedioComentarios.write('pop ' + arg + '\n')
            self.archivoCodigoIntermedio.write('pop ' + arg + '\n')

        self.visitBloqueespecial(ctx.getChild(5)) #visito las instrucciones
        self.archivoCodigoIntermedio.write('label end_' + labelFuncion+ '\n')
        self.archivoCodigoIntermedioComentarios.write('label end_' + labelFuncion+ '\n')
        
        #pusheamos a la pila la variable de retorno
        if len(self.varRetorno) != 0:
            varRetorno = self.varRetorno.pop()
            self.archivoCodigoIntermedioComentarios.write('push ' + varRetorno + '\n')
            self.archivoCodigoIntermedio.write('push ' + varRetorno + '\n')
        
        self.archivoCodigoIntermedioComentarios.write('jump ' + dirRetorno + '\n') #saltoa direccion de retorno
        self.archivoCodigoIntermedio.write('jump ' + dirRetorno + '\n') #saltoa direccion de retorno
                        
    
    def visitArgumentosf(self, ctx):
        if ctx.getChildCount() != 0: #puede no tener argumentos
            self.visitFuncargumentos(ctx.getChild(0)) #siempre va a tener un argumetno, lo visito
            if ctx.getChildCount() > 1:
                self.visitArgumentosf(ctx.getChild(2)) #si tiene mas, hago una especie de recursividad
            
            
    
    def visitFuncargumentos(self, ctx):
        self.argumentosFunciones.append(ctx.getChild(1).getText())
        #self.archivoCodigoIntermedioComentarios.write('pop ' + ctx.getChild(1).getText() + '\n')
      
    
         
    
    #-------------------parte de llamada a funciones-------------------------------------# 
    def visitLlamadafunc(self, ctx):
        self.archivoCodigoIntermedioComentarios.write('\n--- Llamada a funcion --- \n') 
        
        self.visitArgumentosllamada(ctx.getChild(2))
        
        labelLlamada = 'l' + str(self.contadorEtiquetas)
        self.contadorEtiquetas = self.contadorEtiquetas + 1 
        
        labelFuncion = ctx.getChild(0).getText()
        
        
        
        self.etiquetasFunciones[ctx.getChild(0).getText()] = labelFuncion 
        self.archivoCodigoIntermedioComentarios.write('push ' + labelLlamada + '\n') #cuando se ejecute la funcion vuelve a ese label
        self.archivoCodigoIntermedio.write('push ' + labelLlamada + '\n') #cuando se ejecute la funcion vuelve a ese label
        
        self.archivoCodigoIntermedioComentarios.write('jump ' + labelFuncion +  '\n') 
        self.archivoCodigoIntermedio.write('jump ' + labelFuncion +  '\n') 
        
        self.archivoCodigoIntermedioComentarios.write('label ' + labelLlamada + '\n') 
        self.archivoCodigoIntermedio.write('label ' + labelLlamada + '\n') 


        print('jmp ' + labelFuncion)
        
        
    
    def visitArgumentosllamada(self, ctx):
        if ctx.getChildCount() != 0: #puede no tener argumentos
            self.visitLlamargumentos(ctx.getChild(0)) #siempre va a tener un argumetno, lo visito
            if ctx.getChildCount() > 1:
                print('entre')
                self.visitArgumentosllamada(ctx.getChild(2)) #si tiene mas, hago una especie de recursividad
    
    def visitLlamargumentos(self, ctx):
        self.archivoCodigoIntermedioComentarios.write('push ' + ctx.getChild(0).getText() + '\n')
        self.archivoCodigoIntermedio.write('push ' + ctx.getChild(0).getText() + '\n')
    def visitIif(self, ctx):
        print('Entre a if')
        self.archivoCodigoIntermedioComentarios.write('\n--- IF linea ' + str(ctx.start.line) + ' --- \n') 
        
        self.visitOpal(ctx.getChild(2))
        # t0 = x > 1
        varComp = self.variablesTemporales.pop() #tiene el t0
        #creamos la etiqueta donde va a saltar
        #self.etiquetas.append('l' + str(self.contadorEtiquetas))
        etiqSaltar = "l" + str(self.contadorEtiquetas)  #si no hay else
        etiqSaltarElse = "l" + str(self.contadorEtiquetas + 1)  #si  hay else
        
        if ctx.getChildCount() > 5: #hay else
            self.archivoCodigoIntermedioComentarios.write("ifntjmp " + varComp + " , " + etiqSaltarElse + '\n')
            self.archivoCodigoIntermedio.write("ifntjmp " + varComp + " , " + etiqSaltarElse + '\n')
            
            print("ifntjmp " + varComp + ", " + etiqSaltar)
        
        else:
            self.archivoCodigoIntermedioComentarios.write("ifntjmp " + varComp + " , " + etiqSaltar + '\n')
            self.archivoCodigoIntermedio.write("ifntjmp " + varComp + " , " + etiqSaltar + '\n')
            
            print("ifntjmp " + varComp + ", " + etiqSaltar)
            
            
          
        self.contadorEtiquetas = self.contadorEtiquetas + 1 
        self.visitInstruccion(ctx.getChild(4))
        if ctx.getChildCount() > 5: #hay un else
            
            self.archivoCodigoIntermedioComentarios.write("jump " + etiqSaltar+ '\n')     
            self.archivoCodigoIntermedio.write("jump " + etiqSaltar+ '\n')     
            print("jmp " + etiqSaltarElse) #ya entro al if, escapo dl else
            
            self.archivoCodigoIntermedioComentarios.write('label '+ etiqSaltarElse+ '\n')     
            self.archivoCodigoIntermedio.write('label '+ etiqSaltarElse+ '\n')            
            print('label '+ etiqSaltar)
            
            self.visitInstruccion(ctx.getChild(6))
        
            
        self.archivoCodigoIntermedioComentarios.write('label '+ etiqSaltar+ '\n')     
        self.archivoCodigoIntermedio.write('label '+ etiqSaltar+ '\n')     
        print('label '+ etiqSaltar) #seria como el fin del bloque del if
        
        self.contadorEtiquetas = self.contadorEtiquetas + 1
        


    def visitIfor(self, ctx):
        #for ( i = 0 ; i< x ; i = i + 1 ) y = z * x;
        self.archivoCodigoIntermedioComentarios.write('\n--- For linea ' + str(ctx.start.line) + ' ---\n')

        self.visitAsignacion(ctx.getChild(2)) #visito i = 0
        labelEvalCond = 'l' + str(self.contadorEtiquetas) #label en el que evaluo si x < 0
        
        self.archivoCodigoIntermedioComentarios.write('label ' + labelEvalCond+ '\n')
        self.archivoCodigoIntermedio.write('label ' + labelEvalCond+ '\n')
        
        print('label ' + labelEvalCond)
        
        self.contadorEtiquetas = self.contadorEtiquetas + 1
        labelFinFor = 'l' + str(self.contadorEtiquetas) #cuando salga del for me vot aca
        self.visitCond(ctx.getChild(4)) #entro a la condicion
        
        #sies falso salto al fin del dor
        self.archivoCodigoIntermedioComentarios.write('ifntjmp t' + str(self.contadorVarTemporales - 1) + ' , l' + str(self.contadorEtiquetas)+ '\n')
        self.archivoCodigoIntermedio.write('ifntjmp t' + str(self.contadorVarTemporales - 1) + ' , l' + str(self.contadorEtiquetas)+ '\n')
        print('ifntjmp t' + str(self.contadorVarTemporales - 1) + ', l' + str(self.contadorEtiquetas))
        
        self.visitInstruccion(ctx.getChild(8)) #visito el bloque
        self.visitIter(ctx.getChild(6)) #una vez finalizaod el bloque incremento i por ejemolo
        
        self.archivoCodigoIntermedio.write('jump ' + labelEvalCond + '\n')
        self.archivoCodigoIntermedioComentarios.write('jump ' + labelEvalCond + '\n')
        print('jmp ' + labelEvalCond)
        
        self.archivoCodigoIntermedio.write('label ' + labelFinFor + '\n')
        self.archivoCodigoIntermedioComentarios.write('label ' + labelFinFor + '\n')
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
                self.archivoCodigoIntermedioComentarios.write("t" + str(self.contadorVarTemporales) + " = "+ ctx.getText()+ '\n')      
                print("t" + str(self.contadorVarTemporales) + " = "+ ctx.getText())
                
                self.variablesTemporales.append("t" + str(self.contadorVarTemporales)) #hago el append para que salte despues
                self.contadorVarTemporales = self.contadorVarTemporales + 1    

                return
    
   
    def visitTermino4(self, ctx):
        print('parte termino 4')
        
        #primero me fijo tema parentesits
        if ctx.getChild(0).getChild(0).getChild(0).getChild(0).getChildCount() == 3: 
            self.visitOpal(ctx.getChild(0).getChild(0).getChild(0).getChild(0).getChild(1))
            if ctx.getChild(0).getChild(1).getChildCount() != 0: #si hay otro termino al lado lo visito
                self.visitPartemuldivmod(ctx.getChild(0).getChild(1))
            if ctx.getChild(1).getChildCount() != 0: #si hay otro termino al lado lo visito
                self.visitPartesumaresta(ctx.getChild(1))
        else:
        #primero tengo que chequear que no haya ninguna multiplicacion
            if ctx.getChild(0).getChild(1).getChildCount() != 0: #x = 2* 5 + 1
                self.visitTermino5(ctx.getChild(0))
                """ if len(self.operadorSumaResta) != 0 and len(self.variablesTemporales) > 1 and ctx.getChild(1).getChildCount() == 0: # x = (1 * 2)-> en pila de variables + (8 * 9)-> en pila de variables
                    segNum = self.variablesTemporales.pop()    
                    primNum = self.variablesTemporales.pop()
                    op = self.operadorSumaResta.pop()    
            
                    self.archivoCodigoIntermedioComentarios.write("t" + str(self.contadorVarTemporales) + " = "+ primNum+ ' ' + op+ ' ' + segNum+ '\n')      
                    print("t" + str(self.contadorVarTemporales) + " = "+ primNum + op + segNum ) #t0 = 5*8
                        
                    self.variablesTemporales.append("t" + str(self.contadorVarTemporales)) #lo anado a la pila porque despues a esto lo multiplico por 7
                    self.contadorVarTemporales =self.contadorVarTemporales + 1
                 """
                if ctx.getChild(1).getChildCount() != 0:        
                    self.visitPartesumaresta(ctx.getChild(1))
            
            else:
                if len(self.operadorSumaResta) != 0: #caso base, ejemplo x = 2  + 1 - (7) -> esto me llega
                    
                    varTemp = self.variablesTemporales.pop() 
                    operador = self.operadorSumaResta.pop() 
                    
                    self.archivoCodigoIntermedio.write("t" + str(self.contadorVarTemporales) + " = "+ varTemp+ ' ' + operador+ ' ' + ctx.getChild(0).getText()+ '\n')      
                    self.archivoCodigoIntermedioComentarios.write("t" + str(self.contadorVarTemporales) + " = "+ varTemp+ ' ' + operador+ ' ' + ctx.getChild(0).getText()+ '\n')      
                    print("t" + str(self.contadorVarTemporales) + " = "+ varTemp + ' ' + operador+ ' ' + ctx.getChild(0).getText()) #t1 = t0*7
                
                    self.variablesTemporales.append("t" + str(self.contadorVarTemporales)) #lo anado a la pila porque despues a esto lo multiplico por 7
                    self.contadorVarTemporales = self.contadorVarTemporales +1
                    
                    if ctx.getChild(1).getChildCount() != 0:
                        self.visitPartesumaresta(ctx.getChild(1))

                
                else:
                    #si llego hasta aca es porque tiene mas de dosterminos x = 2 + 3 + 2 + 5
                    if ctx.getChild(1).getChild(1).getChild(1).getChildCount() == 0: #x = 2 + 3
                        
                        if ctx.getChild(1).getChild(1).getChild(0).getChild(1).getChildCount() != 0: #aca hay una multiplicacion x = 1 + 5*7

                            primNum = ctx.getChild(0).getText()
                            
                            self.archivoCodigoIntermedio.write("t" + str(self.contadorVarTemporales) + " = "+ primNum+  '\n')      
                            self.archivoCodigoIntermedioComentarios.write("t" + str(self.contadorVarTemporales) + " = "+ primNum+  '\n')      
                            print("t" + str(self.contadorVarTemporales) + " = "+ primNum ) #t0 = 5*8
                        
                            self.variablesTemporales.append("t" + str(self.contadorVarTemporales)) #lo anado a la pila porque despues a esto lo multiplico por 7
                            self.contadorVarTemporales =self.contadorVarTemporales + 1
                            
                            #self.visitTermino5(ctx.getChild(1).getChild(1).getChild(0)) #voy a la multiplicacion
                            self.visitPartesumaresta(ctx.getChild(1))
                            #hago la suma de los dos terminos
                            """ segNum = self.variablesTemporales.pop()    
                            primNum = self.variablesTemporales.pop()
                            op = self.operadorSumaResta.pop()    
            
                            self.archivoCodigoIntermedioComentarios.write("t" + str(self.contadorVarTemporales) + " = "+ primNum+ ' ' + op+ ' ' + segNum+ '\n')      
                            print("t" + str(self.contadorVarTemporales) + " = "+ primNum + op + segNum ) #t0 = 5*8
                        
                            self.variablesTemporales.append("t" + str(self.contadorVarTemporales)) #lo anado a la pila porque despues a esto lo multiplico por 7
                            self.contadorVarTemporales =self.contadorVarTemporales + 1 """
                    
                        else:
                            segNum = ctx.getChild(1).getChild(1).getChild(0).getText()    
                            primNum = ctx.getChild(0).getText()
                            op = ctx.getChild(1).getChild(0).getText()    
            
                            self.archivoCodigoIntermedio.write("t" + str(self.contadorVarTemporales) + " = "+ primNum+ ' ' + op+ ' ' + segNum+ '\n')      
                            self.archivoCodigoIntermedioComentarios.write("t" + str(self.contadorVarTemporales) + " = "+ primNum+ ' ' + op+ ' ' + segNum+ '\n')      
                            print("t" + str(self.contadorVarTemporales) + " = "+ primNum + op + segNum ) #t0 = 5*8
                        
                            self.variablesTemporales.append("t" + str(self.contadorVarTemporales)) #lo anado a la pila porque despues a esto lo multiplico por 7
                            self.contadorVarTemporales =self.contadorVarTemporales + 1
                    
                    else: #x = (2 + 6)-> tengo que partir esto + 7
                            segNum = ctx.getChild(1).getChild(1).getChild(0).getText()    
                            primNum = ctx.getChild(0).getText()
                            op = ctx.getChild(1).getChild(0).getText()    
            
                            self.archivoCodigoIntermedio.write("t" + str(self.contadorVarTemporales) + " = "+ primNum+ ' ' + op+ ' ' + segNum+ '\n')      
                            self.archivoCodigoIntermedioComentarios.write("t" + str(self.contadorVarTemporales) + " = "+ primNum+ ' ' + op+ ' ' + segNum+ '\n')      
                            print("t" + str(self.contadorVarTemporales) + " = "+ primNum + op + segNum ) #t0 = 5*8
                        
                            self.variablesTemporales.append("t" + str(self.contadorVarTemporales)) #lo anado a la pila porque despues a esto lo multiplico por 7
                            self.contadorVarTemporales =self.contadorVarTemporales + 1
                        
                            self.visitPartesumaresta(ctx.getChild(1).getChild(1).getChild(1))
                        
                        
                
         
             
         

    def visitPartesumaresta(self, ctx):
        print("Visitando la parte de suma resta")
        self.operadorSumaResta.append(ctx.getChild(0).getText())  #le paso arriba el operador de suma para que recuerde que operacion esta haciendo
        #print(ctx.getText())
        self.visitTermino4(ctx.getChild(1))  #visito el que termino de la derecha
        
        return None

    
    def visitTermino5(self, ctx):
        print('parte termino 5')
       #comoel caso base, x = 5 * 7 * (1) -> esto seria
        if ctx.getChild(1).getChildCount() == 0:
            varTemp = self.variablesTemporales.pop() #saco la variabler anterior, en este caso t0
            operador = self.operadorMulDiv.pop() #el operador que le agregue en el coso muldiv
                
            self.archivoCodigoIntermedio.write("t" + str(self.contadorVarTemporales) + " = "+ varTemp+ ' ' + operador+ ' ' + ctx.getChild(0).getText()+ '\n')      
            self.archivoCodigoIntermedioComentarios.write("t" + str(self.contadorVarTemporales) + " = "+ varTemp+ ' ' + operador+ ' ' + ctx.getChild(0).getText()+ '\n')      
            print("t" + str(self.contadorVarTemporales) + " = "+ varTemp + ' ' + operador+ ' ' + ctx.getChild(0).getText()) #t1 = t0*7
            
            self.variablesTemporales.append("t" + str(self.contadorVarTemporales)) #lo anado a la pila porque despues a esto lo multiplico por 7
            self.contadorVarTemporales = self.contadorVarTemporales +1
                
        
        else:
            if ctx.getChild(1).getChild(1).getChild(1).getChildCount() == 0 and len(self.operadorMulDiv) == 0: #x = 2 * 5 ->solo esto
                self.archivoCodigoIntermedio.write("t" + str(self.contadorVarTemporales) + " = "+ ctx.getText()+ '\n' )      
                self.archivoCodigoIntermedioComentarios.write("t" + str(self.contadorVarTemporales) + " = "+ ctx.getText()+ '\n' )      
                print("t" + str(self.contadorVarTemporales) + " = "+ ctx.getText())
            
                self.variablesTemporales.append("t" + str(self.contadorVarTemporales)) #lo anado a la pila porque despues a esto lo multiplico por 7
                self.contadorVarTemporales = self.contadorVarTemporales +1
                return

            if ctx.getChild(1).getChildCount() != 0 and len(self.operadorMulDiv) != 0: #x = 2 * 1 * (8) * 2
                varTemp = self.variablesTemporales.pop() #saco la variabler anterior, en este caso t0
                operador = self.operadorMulDiv.pop() #el operador que le agregue en el coso muldiv
                
                self.archivoCodigoIntermedio.write("t" + str(self.contadorVarTemporales) + " = "+ varTemp+ ' ' + operador+ ' ' + ctx.getChild(0).getText()+ '\n')      
                self.archivoCodigoIntermedioComentarios.write("t" + str(self.contadorVarTemporales) + " = "+ varTemp+ ' ' + operador+ ' ' + ctx.getChild(0).getText()+ '\n')      
                print("t" + str(self.contadorVarTemporales) + " = "+ varTemp + ' ' + operador+ ' ' + ctx.getChild(0).getText()) #t1 = t0*7
            
                self.variablesTemporales.append("t" + str(self.contadorVarTemporales)) #lo anado a la pila porque despues a esto lo multiplico por 7
                self.contadorVarTemporales = self.contadorVarTemporales +1
                
                self.visitPartemuldivmod(ctx.getChild(1)) #x = 5 * 8 (* 7) / 7-> parte mul
                           
            else: # tiene mas de 2 terminos x = 2 * 7 / 2 * 1
                
                op = ctx.getChild(1).getChild(0).getText() #*
                primNum = ctx.getChild(0).getText() #2
                segNum = ctx.getChild(1).getChild(1).getChild(0).getText() #7
                # siempre va a ser distinto en la primera parte porque hay que partir en 3 primero

                self.archivoCodigoIntermedio.write("t" + str(self.contadorVarTemporales) + " = "+ primNum+ ' ' + op+ ' ' + segNum+ '\n')      
                self.archivoCodigoIntermedioComentarios.write("t" + str(self.contadorVarTemporales) + " = "+ primNum+ ' ' + op+ ' ' + segNum+ '\n')      
                print("t" + str(self.contadorVarTemporales) + " = "+ primNum + op + segNum ) #t0 = 5*8
                    
                self.variablesTemporales.append("t" + str(self.contadorVarTemporales)) #lo anado a la pila porque despues a esto lo multiplico por 7
                self.contadorVarTemporales =self.contadorVarTemporales + 1
                
                self.visitPartemuldivmod(ctx.getChild(1).getChild(1).getChild(1)) #x = 5 * 8 (* 7)-> parte mul
                
       
       
    def visitPartemuldivmod(self, ctx):
        print("Visitando la parte de muldiv")
        #print(ctx.getText())
        self.operadorMulDiv.append(ctx.getChild(0).getText())  #le paso arriba el operador de suma para que recuerde que operacion esta haciendo
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
    
    