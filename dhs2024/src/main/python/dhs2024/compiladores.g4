grammar compiladores;

fragment LETRA : [A-Za-z] ;
fragment DIGITO : [0-9] ;

PA: '(';
PC: ')';
LLA: '{';
LLC: '}';
PYC: ';';
COMA: ',';
COMDOBLE: '"';

SUMA : '+' ;
RESTA : '-';
MULT : '*';
DIV : '/';
MOD : '%';

MAS : '++';
MEN : '--';
ASIG : '=' ;

EQ : '==';
DISTEQ : '!=';
MIN : '<';
MINEQ : '<=';
MAY : '>';
MAYEQ : '>=';

AND : '&&'; 
OR : '||';
NOT: '!';

INT:'int';
FLOAT : 'float';
DOUBLE: 'double';
CHAR: 'char';
VOID: 'void';
BOOLEAN: 'bool';

WHILE :'while';
FOR: 'for';
IF: 'if';
ELSE: 'else';
DO: 'do';
MAIN:'main';

NUMERO : DIGITO+ ;
NUMEROFLOAT: DIGITO.DIGITO ;
WS : [ \t\n\r] -> skip;
ID : (LETRA | '_')(LETRA | DIGITO | '_')* ;
LET : LETRA+ ;

// REGLAS----------------------------------------------------------------------------------------------------
programa : instrucciones EOF ; //secuencia de instrucciones hasta el final del archivo

instrucciones : instruccion instrucciones //es una instruccion con mas instrucciones 
                |
                ;
//todas las sentencias que puede tener el programa
instruccion: declaracion (PYC | ) //hacemos esto para que el programa lo tome como valido a la sentencia para poder controlar nosotros este error
            | asignacion (PYC | ) // el | y el espacio significa que puede no estar el punto y coma
            | bloque
            | ifor
            | iif
            | prototipofunc
            | func
            | iwhile
            | llamadafunc
            ;

// ----------------------------------------------------------------------------------------------------------
declaracion: tipodato (ID | NUMERO) ; //int x;

// asignacion------------------------------------------------------------------------------------------------
 //para el char USAMOS LET
asignacion : ID ASIG opal
           | ID ASIG llamadafunc
           | ID ASIG COMDOBLE LET COMDOBLE //para los chars, se reutiliza ID
           ; //opal(operacion aritmetica logica)

//tipos de datos para inicializar variables
tipodato : INT
         |DOUBLE
         |FLOAT
         |BOOLEAN
         |CHAR
         ;

//tipos de datos para los prototipos de las funciones
tipodatof : tipodato
          | VOID
          ;

//expresiones aritmeticas-logicas----------------------------------------------------------------------------
opal : termino1 parteor;
parteor: OR opal
       |  
       ;
termino1: termino2 parteand;
parteand: AND termino1
        | 
        ;
termino2: termino3 parteigualdad;
parteigualdad: EQ termino2
             | DISTEQ termino2
             |
             ;
termino3: termino4 parterelacion;
parterelacion: MAY termino3
             | MIN termino3
             | MINEQ termino3
             | MAYEQ termino3
             |
             ;
termino4 : termino5 partesumaresta; 
partesumaresta : SUMA termino4
               | RESTA termino4 
               |           
               ;
termino5  : termino6 partemuldivmod; 
partemuldivmod: MULT termino5
              | DIV termino5
              | MOD termino5
              |
              ;
termino6: termino7 partepreincr;
partepreincr: MAS termino6
              | MEN termino6
              |
               ;
termino7: factor parteposincr;
parteposincr: termino7 MAS
              | termino7 MEN
              |
              ;

factor : NUMERO
       | NUMEROFLOAT
       | ID         
       | PA opal PC    
       ;

//bloque de codigo-------------------------------------------------------------------------------------------
bloque : LLA instrucciones LLC; //bloque de codigo

//FOR -------------------------------------------------------------------------------------------------------
ifor : FOR (PA | ) init PYC cond PYC iter PC bloque; //for(init ; cond ; iter) instruccion
init : tipodato ID ASIG opal;
cond : opal;
iter : asignacion;
bloquefor : LLA instrucciones LLC; //bloque solo para for para que no cree contexto

//IF---------------------------------------------------------------------------------------------------------
iif: IF (PA | ) opal PC bloque // suponiendo if(x)
   | IF (PA | ) opal PC bloque ELSE bloque ; //una estructura con if else

//WHILE------------------------------------------------------------------------------------------------------
iwhile : WHILE (PA | ) opal PC bloque ;
      
//Prototipo de funcion---------------------------------------------------------------------------------------
declargumentos : tipodato ID;

prototipofunc : tipodatof ID (PA | ) argumentos PC (PYC | ); 

argumentos : declargumentos COMA argumentos
           | declargumentos
           | 
           ;

//funciones--------------------------------------------------------------------------------------------------

/*se realiza un bloque especial para agregar los argumentos de la funcion al contexto  */
bloqueespecial : LLA instrucciones LLC;

/*cunado sepa el nombre de la funcion necesito traer sus argumentos para crear el contexto */
nombrefuncion: ID ;
func :  tipodatofunc nombrefuncion (PA | ) argumentosf PC bloqueespecial;
argumentosf : funcargumentos COMA argumentosf
            | funcargumentos
            | 
            ; 
            
tipodatofunc: tipodatof;

funcargumentos : tipodato ID;

llamadafunc : nombre PA argumentosllamada PC (PYC | );

argumentosllamada : llamargumentos COMA argumentosllamada
                  | llamargumentos
                  | 
                  ; 

llamargumentos: ID;

nombre: ID;

fmain : tipodatomain MAIN PA PC bloque;
tipodatomain: INT;