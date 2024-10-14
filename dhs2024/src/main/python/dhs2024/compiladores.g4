grammar compiladores;

fragment LETRA : [A-Za-z] ;
fragment DIGITO : [0-9] ;

PA: '(';
PC: ')';
LLA: '{';
LLC: '}';
PYC: ';';
COMA: ',';

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

NUMERO : DIGITO+ ;
WS : [ \t\n\r] -> skip;
ID : (LETRA | '_')(LETRA | DIGITO | '_')* ;

// REGLAS-----------------------------------------------------------------------------------------------------
programa : instrucciones EOF ; //secuencia de instrucciones hasta el final del archivo
instrucciones : instruccion instrucciones //es una instruccion con mas instrucciones 
                |
                ;
tipodato : INT
         |DOUBLE
         |FLOAT
         |BOOLEAN
         |CHAR
         ;

instruccion: declaracion
            | asignacion
            | bloque
            | ifor
            | iif
            | prototipofunc
            | func
            | iwhile
            ;
// ---------------------------------------------------------------------------------------------------------

declaracion: tipodato ID PYC; //int x;

// ---------------------------------------------------------------------------------------------------------

asignacion : ID ASIG opal PYC; //opal(operacion aritmetica logica)

opal : exp log //exp(expresiones aritmeticas) log(expresiones logicas)
     |
     ; 

//PARTE ARITMETICA -----------------------------------------------------------------------------------------
exp : term e; 

e : SUMA term e
  | RESTA term e  
  |           
  ;

term  : factor t; //separo esto para que primero se resuelvan operaciones de * / % y recien ahi despues se suma o resta

t     : MULT factor t
      | DIV factor t
      | MOD factor t
      |
      ;
factor : NUMERO 
       | ID            //ACORDATE QUE ID ES UNA VARIABLE 
       | PA exp PC    // (expresion eemmplo 4*10-1)
       ;

// PARTE LOGICA------------------------------------------------------------------------------------------

log : comp exp
    | igdis exp //igual o distinto
    |
    ;

comp: MAY 
    | MIN 
    | MINEQ 
    | MAYEQ 
    ;
igdis : EQ 
      | DISTEQ
      ;

//-----------------------------------------------------------------------------------------------------------

bloque : LLA instrucciones LLC; //bloque de codigo

//FOR --------------------------------------------------------------------------------------------------------

ifor : FOR PA init PYC cond PYC iter PC bloque; //for(init ; cond ; iter) instruccion
init : asignacion;
cond : opal;
iter : opal;

//IF---------------------------------------------------------------------------------------------------------

iif: IF PA opal PC bloque // suponiendo if(x)
   | IF PA opal PC bloque ELSE bloque ; //una estructura con if else

//-----------------------------------------------------------------------------------------------------------

iwhile : WHILE PA ID PC bloque ;
      














prototipofunc : tipodatof ID PA argumentos PC PYC; 

func : prototipofunc bloque;

tipodatof : INT
         |DOUBLE
         |FLOAT
         |VOID
         |BOOLEAN
         |CHAR
         ;

argumentos : tipodato ID COMA argumentos
           | tipodato ID
           | 
           ;


