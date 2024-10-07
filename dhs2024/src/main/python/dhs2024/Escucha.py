from antlr4 import TerminalNode
from compiladoresListener import compiladoresListener
from compiladoresParser import compiladoresParser

class Escucha (compiladoresListener) :
    numTokens = 0
    numNodos = 0
    # Enter a parse tree produced by compiladoresParser#programa.
    def enterPrograma(self, ctx:compiladoresParser.ProgramaContext):
        print("comienza la compilacion")
        
    # Exit a parse tree produced by compiladoresParser#programa.
    def exitPrograma(self, ctx:compiladoresParser.ProgramaContext):
        print("comienza la compilacion")
        print('\nse encontraron: ')
        print('\n numero de tokens: ' + str(self.numTokens))
        print('\n numero de nodos: ' + str(self.numNodos))

    # Enter a parse tree produced by compiladoresParser#iwhile.
    def enterIwhile(self, ctx:compiladoresParser.IwhileContext):
        print('Encontre WHILE')
        print('\n Cantidad de hijos: ' + str(ctx.getChildCount()))
        print('\nTokens: ' + ctx.getText())

    # Exit a parse tree produced by compiladoresParser#iwhile.
    def exitIwhile(self, ctx:compiladoresParser.IwhileContext):
        print('Fin WHILE')
        print('\n Cantidad de hijos: ' + str(ctx.getChildCount()))
        print('\nTokens: ' + ctx.getText())

        # Enter a parse tree produced by compiladoresParser#declaracion.
    def enterDeclaracion(self, ctx:compiladoresParser.DeclaracionContext):
        print('#### declaracion')

    # Exit a parse tree produced by compiladoresParser#declaracion.
    def exitDeclaracion(self, ctx:compiladoresParser.DeclaracionContext):
        print('\n nombre de variable: ' + ctx.getChild(1).getText())

    def visitTerminal(self, node: TerminalNode):
        self.numTokens+=1

    def enterEveryRule(self, ctx):
        self.numNodos+=1