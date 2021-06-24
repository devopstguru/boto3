#!/bin/bash

######################## COPYING /etc/fstab entries onto S3 ##################
input="/etc/fstab"
rm  /tmp/fstabbackup
rm  /tmp/fstab
while IFS= read -r line
do
  echo "$line" >> /tmp/fstab
done < "$input"
cat /tmp/fstab | grep -A100 /backup >> /tmp/fstabbackup


/usr/local/bin/aws s3 cp /tmp/fstabbackup s3://cf-templates-tqftrjy4ugkm-us-east-1
######################## COPYING /etc/hosts entries onto S3 ##################
input="/etc/hosts"
rm  /tmp/etchostsbkp
rm  /tmp/hostbkp
while IFS= read -r line
do
  echo "$line" >> /tmp/hostbkp
done < "$input"
cat /tmp/hostbkp | grep -A100 /backup >> /tmp/etchostsbkp


/usr/local/bin/aws s3 cp /tmp/etchostsbkp s3://cf-templates-tqftrjy4ugkm-us-east-1

######################## COPYING /etc/hostname entries onto S3 ################
input="/etc/hostname"
rm  /tmp/etchostnamebkp
rm  /tmp/hostnamebkp
while IFS= read -r line
do
  echo "$line" >> /tmp/hostnamebkp
done < "$input"
cat /tmp/hostnamebkp | grep -A100 /backup >> /tmp/etchostnamebkp


/usr/local/bin/aws s3 cp /tmp/etchostnamebkp s3://cf-templates-tqftrjy4ugkm-us-east-1
###################### COPYING mount points entries onto S3 ##################
rm /tmp/mntout.txt
sudo df -h >> /tmp/mntout.txt
cat /tmp/mntout.txt | sed 's/\|/ /'|awk '{print $6}' >> /tmp/mntin.txt
#for mpoint in $(cat in.txt); do mkdir 777 $mpoint; done
/usr/local/bin/aws s3 cp /tmp/mntin.txt s3://cf-templates-tqftrjy4ugkm-us-east-1/
