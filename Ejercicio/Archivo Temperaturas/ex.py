def es_flotante(cadena): #funcion que me ayuda a ver si falta o no falta tmax o tmin
    try:
        float(cadena)
        return True
    except ValueError:
        return False
    
def contar_espacios(campo, campo_string):
    index = campo_string.find(campo[1])    
    longitud = len(campo[0])
    return index - longitud

def obtener_datos (campo , campo_string): #devuelve lista [Fecha, Tmax , Tmin , Estacion]
    if not es_flotante(campo[1]): #faltan tmax y tmin
        tmin = str(None)
        tmax = str(None)
        fecha = campo[0]
        estacion = campo[1:]
    else: 
        if es_flotante(campo[2]): #no faltan datos
            fecha = campo[0]
            tmax = campo[1]
            tmin = campo[2]
            estacion = campo [3:]

        else:  #faltan datos. ahora bien. cual. sera minimo o maximo?

            espacios = contar_espacios(campo,campo_string)
            if espacios > 4: #entonces el campo que falta es tmax
                fecha = campo[0]
                tmin = campo[1]
                tmax = str(None)
                estacion = campo [2:]
            else: #falta tmin
                estacion = campo [2:]
                tmin = str(None)
                fecha = campo[0]
                tmax = campo[1]
    return[fecha , tmax , tmin , " ".join(estacion)]

def actualizar_diccionario(diccionario , datos):
    if datos[3] not in diccionario.keys():
            diccionario.update({datos[3] : [{"tmax" : [ datos[1]+"_"+datos[0] ] } , {"tmin" : [ datos[2]+"_"+datos[0] ] } ] })
    else:
        #obtengo los valores para la estacion datos[3]
        valores = diccionario[datos[3]] 
        
        #obtengo diccionario referido al tmax y tmin
        tmax_diccionario = valores[0]   
        tmin_diccionario = valores[1]
            
        #obtengo la lista de valores de tmax y tmin
        tmax_lista = tmax_diccionario["tmax"] 
        tmin_lista = tmin_diccionario["tmin"]

        #le agrego los valores nuevos a las listas de tmax y tmin. los datos que se guardan son del tipo "dato_fecha"
        tmax_lista.append(datos[1]+" fecha:"+datos[0])
        tmin_lista.append(datos[2]+" fecha:"+datos[0])

        #actualizo los diccionarios de tmax y tmin
        tmax_diccionario["tmax"] = tmax_lista
        tmin_diccionario["tmin"] = tmin_lista

        #actualizo la estacion
        diccionario[datos[3]] = [tmax_diccionario , tmin_diccionario]
    return diccionario

def construir_diccionario(nombre): #retorna el diccionario con todas las estaciones y sus valores despues de leer todo el archivo. {estacion : [ {tmax:[datos_fechas]} , {tmin : [datos_fechas]} ]}
    diccionario = {}
    archivo = open(nombre,"r")

    for renglon in archivo:

        #omitir los primeros dos renglones
        if "FECHA" in renglon or "--------" in renglon: 
            continue  

        campo = renglon.strip().split()
        campo_string = renglon.strip()
        datos = obtener_datos(campo , campo_string)
        diccionario = actualizar_diccionario(diccionario,datos)

    return diccionario

def construccion_lista(dato):#devuelve una lista separada de la string ingresada para la busqueda del dato.[CORDOBA OBSERVATORIO][tmin][3] --> ['CORDOBA OBSERVATORIO', 'tmin', '3']
    dato = dato.strip("[]")
    lista =  dato.split('][')
    return(lista)

def impresion_informacion(diccionario , lista_dato): #imprime lo que se le pida
    indice = int(lista_dato[2]) - 1
    if lista_dato[1] == "tmax":
        requerido = 0
    else:
        requerido = 1
    dic =  diccionario[lista_dato[0]][requerido]
    return dic[lista_dato[1]][indice]

nombre = "registro_temperatura365d_smn.txt" #nombre del archivo.    registro_temperatura365d_smn.txt. #suponemos que la ultima fecha es la que se encuentra mas arriba en el archivo
diccionario = dict
diccionario = construir_diccionario(nombre)

dato = input("\nSi quiero saber la temperatura mínima de Córdoba hace 3 días atrás debo accederla de la siguiente forma:\n[CORDOBA OBSERVATORIO][tmin][3]\n")

lista_dato = construccion_lista(dato)

print(impresion_informacion(diccionario , lista_dato))

#mejoras
# 1) no suponer que las fechas esten ordenadas
# 2) tirar error en el caso que se pida una fecha que no haya
# 3) no suponer lo de los espacios, tiene que haber alguna funcion que me permita trabajar genericamente
# 4) que el programa funcione aunque haya espacios arriba y abajo de mas
# 5) optimizar algunas cosas, quizas hay redundancia y demas.
# 6) emprolijar el codigo, nombres de variables, funciones y demas.
# 7) que los None no sean un string que sea literalmente None