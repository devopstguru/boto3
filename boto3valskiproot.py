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
######################################################################################
############### Enter Source and Destinaton server details ###########################
######################################################################################
new_instance ='dev-amibake-09' #input("Enter new Instance Name :") #Destination EC2 Instance
instance =ec2.Instance('i-077fc02451a53c6a1') #Source EC2 Instance
#####################################################################################
volumes = instance.volumes.all()
#print(type(volumes))
DeviceList = []
DeviceList = ['/dev/sdg','/dev/sdh','/dev/sdi','/dev/sdj','/dev/sdk','/dev/sdl','/dev/sdm','/dev/sdn','/dev/sdo','/dev/sdp','/dev/sdq','/dev/sdr','/dev/sds','/dev/sdt','/dev/sdu','/dev/sdv','/dev/sdw','/dev/sdx','/dev/sdy','/dev/sdz']
print('  {0:3}    {1:30s}  {2:15s}     {3:15s}   {4:15s}   {5:10s}'.format("S No. ", "NAME", "INSTANCE ID", "IP ADDRESS",'AvailabilityZone', "STATE"))
print('----------------------------------------------------------------------------------------------------------------- \n')

ec2_vm = boto3.resource('ec2', region_name = 'us-west-2')

for ec2_instance in ec2_vm.instances.all():

        for tag in ec2_instance.tags:

          if tag['Value'] == new_instance:
              print('  {0:3}  ',format("Name"))
              print("Restackign started for : ",new_instance)
              for v in volumes:
                  if v.attachments[0][u'Device'] == '/dev/sda1':
                      print("root volume is skipped")
                  else:
                      devicecount +=1
                      print(v.id)
                      #volume = ec2.Volume(v.id)
                      volid=v.id
                      snapshot = ec2.create_snapshot(
                          VolumeId=volid,
                          TagSpecifications=[
                              {
                                  'ResourceType': 'snapshot',
                                  'Tags': [
                                       {
                                           'Key': 'Name',
                                           'Value': new_instance
                                       },
                                  ]
                          },
                      ])
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
                              DryRun=False,
                              TagSpecifications=[
                                  {
                                      'ResourceType': 'volume',
                                      'Tags': [
                                          {
                                              'Key': 'Name',
                                              'Value': new_instance 
                                          },
                                       ]
                                  },
                              ])
                          #vids = response.id #vid.id
                          #retrieve volume id and wait till it is available
                          volume_id = response.id
                          volume_available_waiter.wait(VolumeIds=[volume_id])
                          print("New Volume ID : ", volume_id)
                          time.sleep(20) 
                          response= ec2_instance.attach_volume(Device=DeviceList[devicecount], InstanceId=ec2_instance.id, VolumeId=volume_id)
                          # wait till the volume is properly attached to EC2 instance
                          volume_attached_waiter.wait(VolumeIds=[volume_id])
                          #print("State : ",response['State'])
                          client = boto3.client('ec2', region_name = 'us-west-2')
                          print("snapshot Id:",snapshot.id)
                          sid = snapshot.id
                          responses = client.delete_snapshot(SnapshotId=sid)
