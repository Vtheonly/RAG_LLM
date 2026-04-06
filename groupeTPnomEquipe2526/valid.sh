#!/bin/bash

echo "Table of permutations in one-line notation, up to size 5, in the files data/permlineI.pl:"

for (( i=0; i<=5; i++ )) do
  ./write_swi permut.pl permline $i data/permline$i.pl
done

exit

