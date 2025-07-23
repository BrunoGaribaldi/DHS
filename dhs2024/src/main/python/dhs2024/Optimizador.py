class Optimizador: 

    def __init__(self):
        self.bloques = []
    

    def optimizar(self):
        with open("./Entrada.txt", "r") as src, open("./CodigoIntermedioOptimizado", "w") as dest:
            lineasCodigoIntermedio = src.readlines()
            self.generadorDeBloques(lineasCodigoIntermedio)
            self.propagacionDeConstantes(lineasCodigoIntermedio,dest)
            

    def generadorDeBloques(self,lineasCodigoIntermedio):
        print('Identificando bloques...')
        self.bloques = []
        #print(lineasCodigoIntermedio)
        banderajmp = 0
        for i, linea in enumerate(lineasCodigoIntermedio):
            #print(i, linea)
            lineaSplit = linea.split() 

            #caso: la primer linea de toas es un lider
            if i == 0:
                self.bloques.append([i,i])
            else:
                if(lineaSplit[0] == 'jmp' or lineaSplit[0] == 'ifntjmp'):
                    self.bloques[-1][1] = i
                    #caso el siguiente a un salto es lider
                    self.bloques.append([i+1,i+1])
                    banderajmp = 1
                else:
                    #caso el destino de un salto es lider y la anterior instruccion no es jmp o ifntjmp
                    if (lineaSplit[0] == 'label' and banderajmp == 0):
                        self.bloques.append([i,i])
                    else:
                        if(lineaSplit[0] == 'label' and banderajmp == 1):
                        #en el caso de que lo sea, la omito xq ya la agregue en append([i+1,i+1])
                            banderajmp = 0
                        else: 
                            if (banderajmp == 1):
                                continue
                            else:
                                #caso cualquiera donde yo me encuentro una variable o una t
                                 self.bloques[-1][1] = i                     
        print("Bloques optimizables:", self.bloques) 

    
    def propagacionDeConstantes(self,lineasCodigoIntermedio,dest):
        print('Propagacion de constantes...')  
        optimizado = lineasCodigoIntermedio.copy() 
        for bloquen in self.bloques:
            inicio,fin = bloquen
            constantes = dict()
            print("-------------------------------------------------")

            #bucle sobre cada bloque optimizable
            for i in range(inicio , fin + 1):
                linea = optimizado[i].split()
                print(linea)

                # 1)es asignacion?
                if (linea[1] != '='):
                    continue
                else:
                    # t1 = 2
                    if len(linea) == 3 and (linea[2].isdigit() or linea[2].isalpha()):
                        constantes[linea[0]] = linea[2]
                        continue
                    else: 
                        # t1 = t2 y en mi diccionario existe t2
                        if len(linea) == 3 and (linea[2] in constantes):
                            constantes[linea[0]] = constantes[linea[2]]
                            continue
                        else:
                        # caso t = 2 + 4
                            if len(linea) == 5 and (linea[2].isdigit() and linea[4].isdigit()):
                                tokens = [linea[2],linea[3],linea[4]]
                                expr = " ".join(tokens)  # '2 + 4'
                                resultado = eval(expr)   # 6 
                                str_resultado = str(resultado)
                                print(str_resultado) #aca guarda en archivo. REVISAR EL TEMA DE LOS TIPOS DE DATOS EN LAS VARIABLES T.
                                constantes[linea[0]] = resultado #guardo en diccionario
                            else:
                                #caso t = 2 + t   
                                if len(linea) == 5 and (linea[2].isdigit() and not linea[4].isdigit() and linea[4] in constantes):
                                    tokens = [linea[2],linea[3],constantes(linea[4])]
                                    expr = " ".join(tokens)  # '2 + 4'
                                    resultado = eval(expr)   # 6 
                                    str_resultado = str(resultado)
                                    print(str_resultado) #aca guarda en archivo. REVISAR EL TEMA DE LOS TIPOS DE DATOS EN LAS VARIABLES T.
                                    constantes[linea[0]] = resultado #guardo en diccionario
                                else:
                                    #caso t = t + 2
                                    if len(linea) == 5 and (not linea[2].isdigit() and linea[4].isdigit() and linea[2] in constantes):
                                        tokens = [constantes(linea[2]),linea[3],linea[4]]
                                        expr = " ".join(tokens)  # '2 + 4'
                                        resultado = eval(expr)   # 6 
                                        str_resultado = str(resultado)
                                        print(str_resultado) #aca guarda en archivo. REVISAR EL TEMA DE LOS TIPOS DE DATOS EN LAS VARIABLES T.
                                        constantes[linea[0]] = resultado #guardo en diccionario
                                    else:
                                        #caso t = t1 + t2
                                        if len(linea) == 5 and linea[2] in constantes and linea [4] in constantes: #osea q t1 y t2 este en mi diccionario
                                            tokens = [constantes(linea[2]),linea[3],constantes(linea[4])]
                                            expr = " ".join(tokens)  # '2 + 4'
                                            resultado = eval(expr)   # 6 
                                            str_resultado = str(resultado)
                                            print(str_resultado) #aca guarda en archivo. REVISAR EL TEMA DE LOS TIPOS DE DATOS EN LAS VARIABLES T.
                                            constantes[linea[0]] = resultado #guardo en diccionario
                                        else:
                                            #caso t = t1 + t2 pero t1 no lo tengo en el diccionario
                                            if len(linea) == 5 and linea[2] in constantes:
                                                continue #agregar a la salida
                                            else:
                                                continue # agregar a la salida
            print(constantes)
                                

                


        
        

if __name__ == "__main__":
    opt = Optimizador()
    opt.optimizar()

    




