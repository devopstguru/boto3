import boto3
import time
ec2 = boto3.resource('ec2', region_name = 'us-west-2')
ec2_client = boto3.client('ec2', region_name = 'us-west-2')
volume_available_waiter = ec2_client.get_waiter('volume_available')
volume_attached_waiter = ec2_client.get_waiter('volume_in_use')
iId = int(1)
vids = []
ec2_instance = boto3.client('ec2', region_name = 'us-west-2')
vmresponse = ec2_instance.describe_instances()
instance_dict = {}
count = 1
devicecount = 0

new_instance ='restack-check' #input("Enter new Instance Name :")
instance =ec2.Instance('i-0aa30ac7088563e5a')
volumes = instance.volumes.all()
#print(type(volumes))
DeviceList = []
DeviceList = ['/dev/sdg','/dev/sdh','/dev/sdi','/dev/sdj','/dev/sdk','/dev/sdl','/dev/sdm','/dev/sdn','/dev/sdo','/dev/sdp','/dev/sdq','/dev/sdr','/dev/sds','/d
ev/sdt','/dev/sdu','/dev/sdv','/dev/sdw','/dev/sdx','/dev/sdy','/dev/sdz']
print('  {0:3}    {1:30s}  {2:15s}     {3:15s}   {4:15s}   {5:10s}'.format("S No. ", "NAME", "INSTANCE ID", "IP ADDRESS",'AvailabilityZone', "STATE"))
print('----------------------------------------------------------------------------------------------------------------- \n')

for reservation in vmresponse["Reservations"]:
    for instance in reservation["Instances"]:

        if instance['State']['Name'] == "running":
            if instance.__contains__("Tags"):

              if instance["Tags"][0]["Value"] == new_instance:
                print ("\t Started Restacking: ", new_instance)

                instance_dict[count] = instance["InstanceId"],instance['Placement']['AvailabilityZone']
                #for DeviceName in DeviceList:

                for v in volumes:
                  if 'restack-check' == new_instance:
                    devicecount +=1
                    print(v.id)
                    #volume = ec2.Volume(v.id)
                    volid=v.id
                    snapshot = ec2.create_snapshot(VolumeId=volid)
                    #snapshot = ec2.create_snapshot(VolumeId=volume.id)
                    print(snapshot.id)
                    while snapshot.state != 'completed':
                        print (snapshot.progress)
                        print ("Snapshot under creation")
                        time.sleep(10)
                        snapshot.load()
                    else:
                        print("snapshot READY")
                        response = ec2.create_volume(
                            AvailabilityZone='us-west-2a',
                            Encrypted=False,
                            SnapshotId=snapshot.id,
                            VolumeType='gp2',
                            DryRun=False)
                        vids = response.id #vid.id
                        #print(instance["Tags"][0]["Value"])


                        #retrieve volume id and wait till it is available
                        volume_id = response.id
                        volume_available_waiter.wait(VolumeIds=[volume_id])



                        print("New Volume ID : ", vids)

                        time.sleep(20)
                        for instance in reservation["Instances"]:

                          if instance['State']['Name'] == "running":
                            if instance.__contains__("Tags"):
                              #print(instance["Tags"][0]["Value"])
                              if instance["Tags"][0]["Value"] == new_instance:


                                print(instance["Tags"][0]["Value"])
                                #if instance["Tags"][0]["Value"] == new_instance:
                                response= ec2_instance.attach_volume(Device=DeviceList[devicecount], InstanceId=instance_dict[iId][0], VolumeId=volume_id)

                                # wait till the volume is properly attached to EC2 instance
                                volume_attached_waiter.wait(VolumeIds=[volume_id])

                                print("State : ",response['State'])
                        client = boto3.client('ec2', region_name = 'us-west-2')
                        print("snapshot Id:",snapshot.id)
                        sid = snapshot.id
                        responses = client.delete_snapshot(SnapshotId=sid)
