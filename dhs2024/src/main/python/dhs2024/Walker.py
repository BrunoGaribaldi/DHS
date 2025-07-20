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
        self.visitTermino5(ctx.getChild(0))  #miro para ver si hay una multiplicacion o division primero
        if len(ctx.getChild(0).getText()) == 3: #x = 5 * 6 
            print("t" + str(self.contadorVarTemporales) + " = "+ ctx.getChild(0).getText())
            self.contadorVarTemporales =+ 1
            return
            
        else:  
            if len(ctx.getChild(1).getText()) > 2:  #x = 5 + 7 - 8
                op = ctx.getChild(1).getChild(0).getText()
                primNum = ctx.getChild(0).getText()
                segNum = ctx.getChild(1).getChild(1).getChild(0).getText()
            
                print("t" + str(self.contadorVarTemporales) + " = "+ primNum + op + segNum )
                self.variablesTemporales.append("t" + str(self.contadorVarTemporales))
                self.contadorVarTemporales =+ 1
                
                if len(self.operador) == 0: #primera vuelta
                    self.visitPartesumaresta(ctx.getChild(1).getChild(1).getChild(1)) #x = 5 * 6 (+ 1)-> parte sumaresta
                else:
                    self.visitPartesumaresta(ctx.getChild(1))
                    
            if len(ctx.getChild(0).getText()) == 1 and len(self.operador) != 0:  #x = 5 + 7 - (8)-> esto seria
                varTemp = self.variablesTemporales.pop() #saco la variabler anterior, en este caso t0
                operador = self.operador.pop() #el operador que le agregue en el coso muldiv
                print("t" + str(self.contadorVarTemporales) + " = "+ varTemp + operador + ctx.getChild(0).getText()) #t1 = t0 - 7
                
                if len(ctx.getChild(1).getText()) >=2: #x = 5 * 8 * 7
                    self.variablesTemporales.append("t" + str(self.contadorVarTemporales)) 
                    self.contadorVarTemporales = self.contadorVarTemporales + 1
                    self.visitPartesumaresta(ctx.getChild(1)) #x = 5 * 6 (* 1 * 8)-> parte mul
                else:
                    self.contadorVarTemporales = self.contadorVarTemporales + 1 #no appendeo ninguna variable, solo sumo
                return
    
        return None
        

         

    def visitPartesumaresta(self, ctx):
        print("Visitando la parte de suma resta")
        self.operador.append(ctx.getChild(0).getText())  #le paso arriba el operador de suma para que recuerde que operacion esta haciendo
        print(ctx.getText())
        self.visitTermino4(ctx.getChild(1))  #visito el que termino de la derecha
        
        return None

    
    def visitTermino5(self, ctx):
       
        if len(ctx.getText()) == 3 and len(self.operador) == 0: #x = ( 5 * 6 ) -> primera vez
            print("primer caso")
            print("t" + str(self.contadorVarTemporales) + " = "+ ctx.getText())
            self.contadorVarTemporales =+ 1
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
    
    