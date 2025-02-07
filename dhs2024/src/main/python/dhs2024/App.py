import sys
from antlr4 import *
from compiladoresLexer  import compiladoresLexer
from compiladoresParser import compiladoresParser
from Escucha import Escucha
from Walker import Walker

def main(argv):
    archivo = "input/entrada.txt"
    if len(argv) > 1 :
        archivo = argv[1]
    input = FileStream(archivo)
    lexer = compiladoresLexer(input)
    stream = CommonTokenStream(lexer)
    parser = compiladoresParser(stream)
    escucha = Escucha()
    parser.addParseListener(escucha)
    tree = parser.programa()
    #print(tree.toStringTree())
    
    if(len(escucha.erroresSemanticos) == 0): 
        print('\nTu codigo no presenta errores semanticos, realizando el codigo intermedio ...\n')
        caminante = Walker()
        caminante.visitPrograma(tree)

    else:
        print('\nTu codigo presenta errores semanticos, no es posible realizar el codigo intermedio\n')

if __name__ == '__main__':
    main(sys.argv)