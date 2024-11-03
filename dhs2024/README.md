# Proyecto Desarrollo de Herramientas de Software IUA 

## Introducción
Trabajo practico 1. Resolvimos las consignas del PDF "ConsignaTP-DHS24"

## Participantes
Este proyecto ha sido desarrollado por:

- **Garibaldi Bruno** 
- **Joaquin Cernik** 


## Mensajes del Programa
A continuación se presentan algunos de los mensajes que el programa muestra en diferentes situaciones:

- **Funcion main**: "Ingresamos al bloque de la funcion main."

- **Prototipo de funcion**: "Detecta que ha encontrado un prototipo de funcion."

- **ERROR: Estas definiendo argumentos con el mismo nombre**: "Esto sucede cuando en el prototipo de una funcion, declaras variables con el mismo nombre. Esto hara que el prototipo no sea guardado en la tabla de simbolos."

- **"ERROR: No declaramos main"**: "No se puede declarar un prototipo de funcion con el nombre main."

- **ERROR: Ya existe el prototipo de funcion con el nombre**: "Esto sucede cuando queremos declarar un prototipo con un nombre de un prototipo ya declarado"

- **ERROR: No existe el prototipo de la funcion**: "Sucede cuando queremos inicializar una funcion cuyo prototipo no existe."

- **Inicializacion funcion**: "Detecta la inicializacion de una funcion."

- **ERROR: Argumento funcion no coincide con prototipo**: "No permite inicializar una funcion cuya lista de argumentos sea diferente a la lista de argumentos del prototipo ya definido"

- **ERROR: Revisar la cantidad de argumentos**: "Detecta que la cantidad de argumentos de la funcion que se quiere inicializar, es distinta a la del prototipo."


- **Se detecto un bloque FOR**: "Nos encontramos con una sentencia for."


- **@@@ Declaracion**: "Por ejemplo <int x;>."

- **ERROR: La varibale esta siendo usada globalmente**: "Declaramos una variable ya declarada globalmente."

- **ERROR:La varibale esta siendo usada localmete**: "Declaramos una variable ya declarada en un contexto local."

- **ERROR: Tenes que declararla primero !**: "Queremos inicializar una variable que no se encuentra declarada. Por ejemplo <x = 4>"

- **WARNING: Estas queriendo usar una variable la cual no conozco el valor, debes inicializarla primero !**: "No es un error ya que C permite esto, sin embargo el valor que contenga la variable es completamente desconocido. Por eso hacemos un Warning"

- **ERROR: La variable no fue declarada!**: "No podemos utilizar una variable que no hayamos declarado."

- **ERROR: No existe el prototitpo de la funcion**: "Estamos llamando a una funcion cuyo prototipo no existe."

- **ERROR: Estas queriendo pasar como argumento un ID no declarado**: "Estamos llamando a una funcion cuyo prototipo no existe. Acordate que en c los argumentos en la llamada a la funcion deben ir en el mismo orden que el prototipo. ATENCION, EN ESTA VERSION NO SE PERMITE PASAR COMO ARGUMENTO UN DATO O NUMERO, SI O SI TIENE QUE SER UNA VARIABLE."

- **ERROR: Estas pasando mas o menos argumentos de los debidos.**: "Sucede cuando en la llamada a la funcion estamos pasando menos argumentos de los que se han guardado en el prototipo de la funcion."


- **ERROR: Estas queriendo pasar un <tipodedato> cuando la funcion recibe un <tipodedato>.**: "Sucede cuando en la llamada queres pasar un tipo de dato (por ejemplo un entero) y en el prototipo de la funcion recibis otro (un double por ejemplo)."

- **ERROR: Se esperaba un tipo de dato: <TipoDato> y queres inicializar: <TipoDato> .**: "Sucede cuando en la inicializacion de la funcion, ponemos un tipo de dato de retorno distinto al que hemos puesto en el prototipo"

## Uso
Para usar el programa, escribir un programa en C en "entrada.txt"