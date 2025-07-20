from compiladoresVisitor import compiladoresVisitor
from compiladoresParser import compiladoresParser


class VarTemporal:
    contador = -1
    def __init__(self):
        self.nombre = "t" + self.contador
        self.contador = self.contador + 1
        self.proxOp = "" 
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
    

    # def visitTermino4(self, ctx):
    #     print("visitando termino 4 de la variable " + self.varAAsignar)
    #     #print(ctx.getChild(1).getText())
    #     parteSumaResta = ctx.getChild(1)
    #     termino5 = ctx.getChild(0) 

    #     if (len(parteSumaResta.getText()) == 0):
    #         print(ctx.getText())
    #         return self.visitTermino5(termino5)
    #     if len(termino5.getText()) <= 3:

    #         if len(self.variablesTemporales) == 0:
    #             print("t" + str(self.contadorVarTemporales) + " = "+termino5.getText())
    #             self.variablesTemporales.append("t" + str(self.contadorVarTemporales))
    #             self.contadorVarTemporales = self.contadorVarTemporales + 1

    #         else:
                
    #             print("t" + str(self.contadorVarTemporales) + " = "+ self.variablesTemporales[0] + termino5.getText())
    #             self.variablesTemporales.pop()
    #             self.variablesTemporales.append("t" + str(self.contadorVarTemporales)) 
    #             self.contadorVarTemporales = self.contadorVarTemporales + 1
    #         #varTemporal = VarTemporal((ctx.getChild(1)).getChild(0).getText())

    #         return self.visitPartesumaresta(parteSumaResta) 
    #     else:
    #         return self.visitTermino5(termino5)   
    
    #prueba

    def visitTermino4(self, ctx):
        #self.visitTermino5(ctx.getChild(0))  #miro para ver si hay una multiplicacion o division primero
        if len(ctx.getChild(0).getText()) == 3: #x = 5 * 6 
            print("t" + str(self.contadorVarTemporales) + " = "+ ctx.getChild(0).getText())
            self.variablesTemporales.append("t" + str(self.contadorVarTemporales))
            self.contadorVarTemporales =+ 1
            self.visitPartesumaresta(ctx.getChild(1)) #x = 5 * 6 (+ 1)-> parte sumaresta
        else:
            self.visitTermino5(ctx.getChild(0))  #miro para ver si hay una multiplicacion o division primero
        
        
      
            
        if len(ctx.getChild(1).getText()) > 2:  #x = 5 + 7 - 8
            op = ctx.getChild(1).getChild(0).getText()
            primNum = ctx.getChild(0).getText()
            segNum = ctx.getChild(1).getChild(1).getChild(0).getText()
            
            print("t" + str(self.contadorVarTemporales) + " = "+ primNum + op + segNum )
            self.variablesTemporales.append("t" + str(self.contadorVarTemporales))
            self.contadorVarTemporales =+ 1
            self.visitPartesumaresta(ctx.getChild(1).getChild(1).getChild(1)) #x = 5 * 6 (+ 1)-> parte sumaresta
        
        if len(ctx.getChild(0).getText()) == 1 and len(self.operador) != 0:  #x = 5 + 7 - (8)-> esto seria
            print("t" + str(self.contadorVarTemporales) + " = "+ self.variablesTemporales[0] + self.operador[0] + ctx.getChild(0).getText())
            self.variablesTemporales.pop()
            self.operador.pop() #ya termino la cadena recursiva
            return
    
        return None
        

            


          
        """
          if len(ctx.getChild(0).getText()) == 1: #x = 5 * 6 + (1)-> esto seria
            #print(self.variablesTemporales[0])
            print("t" + str(se
        return None
        lf.contadorVarTemporales) + " = "+ self.variablesTemporales[0] + self.operador[0] + ctx.getChild(0).getText())
            self.variablesTemporales.pop()
            self.operador.pop() #ya termino la cadena recursiva
        
        print("visitando termino 4 de la variable " + self.varAAsignar)
        parteSumaResta = ctx.getChild(1) #partesumaresta : SUMA termino4
        termino5 = ctx.getChild(0)  #termino5  : termino6 partemuldivmod; 

        #x = 5 ;
        if len(ctx.getText()) == 1:
            print(self.varAAsignar + " = " + ctx.getChild(0).getText())

        else:
        #x = 5 + 8 + ...
          if len(termino5.getText()) <= 3:  #x = 5 + 8
              if len(self.variablesTemporales) == 0:
                 print("t" + str(self.contadorVarTemporales) + " = "+termino5.getText())
                 self.variablesTemporales.append("t" + str(self.contadorVarTemporales))
                 self.contadorVarTemporales =+ 1
                 
              else:    
                 print("dddd")
                 print("t" + str(self.contadorVarTemporales) + " = "+ self.variablesTemporales[0] + termino5.getText())
                 self.variablesTemporales.pop()
                 self.variablesTemporales.append("t" + str(self.contadorVarTemporales)) 
                 self.contadorVarTemporales = self.contadorVarTemporales + 1
         """        
            



    def visitPartesumaresta(self, ctx):
        print("Visitando la parte de suma resta")
        self.operador.append(ctx.getChild(0).getText())  #le paso arriba el operador de suma para que recuerde que operacion esta haciendo
        print(ctx.getText())
        self.visitTermino4(ctx.getChild(1))  #visito el que termino de la derecha
        
        return None
        # self.variablesTemporales[0] += " " + ctx.getChild(0).getText() + " "
        # if len(ctx.getText()) < 3:
        #     print("t" + str(self.contadorVarTemporales) + " = "+ self.variablesTemporales[0] + ctx.getChild(1).getText())
        #     self.variablesTemporales.pop()
        #     #print(ctx.getChild(1).getText())
        #     print(self.varAAsignar + " = t" + str(self.contadorVarTemporales))
        #     self.contadorVarTemporales = self.contadorVarTemporales + 1
        # else:
        #     return self.visitTermino4(ctx.getChild(1))
    
    def visitTermino5(self, ctx):
        if len(ctx.getChild(1).getText()) > 2: #x = 5 * 8 * 7
            op = ctx.getChild(1).getChild(0).getText()
            primNum = ctx.getChild(0).getText()
            segNum = ctx.getChild(1).getChild(1).getChild(0).getText()
            
            print("t" + str(self.contadorVarTemporales) + " = "+ primNum + op + segNum )
            self.variablesTemporales.append("t" + str(self.contadorVarTemporales))
            self.contadorVarTemporales =+ 1
            self.visitPartemuldivmod(ctx.getChild(1).getChild(1).getChild(1)) #x = 5 * 6 (* 1)-> parte mul


        elif len(ctx.getChild(0).getText()) == 1 and len(self.operador) != 0:  #x = 5 * 7 * (8)-> esto seria
            print("t" + str(self.contadorVarTemporales) + " = "+ self.variablesTemporales[0] + self.operador[0] + ctx.getChild(0).getText())
            self.variablesTemporales.pop()
            self.operador.pop()

            if len(ctx.getChild(1).getText()) >= 2: #x = 5 * 7 * (8 * 7 )-> esto seria
                self.variablesTemporales.append("t" + str(self.contadorVarTemporales))
                self.contadorVarTemporales =+ 1
                self.visitPartemuldivmod(ctx.getChild(1)) #x = 5 * 6 (* 1)-> parte mul

                op = ctx.getChild(1).getChild(0).getText()
                primNum = ctx.getChild(0).getText()
                segNum = ctx.getChild(1).getChild(1).getChild(0).getText()
            
                print("t" + str(self.contadorVarTemporales) + " = "+ primNum + op + segNum )
                self.variablesTemporales.append("t" + str(self.contadorVarTemporales))
                self.contadorVarTemporales =+ 1
                self.visitPartemuldivmod(ctx.getChild(1)) #x = 5 * 6 (* 1)-> parte mul

            return
            
        elif ctx.getChild(1).getChildCount() < 3: #x = 5 (* 6 ) -> parte muldiv
            print("t" + str(self.contadorVarTemporales) + " = "+ ctx.getChild(1).getText())
            return 
             
    
    def visitPartemuldivmod(self, ctx):
        print("Visitando la parte de muldiv")
        self.operador.append(ctx.getChild(0).getText())  #le paso arriba el operador de suma para que recuerde que operacion esta haciendo
        print(ctx.getText())
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
    
    