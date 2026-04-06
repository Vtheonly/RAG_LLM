:- compile(util).
:- compile(measure).

/* 1. Permutations in one-line notation. */

/* The permutation p on {0,...,n-1} is represented by the list
   [p(0),...,p(n-1)] called its 'one-line notation'. Any such list
   contains each element of {0,...,n-1} exactly once. */

/* permline(L,K,N) iff L is a linear list (no duplicates) of length K 
   with elements in {0,...,N-1}. */
permline([],0,_).
permline([Y|P],K,N) :- K > 0, Km1 is K-1, Nm1 is N-1, in(Y,0,Nm1), 
  permline(P,Km1,N), \+ member(Y,P).

/* permline(L,N) iff L is a linear list (no duplicates) of length N 
   with elements in {0,...,N-1}. */
permline(P,N) :- permline(P,N,N).

/* Example of use of 'measure': */
:- iterate(0,6,permline), halt.
/* The output should contain 1,1,2,6,24,120,720 */

/* 2. Factorial lists */
