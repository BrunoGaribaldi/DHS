grammar compiladores;

fragment LETRA : [A-Za-z] ;
fragment DIGITO : [0-9] ;

//INST : (LETRA | DIGITO | [- ,;{}()+=>] )+ '\n'; es una letra, un digito .. no quiero que exceda el guion 
PA: '(';
PC: ')';
LLA: '{';
LLC: '}';
PYC: ';';
WHILE :'while';
NUMERO : DIGITO+ ;
INT:'int';
FOR: 'for';
SUMA : '+' ;
RESTA : '-';
MULT : '*';
DIV : '/';
MOD : '%';
ASIG : '=' ;
MIN : '<' ;
MINEQ : '<=' ;
MAY : '>' ;
MAYEQ : '>=';
EQ : '==';
AND : '&&' ; 
OR : '||' ;
NOT : '!=' ;




WS : [ \t\n\r] -> skip;
ID : (LETRA | '_')(LETRA | DIGITO | '_')* ;
/*OTRO : . ;


s : ID     {print("ID ->" + $ID.text + "<--") }         s
  | NUMERO {print("NUMERO ->" + $NUMERO.text + "<--") } s
  | OTRO   {print("Otro ->" + $OTRO.text + "<--") }     s
  | EOF
  ;
  */

//si : s EOF; que comience en un nodo, que sea solo la razi del arbol
//s: PA s PC s  s permite la anidacion, se cierra un parentesis y se puede abrirotro parentesis. Verifica balance de parentesis
  //|
//;

programa : instrucciones EOF ; //secuencia de instrucciones hasta el final del archivo

instrucciones : instruccion instrucciones //es una instruccion con mas instrucciones 
                |
                ;
instruccion: declaracion
            | iwhile
            | bloque
//            | ifor
//            | iif
            | asignacion PYC
            ;

declaracion: INT ID PYC ;

asignacion : ID ASIG opal; //opal es operacion aritmetca logica

opal : exp log igdis; //completar. Las expresiones (exp) son la parte aritmerica. Me falta la parte logica.

exp : term e; // por ejemplo 4*10/2 + ..... termino es 4*10/2, e es suma o resta, 
e : SUMA term e
  | RESTA term e  
  |           //hasta que termine
  ;

term  : factor t; //separo esto para que primero se resuelvan operaciones de * / % y recien ahi despues se suma o resta
t     : MULT factor t
      | DIV factor t
      | MOD factor t
      |
      ;

log : comp
    |
    ;

comp: MAY exp
    | MIN exp
    | MINEQ exp
    | MAYEQ exp
    |
    ;

factor : NUMERO 
       | ID            //ACORDATE QUE ID ES UNA VARIABLE 
       | PA exp PC    // (expresion eemmplo 4*10-1)
       ;

igdis : igual 
   |
   ;

igual: EQ 
     | NOT
     | 
     ;

iwhile : WHILE PA ID PC instruccion ;//llave representa una instruccion compuesta, despues del while viene siempre una instruccion

bloque : LLA instrucciones LLC; 

//ifor : FOR PA init PYC cond PYC iter PC instruccion ; //for(init ; cond ; iter) instruccion
//init : ;
//cond : ;
//iter : ;
