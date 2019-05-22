#!/bin/bash
for i in $(seq 1 $1)
do 
  ($2 || echo "\"$2\" failed, trying again" && false) && break
done
echo "Giving up."