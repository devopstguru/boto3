#!/bin/bash

sudo df -h >> dfout.txt
cat dfout.txt | sed 's/\|/ /'|awk '{print $6}' >> mntin.txt
for mpoint in $(cat mntin.txt); do mkdir 777 $mpoint; done
