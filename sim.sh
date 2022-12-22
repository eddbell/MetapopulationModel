#!/bin/bash

for iNEVT in 0 1 2 3 4 5 6
do
  gnome-terminal -- Python3 Main.py -c 4 -nsim 5 -NGI 10
done
