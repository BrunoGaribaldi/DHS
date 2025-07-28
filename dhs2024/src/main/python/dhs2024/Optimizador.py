import re
class Optimizador: 

    def __init__(self):
        self.bloques = []
        self.banderajmp = 0
    
    def optimizar(self):
        self.acomodar_entrada()
        with open("./output/archivoTemporalOptimizador.txt", "r") as src:
            lineasCodigoIntermedio = src.readlines()
            self.generadorDeBloques(lineasCodigoIntermedio)
            src.seek(0)
            lineasCodigoIntermedio = src.readlines()

        with open('./output/CodigoIntermedioOptimizado.txt', 'w') as dest:
            self.propagacionDeConstantes(lineasCodigoIntermedio,dest)
        
        with open('./output/CodigoIntermedioOptimizado.txt', 'r') as destino:
            destino.seek(0)
            lineasConPropagacionDeConstantes = destino.readlines()
        
        with open('./output/CodigoIntermedioOptimizado.txt', 'w') as dest:
            self.optimizacionExpresionesComunes(lineasConPropagacionDeConstantes, dest)

            #dest.seek(0)
            # lineasConOptimizacionExpresionesComunes = dest.readlines()
            # self.eliminacionCodigoInnecesario(lineasConOptimizacionExpresionesComunes, dest)
        
    def acomodar_entrada (self):
    
        with open("./output/codigoIntermedio.txt", "r") as src:
            # quitamos espacios en blanco del archivo
            lineas = src.readlines()
            lineas_limpias = [linea.strip() for linea in lineas if linea.strip() != ""]
            operadores = ['>=', '<=', '==', '!=', '++', '--', '&&', '||', '+', '-', '*', '/', '>', '<',  '=',  '%', '!' ]
                
            
            with open("./output/archivoTemporalOptimizador.txt", "w") as f:
                for linea in lineas_limpias:
                    f.write(linea + "\n")
            
            with open("./output/archivoTemporalOptimizador.txt", "r") as f:
                self.bloques = []
                lineasCodigoIntermedio = f.readlines()
                lineasCodigoIntermedio = self.agregar_espacios(lineasCodigoIntermedio, operadores)
                print(lineasCodigoIntermedio)

            with open("./output/archivoTemporalOptimizador.txt", "w") as f:
                for i, linea in enumerate(lineasCodigoIntermedio):
                    if i == len(lineasCodigoIntermedio) - 1:
                        f.write(linea.rstrip('\n'))  # Última línea, sin \n
                    else:
                        f.write(linea)

    def agregar_espacios(self, lineasCodigoIntermedio, operadores):

        for i, linea in enumerate(lineasCodigoIntermedio):
            lineaSplit = linea.split()
            if len(lineaSplit) == 1 and '=' in lineaSplit[0]:
                izquierda, derecha_con_salto = lineaSplit[0].split('=', 1)
                if not derecha_con_salto.endswith('\n'):
                    derecha_con_salto += '\n'
                nueva_linea = f"{izquierda} = {derecha_con_salto}"
                lineasCodigoIntermedio[i] = nueva_linea

            elif len(lineaSplit) >= 3 and lineaSplit[1] == '=':
                patron = '|'.join(sorted(map(re.escape, operadores), key=len, reverse=True))
                regex_operadores = re.compile(rf'\s*({patron})\s*')

                expresion_derecha = ' '.join(lineaSplit[2:])

                expresion_derecha = regex_operadores.sub(r' \1 ', expresion_derecha)
                expresion_derecha = ' '.join(expresion_derecha.split())

                nueva_linea = f"{lineaSplit[0]} = {expresion_derecha}"

                if linea.endswith('\n'):
                    nueva_linea += '\n'
                lineasCodigoIntermedio[i] = nueva_linea

                if not nueva_linea.endswith('\n') and linea.endswith('\n'):
                    nueva_linea += '\n'

                lineasCodigoIntermedio[i] = nueva_linea
        return lineasCodigoIntermedio


    def separar_por_operador(self, texto, operadores):
        for op in operadores:
            if op in texto:
                izquierda, derecha = texto.split(op, 1)
                return izquierda, op, derecha
        return texto, None, None

#Funcion para generar bloques optimizables
    def generadorDeBloques(self,lineasCodigoIntermedio):
        print('Identificando bloques...')

        self.bloques = []
        banderaLlamadaFuncion = 0
        banderaf = 0
        banderaDentroF = 0
        banderaSalidaF = 0
        for i, linea in enumerate(lineasCodigoIntermedio):
            #print(i, linea)
            lineaSplit = linea.split() 
            print(self.bloques)

            #caso: la primer linea de toas es un lider
            if i == 0 and (not lineaSplit[0] == 'label' and not lineaSplit[1] == 'main'):
                self.bloques.append([i,i])
            else:

                #Seccion destinada a identificar funciones. Las funciones no van a ser optimizadas.
                #toda llamada a funcion es push <o varios push> - jmp - label - pop - cualquier cosa (distinta de pop)
                # pero la ejecucion de las funciones termina por ] - push - jmp
                if (
                    lineaSplit[0] == 'push'
                    and banderaLlamadaFuncion == 0
                    and (
                        (i + 1 < len(lineasCodigoIntermedio) and lineasCodigoIntermedio[i + 1].split()[0] == 'push')
                        or (
                            i + 2 < len(lineasCodigoIntermedio)
                            and not lineasCodigoIntermedio[i + 2].split()[1].startswith('l')
                        )
                    )
                ):
                    print(lineaSplit[0])
                    print('i+1', lineasCodigoIntermedio[i+1].split()[0])
                    print('i+2', lineasCodigoIntermedio[i+4].split()[0], lineasCodigoIntermedio[i + 2].split()[1])
                    banderaLlamadaFuncion = 1
                    continue
                
                if banderaLlamadaFuncion == 1:
                    if lineaSplit[0] == 'push':
                        #significa que se pueden seguir cargando cosas a la pila en la funcion.
                        continue
                    
                    if (lineaSplit[0] == 'jump'):
                        banderaLlamadaFuncion = 0
                        continue
                                     
                #toda ejecucion de funcion comienza por label - pop <o varios pop> - [ y termina en ] - push - jmp
                #enrealiad ahora toda funcion ahora comienza por label nombre funcion. Nombre funcion es cualquier cosa distinta de lnumero
                if lineaSplit[0] == 'label' and not lineaSplit[1].startswith("l") and banderaf == 0:
                    print('este es el valor de i aca' , i)
                    banderaf = 1
                    continue
                if banderaf == 1 and lineaSplit[0] == 'pop':
                    if lineasCodigoIntermedio[i-1].split()[0] == 'label' and lineasCodigoIntermedio[i-1].split()[1].startswith('l'):
                        #significa que es la salida de una llamada de funcion que retorna algo
                        self.bloques[-1][1] = i 
                        continue
                    print('me encontre con un pop de funcion' , i)
                    continue
                if banderaf == 1 and banderaDentroF == 0 and lineaSplit[0] != 'pop':
                    print('este no es pop, por lo tanto entro a la funcion' , i)
                    banderaDentroF = 1
                    self.bloques.append([i,i])
                    self.algoritmo(lineaSplit,i)
                    continue
                if banderaDentroF == 1  and banderaf == 1:
                    if lineaSplit[0] == 'label' and lineaSplit[1].startswith('end_'):
                        banderaDentroF = 0 
                        banderaf = 0
                        banderaSalidaF = 1
                        print('fin de la funcion')
                        continue
                    print('sigo dentro de la funcion')
                    self.algoritmo(lineaSplit,i)
                    continue
                if banderaSalidaF == 1 and lineaSplit[0] == 'push':
                    continue
                if banderaSalidaF == 1 and lineaSplit[0] == 'jump':
                    banderaSalidaF = 0
                    continue

                self.algoritmo(lineaSplit,i)
                                    
        print("Bloques optimizables:", self.bloques) 

    def algoritmo (self, lineaSplit, i):
        print(i)
        if(lineaSplit[0] == 'jump' or lineaSplit[0] == 'ifntjmp'):
            self.bloques[-1][1] = i
            #caso el siguiente a un salto es lider
            self.bloques.append([i+1,i+1])
            self.banderajmp = 1
        else:
            #caso el destino de un salto es lider y la anterior instruccion no es jmp o ifntjmp
            if (lineaSplit[0] == 'label' and self.banderajmp == 0):
                self.bloques.append([i,i])
            else:
                if(lineaSplit[0] == 'label' and self.banderajmp == 1):
                #en el caso de que lo sea, la omito xq ya la agregue en append([i+1,i+1])
                    self.banderajmp = 0
                else: 
                    if (self.banderajmp == 1):
                        self.banderajmp = 0
                        return
                    else:
                        #caso cualquiera donde yo me encuentro una variable o una t
                            self.bloques[-1][1] = i 

#funcion algoritmo propagacion de constantes.
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
                    print(i)
                    if len(linea) == 3 and (linea[2].isdigit() or linea[2].isalpha()):
                        constantes[linea[0]] = linea[2]
                        print('linea' , i , 'diccionario' , constantes)
                        continue
                    else: 
                        # t1 = t2 y en mi diccionario existe t2
                        if len(linea) == 3 and (linea[2] in constantes):
                            constantes[linea[0]] = constantes[linea[2]]
                            linea[2] = str(constantes[linea[0]])
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
                                        print('entre acaaaaa')
                                        tokens = [constantes[linea[2]],linea[3],linea[4]]
                                        expr = " ".join(str(token) for token in tokens)  # '2 + 4'
                                        resultado = eval(expr)   # 6
                                        print('este es el resultadooo', resultado) 
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
        print('optimizando expresiones comunes')
        optimizado = src.copy() 
        for bloquen in self.bloques:
            inicio, fin = bloquen
            ('veamos el nestor en bloque' , inicio , fin)
            i = inicio
            while i <= fin: 
                linea = optimizado[i].split()
                print(linea)
                print(linea)
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


    




