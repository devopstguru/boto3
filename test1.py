import boto3
ec2 = boto3.resource('ec2')


instance = ec2.Instance('i-077fc02451a53c6a1')
volumes = instance.volumes.all()

for v in volumes:
    print("List of volumes attached",v.id)

instance = 'i-077fc02451a53c6a1'
instance1 = 'i-077fc02451a53c6a1'
if instance1 == instance :
  volume = ec2.Volume('vol-0a5dc473a57518910')
  snapshot = ec2.create_snapshot(
    VolumeId=volume.id,
    TagSpecifications=[
        {
        'ResourceType': 'snapshot',
        'Tags' : volume.tags,
        },
    ],
    Description='Snapshot of volume ({})'.format(volume.id),
  )
