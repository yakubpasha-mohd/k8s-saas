import boto3

def get_latest_ami(region):
    ec2_client = boto3.client("ec2", region_name=region)

    images = ec2_client.describe_images(
        Owners=["amazon"],
        Filters=[
            {"Name": "name", "Values": ["amzn2-ami-hvm-*"]},
            {"Name": "architecture", "Values": ["x86_64"]},  # ✅ FIX
            {"Name": "state", "Values": ["available"]}
        ]
    )

    images_sorted = sorted(
        images["Images"],
        key=lambda x: x["CreationDate"],
        reverse=True
    )

    return images_sorted[0]["ImageId"]


def create_instance(instance_type, name, region):
    ec2 = boto3.resource("ec2", region_name=region)
    region = "us-east-1"
    # ✅ FIX: define ami_id
    ami_id = get_latest_ami(region)

    instances = ec2.create_instances(
        ImageId=ami_id,
        MinCount=1,
        MaxCount=1,
        InstanceType=instance_type,
        KeyName="aws-ue-east1-keys",
        SecurityGroupIds=["sg-0f06554bdadb085bc"],
        SubnetId="subnet-0b4fc52429428a870",
        TagSpecifications=[
            {
                "ResourceType": "instance",
                "Tags": [{"Key": "Name", "Value": name}],
            }
        ],
    )

    instance = instances[0]
    instance.wait_until_running()
    instance.reload()

    return {
        "id": instance.id,
        "public_ip": instance.public_ip_address,
    }
