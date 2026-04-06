/* Usages:

   - Uncomment one line following '% Counting' and run
       swipl -s oeis.pl
     to check some properties by counting.
   - Comment all lines following '% Counting' and run
       swipl -s oeis.pl
     to enter interactive mode and write queries.
*/

:- compile('util.pl').
:- compile('measure.pl').

/* Arbres binaires planaires avec une seule sorte de feuilles :
   Une formule logique conjonctive est
   - soit une proposition atomique
   - soit une conjonction (et) de deux formules logiques conjonctives.
*/
/* :- est la notation Prolog pour <= et la virgule c'est le et */
/* bin1/1 a un seul parametre */
/* p est une formule binaire */
 /* F /\ G est une formule si F est une formule et G est une formule */
%BEGINbin1
bin1(p).
bin1(and(F,G)) :- bin1(F), bin1(G).
%ENDbin1

/* Ajout de la taille :
   - sans rien ajouter, voir [Tarau..]
   - parametrer avec la taille, ici sans PLC
*/
/* bin1/2 a deux parametres, pas de confusion avec bin1/1.
   bin1(T,N) vrai si et seulement si T est une formule de taille N. 
*/
%BEGINbin1size
bin1(p,1).
bin1(and(F1,F2),N) :-
  Nm1 is N-1,
  in(N1,0,Nm1),
  N2 is Nm1-N1,
  bin1(F1,N1), bin1(F2,N2).
%ENDbin1size
% Counting
:- write('Nombre d\'arbres binaires planaires de taille \'size\' avec une seule sorte de feuille de poids 1 : (bin1)'),
   nl, iterate(0,10,bin1),nl, halt.
/* result : 1,0,1,0,2,0,5,0,14,0 */

/* running time :
 Size      : 0
 Solutions : 0
 Time      : 0 ms
 Size      : 1
 Solutions : 1
 Time      : 0 ms
 Size      : 2
 Solutions : 0
 Time      : 0 ms
 Size      : 3
 Solutions : 1
 Time      : 0 ms
 Size      : 4
 Solutions : 0
 Time      : 0 ms
 Size      : 5
 Solutions : 2
 Time      : 0 ms
 Size      : 6
 Solutions : 0
 Time      : 0 ms
 Size      : 7
 Solutions : 5
 Time      : 1 ms
 Size      : 8
 Solutions : 0
 Time      : 1 ms
 Size      : 9
 Solutions : 14
 Time      : 1 ms
 Size      : 10
 Solutions : 0
 Time      : 2 ms
true 
*/



/* Retrait du poids des feuilles, seuls les noeuds sont comptes. */
bin10(p,0).                           /* p est une formule binaire */
bin10(and(F,G),N) :-
  Nm1 is N-1,   /* Nm1 <- N-1 */
  in(N1,0,Nm1), /* choisit N1 dans [0..Nm1] */
  N2 is Nm1-N1,
  bin10(F,N1), bin10(G,N2). /* F /\ G est une formule si F est une formule et G est une formule */

% Counting
%:- write('Nombre d\'arbres binaires planaires de taille \'size\' avec une seul sorte de feuille 
% de poids 0 : (Catalan)'), nl, iterate(0,10,bin10), nl.
/*result : 1,1,2,5,14,42,132,429,1430,4862,16796,... Catalan numbers */
/*
 Size      : 0
 Solutions : 1
 Time      : 0 ms
1
 Size      : 1
 Solutions : 1
 Time      : 0 ms
1,1
 Size      : 2
 Solutions : 2
 Time      : 0 ms
1,1,2
 Size      : 3
 Solutions : 5
 Time      : 1 ms
1,1,2,5
 Size      : 4
 Solutions : 14
 Time      : 0 ms
1,1,2,5,14
 Size      : 5
 Solutions : 42
 Time      : 0 ms
1,1,2,5,14,42
 Size      : 6
 Solutions : 132
 Time      : 3 ms
1,1,2,5,14,42,132
 Size      : 7
 Solutions : 429
 Time      : 13 ms
1,1,2,5,14,42,132,429
 Size      : 8
 Solutions : 1430
 Time      : 43 ms
1,1,2,5,14,42,132,429,1430
 Size      : 9
 Solutions : 4862
 Time      : 149 ms
1,1,2,5,14,42,132,429,1430,4862
 Size      : 10
 Solutions : 16796
 Time      : 513 ms
1,1,2,5,14,42,132,429,1430,4862,16796
*/



/* With negations */
/* unary-binary (Motzkin) trees with a single kind of weightless leaf.*/
%BEGIN_negAnd
negAnd(p,0).
negAnd(and(F,G),N) :-
  Nm1 is N-1,   /* Nm1 <- N-1 */
  in(N1,0,Nm1), /* choisit N1 dans [0..Nm1] */
  N2 is Nm1-N1,
  negAnd(F,N1), negAnd(G,N2). /* F /\ G est une formule si F est une formule et G est une formule */
negAnd(neg(F),N) :-  /* neg(F) est une formule si F est une formule */
  N > 0, Nm1 is N-1, /* Nm1 <- N-1 */
  negAnd(F,Nm1).
%END_negAnd
% Counting
%:- write('Numbers of formulas with negations and conjunctions : (negAnd)'), nl, iterate(0,10,negAnd), nl.
% result: 1,2,6,22,90,394,1806,8558,41586,206098,1037718,... https://oeis.org/A006318.
% Not clear that this counts unary-binary trees by number of internal nodes.


% TODO: + ternary operators, etc


/* Representer les entiers naturels par des arbres/termes */
nat(z,0).
nat(s(T),N) :- N > 0, Nm1 is N-1, nat(T,Nm1).

%Counting
%:- write('Natural integers : (nat)'), nl, iterate(0,10,nat), nl.
/* result : 1,1,1,1,1,1,1,1,1,1,... */


/* Binary plan trees With several distinct atomic propositions? p -> p(I), I is a natural integer. */
binNat(p(I),N) :- nat(I,N).       /* p est une formule binaire si I enst un entier naturel*/
binNat(and(F,G),N) :- 
  Nm1 is N-1,                     /* Nm1 <- N-1 */
  in(N1,0,Nm1),                   /* choisit N1 dans [0..Nm1] */
  N2 is Nm1-N1,
  binNat(F,N1), binNat(G,N2).     /* F /\ G est une formule si F est une formule et G est une formule */

%Counting
%:- write('Binary plan trees With several distinct atomic propositions : (binNat)'), nl, iterate(0,10,binNat), nl.
/* result : 1,2,5,15,51,188,731,2950,12235,51822,223191,... */


/* same with negAnd */
negAndNat(p(I),N) :- nat(I,N).
negAndNat(and(F,G),N) :-
  Nm1 is N-1,
  in(N1,0,Nm1),
  N2 is Nm1-N1,
  negAndNat(F,N1), negAndNat(G,N2).
negAndNat(neg(F),N) :-
  N > 0, Nm1 is N-1,
  negAnd(F,Nm1).

%Counting
%:- write('Unary binary plane/planar trees With several distinct atomic propositions :(negAndNat)'), nl, iterate(0,10,negAndNat), halt.
/* result : 1,3,9,34,145,666,3209,15987,81635,424854,2244735,... */


/* Voir video 24/1/22 : comment valider une bijection entre deux familles
   combinatoires. */

/* Put random indexes in [1..K] on the leafs of binary trees.*/
binIn(K,p(I),0) :- in(I,1,K).
binIn(K,and(F,G),N) :- 
  Nm1 is N-1,
  in(N1,0,Nm1),
  N2 is Nm1-N1,
  binIn(K,F,N1), binIn(K,G,N2).

/* Remove the indexes of binary trees. */
rmIndex(p(1),p).
rmIndex(and(T1,T2),and(U1,U2)) :- rmIndex(T1,U1),rmIndex(T2,U2).

binIn1(X,N) :- binIn(1,X,N).
%Counting
%:- write('Put all leave indexes at 1: (binIn1)'), nl, iterate(0,10,binIn1), nl. 
/* result: 1,1,2,5,14,42,132,429,1430,4862,16796,... Catalan numbers */

/* Proposition 1: binIn1 trees and Catalan trees are in bijection. They are both binary trees with a single kind of leaf. */
binFromBinIn1(Y,N) :- binIn1(X,N), rmIndex(X,Y).
%Counting
% :- write('Put all leave indexes at 1: (binFromBinIn1)'), nl, iterate(0,10,binFromBinIn1), nl.
% 1,1,2,5,14,42,132,429,1430,4862,16796

prop1(T,N) :- binFromBinIn1(T,N), bin10(T,N).
%Counting
%:- write('Validation of Proposition 1'), nl, iterate(0,10,prop1), nl.
% 1,1,2,5,14,42,132,429,1430,4862,16796


/* Proposition 2 : les arbres binaires (Catalan) sont en bijection avec les arbres de
Motzkin (negAndNotLeftLeaf) dont le fils gauche de chaque noeud binaire n'est pas une feuille.

1. Valider en Prolog, en prenant la taille 0 pour les feuilles. 

 Completer la proposition en ajoutant la taille (est-ce la meme ? oui).

2. Trouver cette bijection.

3. Valider cette bijection en Prolog.

\+ pour la negation en Prolog

*/

/* BEGINcond */
/* cond(T) vrai si et seulement si le fils gauche de chaque noeud binaire de T n'est pas une feuille. */
cond(p).
cond(and(and(F1,F2),G)) :- cond(and(F1,F2)), cond(G).
cond(and(neg(F),G)) :- cond(F), cond(G).  /* another solution is: cond(and(neg(F),G)) :- cond(neg(F)), cond(G). */
cond(neg(F)) :- cond(F).
%ENDcond

%BEGIN_negAndNotLeftLeaf
negAndNotLeftLeaf(T,N) :- negAnd(T,N), cond(T).
%END_negAndNotLeftLeaf

% 1. Counting :
%:- write('Unary-binary trees without left leaf'), nl, iterate(0,10,negAndNotLeftLeaf).
/* result : 1,1,2,5,14,42,132,429,1430,4862,16796 (179 ms),... */
/* Catalan numbers. */

/* Example of fusion of two predicates, added by AG, 1/2/22, to explain */
negAndWithCond(p,0).
negAndWithCond(and(and(F1,F2),G),N) :-
  Nm1 is N-1,   /* Nm1 <- N-1 */
  in(N1,0,Nm1), /* choisit N1 dans [0..Nm1] */
  N2 is Nm1-N1,
  negAndWithCond(and(F1,F2),N1), negAndWithCond(G,N2).
negAndWithCond(and(neg(F),G),N) :-
  Nm1 is N-1,   /* Nm1 <- N-1 */
  in(N1,0,Nm1), /* choisit N1 dans [0..Nm1] */
  N2 is Nm1-N1,
  negAndWithCond(neg(F),N1), negAndWithCond(G,N2).
negAndWithCond(neg(F),N) :-  /* neg(F) est une formule si F est une formule */
  N > 0, Nm1 is N-1, /* Nm1 <- N-1 */
  negAndWithCond(F,Nm1).

% 1. Counting :
%:- write('Unary-binary trees without left leaf, with negAndWithCond'), nl, iterate(0,10,negAndWithCond).
/* result : 1,1,2,5,14,42,132,429,1430,4862,16796 (178 ms),... */
/* Catalan numbers. */


% Same trees?
negAndNotLeftLeafandBin(T,N) :- negAndNotLeftLeaf(T,N), bin10(T,N).
%Counting :
%:- write('Unary-binary trees without left leaf and binary'), nl, iterate(0,10,negAndNotLeftLeafandBin).
% No: smaller numbers

/* 2. bijection */
% bij(X,Y) :-

/* 3. Valider une bijection */

/* TODO :
  - (difficile) trouver une bijection entre ces arbres de Motzkin particuliers
    et les arbres de Catalan.
  - decrire cette bijection comme rmIndex.
  - valider par comptage.
*/

/* Poids aux feuilles */
binInWithLeafWeight(K,p(I),I) :- in(I,1,K).
binInWithLeafWeight(K,and(F,G),N):-
  Nm1 is N-1,
  in(N1,0,Nm1),
  N2 is Nm1-N1,
  binInWithLeafWeight(K,F,N1), binInWithLeafWeight(K,G,N2).

%:- write('Binary trees with weight on leafs : (binInWithLeafWeight)'), nl ,iterate(2,10,binInWithLeafWeight), nl.

/* lambda termes */

/* Arbres de Motzkin avec des entiers naturels aux feuilles */

motzkinNat(var(I),N) :- in(I,0,N).
motzkinNat(app(F,G),N) :-
  Nm1 is N-1,
  in(N1,0,Nm1),
  N2 is Nm1-N1,
  motzkinNat(F,N1), motzkinNat(G,N2).
motzkinNat(lam(F),N) :-
  N > 0, Nm1 is N-1,
  motzkinNat(F,Nm1).

/* This definition cannot be complete

closed(lam(F),N) :-
  N > 0, Nm1 is N-1,
  termsPossiblyWithSomeFreeVars(F,Nm1).

closed(app(T1,T2),N) :-
  Nm1 is N-1,
  in(N1,0,Nm1),
  N2 is Nm1-N1,
  closed(T1,N1), closed(T2,N2). /* a(T1,T2) */
*/

/* m-open terms */

m_open(M,var(I),0) :- M > 0, Mm1 is M-1, in(I,0,Mm1).

m_open(M,lam(F),N) :-
  N > 0, Nm1 is N-1, Mp1 is M+1,
  m_open(Mp1,F,Nm1).

m_open(M,app(T1,T2),N) :-
  Nm1 is N-1,
  in(N1,0,Nm1),
  N2 is Nm1-N1,
  m_open(M,T1,N1), m_open(M,T2,N2). /* a(T1,T2) */

closedTerms(T,N) :- m_open(0,T,N).

/* ?- m_open(1,T,3).

...
T = lam(app(lam(var(2)), var(0)))
*/

