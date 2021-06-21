import boto3
import time
ec2 = boto3.resource('ec2')



iId = int(1)#int(input('On which instance you want to add Volume : '))

#az = instance_dict[iId][1]

#size = input("Enter Size of Volume (default: 10): ")



ec2_instance = boto3.client('ec2')
response = ec2_instance.describe_instances()
instance_dict = {}
count = 1
new_instance = input("Enter new Instance Name :")
instance =ec2.Instance('i-077fc02451a53c6a1')
volumes = instance.volumes.all()


List1 = []
List1 = ['/dev/sdg','/dev/sdh','/dev/sdi','/dev/sdj','/dev/sdk','/dev/sdl','/dev/sdm','/dev/sdn','/dev/sdo','/dev/sdp','/dev/sdq','/dev/sdr','/dev/sds','/dev/sdt','/dev/sdu','/dev/sdv','/dev/sdw','/dev/sdx','/dev/sdy','/dev/sdz']

#for w in wday:
        #print(w)


print('  {0:3}    {1:30s}  {2:15s}     {3:15s}   {4:15s}   {5:10s}'.format("S No. ", "NAME", "INSTANCE ID", "IP ADDRESS",'AvailabilityZone', "STATE"))
print('----------------------------------------------------------------------------------------------------------------- \n')

for reservation in response["Reservations"]:
    for instance in reservation["Instances"]:
        if instance['State']['Name'] == "running":
            if instance.__contains__("Tags"):
              if instance["Tags"][0]["Value"] == new_instance:
                print('  {0:3}    {1:30s}  {2:15s}   {3:15s}   {4:15s}   {5:10s}'.format(
                    count, instance["Tags"][0]["Value"], instance["InstanceId"],
                    instance["PublicIpAddress"], instance['Placement']['AvailabilityZone'], "RUNNING"))
                instance_dict[count] = instance["InstanceId"],instance['Placement']['AvailabilityZone']
                #count += 1
                for v in volumes:
                  for vcount in List1:
                    print(v.id)
                    volume = ec2.Volume(v.id)
                    snapshot = ec2.create_snapshot(
                      VolumeId=volume.id)
                    print(snapshot.id)
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
                            #print("New Volume ID : ", response['VolumeId'])
                            #time.sleep(10)
                            #response = ec2.attach_volume(Device="/dev/sdc", InstanceId=instance_dict[iId][0], VolumeId=response['VolumeId'])
                            #print("State : ",response['State']


                      vid = response.id
                      print("New Volume ID : ", vid)
                      #vcount = 0
                      time.sleep(10)
                      response= ec2_instance.attach_volume(Device=vcount, InstanceId=instance_dict[iId][0], VolumeId=vid)
                      print("State : ",response['State'])
                      vcount #+= 1
                      client = boto3.client('ec2')
                      print("snapshot Id:",snapshot.id)
                      sid = snapshot.id
                      responses = client.delete_snapshot(SnapshotId=sid)
            else:
                print('  {0:3}    {1:30s}  {2:15s}   {3:15s}   {4:15s}   {5:10s}'.format(
                    count, "No Name", instance["InstanceId"], instance["PublicIpAddress"],instance['Placement']['AvailabilityZone'], "RUNNING"))
                instance_dict[count] = instance["InstanceId"],instance['Placement']['AvailabilityZone']
                #count += 1


        """elif instance['State']['Name'] == "stopped":
            if instance.__contains__("Tags"):
                print('  {0:3}    {1:30s}  {2:15s}   {3:15s}   {4:15s}   {5:10s}'.format(
                    count, instance["Tags"][0]["Value"], instance["InstanceId"], "No IP ADDRESS", instance['Placement']['AvailabilityZone'],
                    "STOPPED"))
                instance_dict[count] = instance["InstanceId"],instance['Placement']['AvailabilityZone']
                count += 1"""
