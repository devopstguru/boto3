#!/bin/bash

sudo df -h >> out.txt
cat out.txt | sed 's/\|/ /'|awk '{print $6}' >> in.txt
for mpoint in $(cat in.txt); do mkdir 777 $mpoint; done
