#!/bin/bash 

for n in $(seq 2 -1 2)
do
   for i in $(seq 1 -1 1)
   do
     yhbatch -N $n -n $n -p gpu --dependency=singleton --time=00:08:00 oskar_casa_daliuge.sh $n  
   done
done

