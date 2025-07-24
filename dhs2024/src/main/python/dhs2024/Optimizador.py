class Optimizador: 

    def __init__(self):
        self.bloques = []
    

    def optimizar(self):
        with open("./Entrada.txt", "r") as src, open("./CodigoIntermedioOptimizado", "w+") as dest:
            lineasCodigoIntermedio = src.readlines()
            self.generadorDeBloques(lineasCodigoIntermedio)
            self.propagacionDeConstantes(lineasCodigoIntermedio,dest)
            dest.seek(0)
            lineasConPropagacionDeConstantes = dest.readlines()
            dest.seek(0)
            self.optimizacionExpresionesComunes(lineasConPropagacionDeConstantes, dest)
            

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

    
    def propagacionDeConstantes(self,lineasCodigoIntermedio,dest): #probar el tema de > o < logicos
        print('Propagacion de constantes...')  
        optimizado = lineasCodigoIntermedio.copy() 
        print(optimizado)
        print(self.bloques)
        for bloquen in self.bloques:
            inicio,fin = bloquen
            constantes = dict()
            print("-------------------------------------------------")

            #bucle sobre cada bloque optimizable
            for i in range(inicio , fin + 1):
                linea = optimizado[i].split()
                
                
                # 1)es asignacion?
                if (linea[1] != '='): #no
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
                            linea[2] = constantes[linea[0]]
                            optimizado[i] = " ".join(linea) + "\n"
                        else:
                        # caso t = 2 + 4
                            if len(linea) == 5 and (linea[2].isdigit() and linea[4].isdigit()):
                                tokens = [linea[2],linea[3],linea[4]]
                                expr = " ".join(str(token) for token in tokens)  # '2 + 4'
                                resultado = eval(expr)   # 6 
                                str_resultado = str(resultado)
                                #aca guarda en archivo. REVISAR EL TEMA DE LOS TIPOS DE DATOS EN LAS VARIABLES T.
                                constantes[linea[0]] = resultado #guardo en diccionario
                                nueva_linea = [linea[0], '=', str_resultado]
                                optimizado[i] = " ".join(nueva_linea) + "\n"
                            else:
                                #caso t = 2 + t   
                                if len(linea) == 5 and (linea[2].isdigit() and not linea[4].isdigit() and linea[4] in constantes):
                                    tokens = [linea[2],linea[3],constantes[linea[4]]]
                                    expr = " ".join(str(token) for token in tokens)  # '2 + 4'
                                    resultado = eval(expr)   # 6 
                                    str_resultado = str(resultado)
                                    #aca guarda en archivo. REVISAR EL TEMA DE LOS TIPOS DE DATOS EN LAS VARIABLES T.
                                    constantes[linea[0]] = resultado #guardo en diccionario
                                    nueva_linea = [linea[0], '=', str_resultado]
                                    optimizado[i] = " ".join(nueva_linea) + "\n"
                                else:
                                    #caso t = t + 2
                                    if len(linea) == 5 and (not linea[2].isdigit() and linea[4].isdigit() and linea[2] in constantes):
                                        tokens = [constantes[linea[2]],linea[3],linea[4]]
                                        expr = " ".join(str(token) for token in tokens)  # '2 + 4'
                                        resultado = eval(expr)   # 6 
                                        str_resultado = str(resultado)
                                        #aca guarda en archivo. REVISAR EL TEMA DE LOS TIPOS DE DATOS EN LAS VARIABLES T.
                                        constantes[linea[0]] = resultado #guardo en diccionario
                                        nueva_linea = [linea[0], '=', str_resultado]
                                        optimizado[i] = " ".join(nueva_linea) + "\n"
                                    else:
                                        #caso t = t1 + t2
                                        if len(linea) == 5 and linea[2] in constantes and linea [4] in constantes: #osea q t1 y t2 este en mi diccionario
                                            tokens = [constantes[linea[2]],linea[3],constantes[linea[4]]]
                                            expr = " ".join(str(token) for token in tokens)  # '2 + 4'
                                            resultado = eval(expr)   # 6 
                                            str_resultado = str(resultado)
                                            #aca guarda en archivo. REVISAR EL TEMA DE LOS TIPOS DE DATOS EN LAS VARIABLES T.
                                            constantes[linea[0]] = resultado #guardo en diccionario
                                            nueva_linea = [linea[0], '=', str_resultado]
                                            optimizado[i] = " ".join(nueva_linea) + "\n"
                                        else:
                                            #caso t = t1 + t2 pero t1 no lo tengo en el diccionario
                                            if len(linea) == 5 and linea[4] in constantes:
                                                linea[4] = constantes[linea[4]]
                                                optimizado[i] = " ".join(linea) + "\n"
                                            else:
                                                if linea[2] in constantes:
                                                    linea[2] = constantes[linea[2]]
                                                    optimizado[i] = " ".join(linea) + "\n"
        print(optimizado)
        for lineas in optimizado:
            dest.write(lineas)                                   

    #algoritmo basado en lo siguiente: https://youtu.be/23PoAQKYsHE                 
    def optimizacionExpresionesComunes(self, src , destino):
        optimizado = src.copy() 
        largoOptimizado = len(optimizado)
        for bloquen in self.bloques:
            inicio, fin = bloquen
            i = inicio
            while i <= fin: 
                linea = optimizado[i].split()
                if len(linea) == 5 and linea [1] == '=': #osea si es del tipo p = x + y x ejemplo
                    if linea[0] == linea [2] or linea [0] == linea[4]: # a cambiado p?
                        i += 1
                        continue
                    
                    j = i + 1 #evaluamos las siguientes lineas
                    while j <= fin:
                        siguienteLinea = optimizado[j].split()
                        if len(siguienteLinea) != 5 or siguienteLinea[1] != '=': #pregunto si no es la proxima linea t = t + t (significa que es una asignacion normal o otra cosa)
                            j += 1
                            continue
                    
                        # a cambiado p en t = t + t?
                        if siguienteLinea[0] == linea[2] or siguienteLinea[0] == linea[4]:
                            break

                        # Coincide operación y operandos osea p = x + y === t = t + t????
                        if (siguienteLinea[2] == linea[2] and 
                            siguienteLinea[3] == linea[3] and 
                            siguienteLinea[4] == linea[4]):

                            nueva_linea = f"{siguienteLinea[0]} = {linea[0]}\n"
                            optimizado[j] = nueva_linea

                        j += 1
                i += 1
        print(optimizado)
        # Escribimos todo al destino
        destino.seek(0)
        destino.truncate() #para escribir el archivo de cero
        for linea in optimizado:
            if not linea.endswith('\n'):
                linea += '\n'
            destino.write(linea)


        # optimizado = src.copy()
        # saltar_for = False
        # largoOptimizado = len(optimizado)
        # for bloquen in self.bloques:
        #     inicio,fin = bloquen
        #     print("-------------------------------------------------")

        #     #bucle sobre cada bloque optimizable
        #     for i in range(inicio , fin + 1): # en este caso el candidato no los indica la i
        #         linea = optimizado[i].split()  
        #         print("esta es la linea con la que nos encontramos de candidato ahora", linea)
        #         counter = 1
        #         print("es", linea, "= 5 y tiene = ?" )
        #         if len(linea) == 5 and linea[1] == '=': 
        #             print("si!, es ", linea[0] , "igual a ",  linea [2] , " o es igual a ", linea [4])
        #             if linea[0] == linea [2] or linea[0] == linea [4]: #ha cambiado p?
        #                 print("si!!! por lo tanto deja de ser candidato")
        #                 continue
        #             print("no! no deja de ser candidato por lo tanto entramos al while")
        #             print("largoOptimizado > i + counter ?????")
        #             while largoOptimizado > i + counter: # no cambio p   
        #                 siguiente_linea = optimizado[i + counter].split()
        #                 print("esta es la siguiente linea", siguiente_linea, "es mayor a 5 y tiene el =? " )
        #                 if len(siguiente_linea) == 5 and siguiente_linea[1] == '=': #el que le sigue es del tipo t = x + x?
        #                     print(siguiente_linea, "SIII es mayor a 5 y tiene el =. aHORA, ", siguiente_linea[0] , "ES IGUAL A " , linea [2], "O A " , linea [4])
        #                     if siguiente_linea[0] == linea [2] or siguiente_linea[0] == linea [4]: #ha cambiado p en t = x + x?
        #                        print("sep por lo tanto deja de ser candidato, me voy al siguiente")
        #                        counter = 1
        #                        #si cambia deja de ser candidato p, tengo que ir a la siguiente iteracion del for
        #                        saltar_for = True
        #                        break #salgo del while
        #                     else: 
        #                         print("nononononono por lo tanto nos cuestionamos si ", siguiente_linea[2],"=", linea [2],"y", siguiente_linea[4],"=", linea [4] ,"y",siguiente_linea[3] ,"=",linea [3])  
        #                         if siguiente_linea[2] == linea [2] and siguiente_linea[4] == linea [4] and siguiente_linea[3] == linea [3]: #p + 0 == x + x????
        #                           print('ASI ES MUCHACHOS POR LO TANTO CREAMOS UNA NUEVA LINEA, cuanto sera i + counter?', i + counter)
        #                           #si es igual osea p + 0 == p + 0
        #                           nueva_linea = [siguiente_linea[0], '=' , linea[0]] 
        #                           optimizado[i+counter] = " ".join(nueva_linea) + "\n"
        #                           counter += 1
        #                           continue
        #                         else: 
        #                            print('NO SE CREA UNA PORONGA')
        #                            continue
        #                 else:
        #                     print(siguiente_linea, "NOOO es mayor a 5 y tiene el =")
        #                     counter += 1
        #                     continue # no es del tipo t = x + x     
        #             if saltar_for:
        #                 print("holaaa saltamos al siguiente ciclo for")
        #                 saltar_for = False
        #                 continue #siguiente it del for
        #         else:   
        #             print("es", linea, "= 5 y tiene = ? NOOOOOO" )
        #             continue    
        # for lineas in optimizado:
        #     destino.write(lineas)        


        
        

if __name__ == "__main__":
    opt = Optimizador()
    opt.optimizar()

    




