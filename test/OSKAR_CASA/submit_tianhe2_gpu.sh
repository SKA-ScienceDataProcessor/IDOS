#!/bin/sh
for n in $(seq 2 -1 2)
do 
   for i in $(seq 1 -1 1)
   do
     yhbatch -N $n -n $n -p gpu --dependency=singleton oskar_casa.sh $n $i
   done
done
