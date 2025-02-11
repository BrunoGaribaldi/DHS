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
    

    def visitTermino4(self, ctx):
        print("visitando termino 4 de la variable " + self.varAAsignar)
        #print(ctx.getChild(0).getText())
        parteSumaResta = ctx.getChild(1)
        termino5 = ctx.getChild(0) 
        if len(termino5.getText()) <= 3:
            print("AAAA:"+termino5.getText())
            #varTemporal = VarTemporal((ctx.getChild(1)).getChild(0).getText())
            return self.visitPartesumaresta(parteSumaResta) 
        else:
            return self.visitTermino5(termino5)   
    

    def visitPartesumaresta(self, ctx):
        print("Visitando la parte de suma resta")
        print(ctx.getChild(0).getText())
        if len(ctx.getText()) < 3:
            print(ctx.getChild(1).getText())
        else:
            return self.visitTermino4(ctx.getChild(1))
    
    def visitTermino5(self, ctx):
        print("visitando termino 5 de la variable " + self.varAAsignar)
        
        print(ctx.getText()) 

        

    
    
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
    
    