import boto3

ec2 = boto3.resource('ec2')
instances = ec2.instances.filter()
srcvm = ec2.Instance('i-077fc02451a53c6a1')
destvm = ec2.Instance('i-072f97b3f5eeba24f')
all_sg_ids = ['']
print(srcvm.id)
print(destvm.id)
print("Fetching source VM security groups")
for instance in instances:
  if instance.id == srcvm.id:
    all_sg_ids = [sg['GroupId'] for sg in instance.security_groups]  
    for sg_id in all_sg_ids:                                         
      print(sg_id)
  if instance.id == destvm.id:
      instance.modify_attribute(Groups=all_sg_ids) 
