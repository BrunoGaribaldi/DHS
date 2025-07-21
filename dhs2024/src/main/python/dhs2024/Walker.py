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

    contadorVarTemporales = 0
    variablesTemporales = []
    operador = []
    varAAsignar = ''

    
    def visitPrograma(self, ctx: compiladoresParser.ProgramaContext):
         return super().visitPrograma(ctx)
      

  
    def visitAsignacion(self, ctx):
        self.varAAsignar = ctx.getChild(0).getText()
        print(self.varAAsignar)
        return self.visitOpal(ctx.getChild(2))
    
    
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
        return self.visitTermino4(ctx.getChild(0))
    
    #prueba

    def visitTermino4(self, ctx):
        print('parte termino 4')
        """ if ctx.getChild(0).getChild(1).getChildCount() != 0: #va a termino 5 y se fija en la parte muldiv
            self.visitTermino5(ctx.getChild(0))  #miro para ver si hay una multiplicacion o division primero
         """
        
        if ctx.getChild(0).getChild(1).getChildCount() != 0 : #si hay alguna multiplicacion visito esto
            self.visitTermino5(ctx.getChild(0))
            self.visitPartesumaresta(ctx.getChild(1))
            print(len(self.operador))
            return
                        
        #caso base 
        if ctx.getChild(1).getChildCount() == 0 and len(self.operador) != 0:  #x = 5 + 7 - (8)-> esto seria
            varTemp = self.variablesTemporales.pop() #saco la variabler anterior, en este caso t0
            operador = self.operador.pop() #el operador que le agregue en el coso muldiv
            print("t" + str(self.contadorVarTemporales) + " = "+ varTemp + operador + ctx.getChild(0).getText()) #t1 = t0 - 7
            self.contadorVarTemporales = self.contadorVarTemporales + 1 #no appendeo ninguna variable, solo sumo
            return
        
        if len(ctx.getText()) == 3 and '+' in ctx.getText() and len(self.operador) == 0: #x = 5 + 6 -> solamente en estos casos
            print("t" + str(self.contadorVarTemporales) + " = "+ ctx.getText())
            self.contadorVarTemporales =+ 1
            return
        else:
            #la primera particion ponele
            if len(self.variablesTemporales) == 0  : # x = (4 + 5) ->esto queiro partir + 7
                op = ctx.getChild(1).getChild(0).getText()
                primNum = ctx.getChild(0).getText()
                segNum = ctx.getChild(1).getChild(1).getChild(0).getText()
                print("t" + str(self.contadorVarTemporales) + " = "+ primNum + op + segNum ) #t0 = 4+5
                
            
                self.variablesTemporales.append("t" + str(self.contadorVarTemporales)) #appendeo t0
                self.contadorVarTemporales = self.contadorVarTemporales +1  
                
                if ctx.getChild(1).getChild(1).getChild(1).getChildCount()!=0:
                    self.visitPartesumaresta(ctx.getChild(1).getChild(1).getChild(1)) #x = 5 * 6 (+ 1)-> le paso esta parte
                
            if ctx.getChild(1).getChildCount() == 0 and len(self.operador) == 0: #cuando es solo multiplcacion por ejempli
                return
 
            else:
                if ctx.getChild(1).getChildCount() == 0 and len(self.operador) == 0:
                    varTemp = self.variablesTemporales.pop() #saco la variabler anterior, en este caso t0
                    operador = self.operador.pop() #el operador que le agregue en el coso muldiv
                    print("t" + str(self.contadorVarTemporales) + " = "+ varTemp + operador + ctx.getChild(0).getText()) #t1 = t0 - 7
                    self.variablesTemporales.append("t" + str(self.contadorVarTemporales)) 
                    self.contadorVarTemporales = self.contadorVarTemporales + 1 #no appendeo ninguna variable, solo sumo
     
                        
                
                
                
                
        

            
        """ else: 
            
            if len(ctx.getText()) == 3 and '+' in ctx.getText(): #x = 5 + 6 -> solamente en estos casos
                print("t" + str(self.contadorVarTemporales) + " = "+ ctx.getText())
                self.contadorVarTemporales =+ 1
            
            if ctx.getChild(1).getChild(1).getChild(1).getChildCount() != 0:  #x = 5 + 7 - 8
                op = ctx.getChild(1).getChild(0).getText()
                primNum = ctx.getChild(0).getText()
                segNum = ctx.getChild(1).getChild(1).getChild(0).getText()
                
                if len(self.variablesTemporales) != 0: # aca es si entro y habia una multiplicacion por ejemplo
                    #ejemplo x = 5 * 9 + 7 / 1
                    if len(segNum) > 1 : #x = 5 * 9 + (7 / 1) ->segnum
                        self.visitTermino5(ctx.getChild(1).getChild(1).getChild(0))  #si hay una multiplicacion adentro 
                    #en el termino 5 imprimio t0 = 5*9 y t1 = 7/1
                    # en la stack entonces tengo t1,t0 
                    segNum = self.variablesTemporales.pop() # saco la variable t1
                    primNum = self.variablesTemporales.pop() #saco la variable t0
                    print("t" + str(self.contadorVarTemporales) + " = "+ primNum + op + segNum ) # t0 = 5*9; t1 = t0 + 7
                
                else:
                    print("t" + str(self.contadorVarTemporales) + " = "+ primNum + op + segNum ) 
            
                self.variablesTemporales.append("t" + str(self.contadorVarTemporales))
                self.contadorVarTemporales = self.contadorVarTemporales +1
                
                if len(self.operador) == 0: #primera vuelta
                    self.visitPartesumaresta(ctx.getChild(1).getChild(1).getChild(1)) #x = 5 * 6 (+ 1)-> parte sumaresta
                else:
                    self.visitPartesumaresta(ctx.getChild(1))
                    
            if ctx.getChild(1).getChildCount() == 0 and len(self.operador) != 0:  #x = 5 + 7 - (8)-> esto seria
                varTemp = self.variablesTemporales.pop() #saco la variabler anterior, en este caso t0
                operador = self.operador.pop() #el operador que le agregue en el coso muldiv

                print("t" + str(self.contadorVarTemporales) + " = "+ varTemp + operador + ctx.getChild(0).getText()) #t1 = t0 - 7
                
                if ctx.getChild(1).getChildCount() != 0: #x = 5 * 8 * 7
                    self.variablesTemporales.append("t" + str(self.contadorVarTemporales)) 
                    self.contadorVarTemporales = self.contadorVarTemporales + 1
                    self.visitPartesumaresta(ctx.getChild(1)) #x = 5 * 6 (* 1 * 8)-> parte mul
                else:
                    self.contadorVarTemporales = self.contadorVarTemporales + 1 #no appendeo ninguna variable, solo sumo
                
     """
        return None
        

         

    def visitPartesumaresta(self, ctx):
        print("Visitando la parte de suma resta")
        self.operador.append(ctx.getChild(0).getText())  #le paso arriba el operador de suma para que recuerde que operacion esta haciendo
        print(ctx.getText())
        self.visitTermino4(ctx.getChild(1))  #visito el que termino de la derecha
        
        return None

    
    def visitTermino5(self, ctx):
        print('parte termino 5')

        if len(ctx.getText()) == 3 and '*' not in self.operador and '/' not in self.operador : #x = ( 5 * 6 ) -> primera vez
            print("primer caso")
            print("t" + str(self.contadorVarTemporales) + " = "+ ctx.getText())
            self.variablesTemporales.append("t" + str(self.contadorVarTemporales)) #lo anado a la pila porque despues a esto lo multiplico por 7
            self.contadorVarTemporales = self.contadorVarTemporales +1
            return
        else:    
            if len(ctx.getChild(1).getText()) > 2: #x = 5 * 8 * 7
                op = ctx.getChild(1).getChild(0).getText() #*
                primNum = ctx.getChild(0).getText() #5
                segNum = ctx.getChild(1).getChild(1).getChild(0).getText() #7
                # siempre va a ser distinto en la primera parte porque hay que partir en 3 primero

                print("t" + str(self.contadorVarTemporales) + " = "+ primNum + op + segNum ) #t0 = 5*8
                self.variablesTemporales.append("t" + str(self.contadorVarTemporales)) #lo anado a la pila porque despues a esto lo multiplico por 7
                self.contadorVarTemporales =+ 1
            
                if len(self.operador) == 0: #primera vuelta
                    self.visitPartemuldivmod(ctx.getChild(1).getChild(1).getChild(1)) #x = 5 * 8 (* 7)-> parte mul
                else:
                    self.visitPartemuldivmod(ctx.getChild(1)) #x = 5 * 6 (* 1 * 8)-> parte mul
            

            if len(ctx.getChild(0).getText()) == 1 and len(self.operador) != 0:  #x = 5 * 7 * (8)-> esto seria, como el caso base ponele
                varTemp = self.variablesTemporales.pop() #saco la variabler anterior, en este caso t0
                operador = self.operador.pop() #el operador que le agregue en el coso muldiv
                print("t" + str(self.contadorVarTemporales) + " = "+ varTemp + operador + ctx.getChild(0).getText()) #t1 = t0*7
                
                if len(ctx.getChild(1).getText()) >=2: #x = 5 * 8 * 7
                    self.variablesTemporales.append("t" + str(self.contadorVarTemporales)) 
                    self.contadorVarTemporales = self.contadorVarTemporales + 1
                    self.visitPartemuldivmod(ctx.getChild(1)) #x = 5 * 6 (* 1 * 8)-> parte mul
                else:
                    
                    self.contadorVarTemporales = self.contadorVarTemporales + 1 #no appendeo ninguna variable, solo sumo
        return
            
    
    def visitPartemuldivmod(self, ctx):
        print("Visitando la parte de muldiv")
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
    
    