import boto3
import time
import sys


ec2 = boto3.resource('ec2')
#instance = ec2.Instance('i-077fc02451a53c6a1')
volumes = instance.volumes.all()
for v in volumes:
    print("current volume id: ",v.id)
    volume = ec2.Volume(v.id)
    snapshot = ec2.create_snapshot(
      VolumeId=volume.id)
    print("Snapshot Id:",snapshot.id)
    while snapshot.state != 'completed':
      print (snapshot.progress)
      print ("Snapshot under creation")
      time.sleep(10)
      snapshot.load()
    else:
      print("snapshot READY")

      response= ec2.create_volume(
            AvailabilityZone='us-west-2a',
            Encrypted=False,
            #Iops=100,
            #KmsKeyId='string',
            #Size=int(size),
            SnapshotId=snapshot.id,
            VolumeType='gp2',    #standard'|'io1'|'gp2'|'sc1'|'st1',
            DryRun=False)

#s = ec2.describe_volumes()
#print(s.status)
      print("New volume Id:",response.id)
      result = conn.attach_volume (response.id, vm,"/dev/sdg")
      #print("Volume ID : ", response[VolumeId])
#time.sleep(10)
      #response= ec2.attach_volume(InstanceId=instance_dict[iId][0], VolumeId=response['VolumeId'])
            #print("State : ",response['State'])
