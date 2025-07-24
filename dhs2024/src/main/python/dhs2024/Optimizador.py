class Optimizador: 

    def __init__(self):
        self.bloques = []
    
    def optimizar(self):
        with open("./Entrada.txt", "r") as src, open("./CodigoIntermedioOptimizado", "w+") as dest:
            #quitamos espacios en blanco del archivo
            lineas = src.readlines()
            lineas_limpias = [linea.strip() for linea in lineas if linea.strip() != ""]
            with open("Entrada.txt", "w") as f:
                for linea in lineas_limpias:
                    f.write(linea + "\n")
            src.seek(0)

            self.bloques = []
            lineasCodigoIntermedio = src.readlines()
            self.generadorDeBloques(lineasCodigoIntermedio)
            # self.propagacionDeConstantes(lineasCodigoIntermedio,dest)
            # dest.seek(0)
            # lineasConPropagacionDeConstantes = dest.readlines()
            # dest.seek(0)
            # self.optimizacionExpresionesComunes(lineasConPropagacionDeConstantes, dest)
            # dest.seek(0)
            # lineasConOptimizacionExpresionesComunes = dest.readlines()
            # self.eliminacionCodigoInnecesario(lineasConOptimizacionExpresionesComunes, dest)

#Funcion para generar bloques optimizables
    def generadorDeBloques(self,lineasCodigoIntermedio):
        print('Identificando bloques...')
        self.bloques = []
        banderajmp = 0
        banderaf = 0
        banderaPush = 0
        contadorCorchete = 0
        for i, linea in enumerate(lineasCodigoIntermedio):
            #print(i, linea)
            lineaSplit = linea.split() 

            #caso: la primer linea de toas es un lider
            
            if i == 0:
                self.bloques.append([i,i])
            else:
                    #Sector llamada funciones
                    if lineaSplit[0] == 'push' :
                        if i + 1 < len(lineasCodigoIntermedio) and lineasCodigoIntermedio[i+1].split()[0] == 'push':
                            banderaPush = 1
                            continue
                        if i + 2 == len(lineasCodigoIntermedio):
                            continue
                        if i + 4 < len(lineasCodigoIntermedio) and (lineasCodigoIntermedio[i+4].split()[0] == 'pop' or lineasCodigoIntermedio[i+4].split()[0] == '['):
                            continue
                        else: 
                            banderaPush = 1
                            continue
                    if lineaSplit[0] == 'jmp' and banderaPush == 1:
                        continue
                    if lineaSplit[0] == 'label' and banderaPush == 1:
                        self.bloques.append([i,i])
                        banderaPush = 0
                        continue
                    #Sector ejecucion funciones
                    if (lineaSplit[0] == 'label' and i + 1 < len(lineasCodigoIntermedio) and i + 2 < len(lineasCodigoIntermedio) and
                        lineasCodigoIntermedio[i+1].split()[0] == 'pop' and 
                        lineasCodigoIntermedio[i+2].split()[0] == '['):
                        banderaf = 1
                        continue
                    if (lineaSplit[0] == 'label' and i + 1 < len(lineasCodigoIntermedio) and i + 2 < len(lineasCodigoIntermedio) and
                        lineasCodigoIntermedio[i+1].split()[0] == 'pop' and 
                        lineasCodigoIntermedio[i+2].split()[0] == 'pop'):
                        banderaf = 1
                        continue
                    if banderaf == 1 and i + 1 < len(lineasCodigoIntermedio) and lineasCodigoIntermedio[i+1].split()[0] != ']' :
                        continue
                    if banderaf == 1 and i + 1 < len(lineasCodigoIntermedio) and lineasCodigoIntermedio[i+1].split()[0] == ']':
                        continue
                    if banderaf == 1 and lineaSplit[0] == ']':
                        banderaf = 0
                        contadorCorchete = 1
                        continue
                    if contadorCorchete == 1: 
                        contadorCorchete = 0
                        continue
                        

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
#SECTOR DE FUNCIONES. Aclaracion. Toda funcion no sera optimizada tanto en la llamada como en su ejecucion.
                        
            
         

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

#Funcion para detectar variables que no se esten utilizando (Dead Code Elimination)
# https://youtu.be/ayyBhYowVIs
    def eliminacionCodigoInnecesario(self, src, destino):
        definidas = set()
        usadas = set()
        optimizado = src.copy()

        for bloquen in self.bloques:
            inicio, fin = bloquen
            i = inicio

            while i <= fin:
                linea = optimizado [i].split()
                if len(linea) >= 3 and linea[1] == '=':
                    definidas.add(linea[0]) #miro el lado izquierdo y agrego a definidas
                    #ahora miramos el lado derecho para ver que variables estan siendo usadas
                    usadas.update([linea[j] for j in range(2, len(linea)) if linea[j].isidentifier()])
                i += 1
            
            #vemos variables que no se esten usando
            innecesarias = definidas - usadas
            i = inicio
            while i <= fin:
                partes = optimizado[i].split()
                if len(partes) >= 3 and partes[1] == '=' and partes[0] in innecesarias:
                    optimizado[i] = "" #saco la linea
                i += 1

        destino.seek(0)
        destino.truncate() #para escribir el archivo de cero
        for linea in optimizado:
            if linea == "":
                continue  # saltar línea vacía
            if not linea.endswith('\n'):
                linea += '\n'
            destino.write(linea)      

if __name__ == "__main__":
    opt = Optimizador()
    opt.optimizar()

    




