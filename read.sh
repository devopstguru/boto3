#!/bin/bash
input="/etc/fstab"
rm  /fstabbackup
rm  /fstab
while IFS= read -r line
do
  echo "$line" >> /fstab
done < "$input"
cat /fstab | grep -A100 /backup >> /fstabbackup


aws s3 cp /fstabbackup s3://cf-templates-tqftrjy4ugkm-us-east-1 
