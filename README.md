# Bottom-Up-Parsers
The Above Files Provides the Implementation of LR(0), LR(1), SLR and LALR parsers.   

Example to use use grammars and Strings for input.    
Grammar:    
Eg 1:    

E -> E + T | T    
T -> T * F | F    
F -> ( E ) | id    

Eg 2:

E -> E + T | b A   
T -> T * F | F    
F -> ( E ) | id   
A -> a | &   

Strings:    
id * id   
b a   
a b b b a a     

Note: 
1) Give spaces while entering Grammar and Strings as shown in above examples. If space not given, the parser consider the whole characters as single terminal.( Eg 'id')
2) Use '&' Symbol instead of 'Lambda'.
3) The above parsers first simplify grammer by eliminating Lambda transition using substitution rule while augumenting the Grammar to simplify complexity.
