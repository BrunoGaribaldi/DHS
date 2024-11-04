class ErrorSemantico():
    def __init__(self, numLinea, titulo, mensaje):
        self.numLinea = numLinea
        self.mensaje = mensaje
        self.titulo = titulo

    def __str__(self):
        return("Numero de linea: " + str(self.numLinea) + "\nTipo de error: " + self.titulo + "\nMensaje: " + self.mensaje + "\n" ) 