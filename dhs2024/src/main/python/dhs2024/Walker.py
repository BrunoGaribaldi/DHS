from compiladoresVisitor import compiladoresVisitor
from compiladoresParser import compiladoresParser


class VarTemporal:
    contador = -1
    def __init__(self):
        self.nombre = "t" + self.contador
        self.contador = self.contador + 1 
class Walker (compiladoresVisitor):

    contadorVarTemporales = 0
    variablesTemporales = []
    varAAsignar = ''

    
    def visitAsignacion(self, ctx):
        self.varAAsignar = ctx.getChild(0).getText()
        print(self.varAAsignar)
        return super().visitOpal(ctx)
    
    
    def visitOpal(self, ctx):
        print("visitando opal de la variable " + self.varAAsignar)
        return super().visitTermino1(ctx)

    def visitTermino1(self, ctx):
        print("visitando termino 1 de la variable " + self.varAAsignar)
        return super().visitTermino2(ctx)

    def visitTermino2(self, ctx):
        print("visitando termino 2 de la variable " + self.varAAsignar)
        return super().visitTermino3(ctx)
    

    def visitTermino3(self, ctx):
        print("visitando termino 3 de la variable " + self.varAAsignar)
        return super().visitTermino4(ctx)
    

    def visitTermino4(self, ctx):
        print("visitando termino 4 de la variable " + self.varAAsignar)
        #print(ctx.getChild(0).getText())
        if len(ctx.getChild(0).getText()) > 3:
            return super().visitTermino5(ctx)
        else:
            print(ctx.getChild(0).getText()) 
            return super().visitPartesumaresta(ctx)   
    

    def visitPartesumaresta(self, ctx):
        print("Visitando la parte de suma resta")
        if len(ctx.getText()) < 3:
            print(ctx.getText())
        else:
            return super().visitTermino4(ctx)
    
    def visitTermino5(self, ctx):
        print("visitando termino 5 de la variable " + self.varAAsignar)
        

    
    
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
    
    