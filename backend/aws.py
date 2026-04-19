import boto3


# ==========================================================
# GET LATEST AMAZON LINUX 2 AMI
# ==========================================================
def get_latest_ami(region):
    ec2 = boto3.client(
        "ec2",
        region_name=region
    )

    images = ec2.describe_images(
        Owners=["amazon"],
        Filters=[
            {
                "Name": "name",
                "Values": [
                    "amzn2-ami-hvm-*"
                ],
            },
            {
                "Name": "architecture",
                "Values": [
                    "x86_64"
                ],
            },
            {
                "Name": "state",
                "Values": [
                    "available"
                ],
            },
        ],
    )

    images_sorted = sorted(
        images["Images"],
        key=lambda x: x[
            "CreationDate"
        ],
        reverse=True,
    )

    return images_sorted[0][
        "ImageId"
    ]


# ==========================================================
# DEFAULT VPC
# ==========================================================
def get_default_vpc(region):
    ec2 = boto3.client(
        "ec2",
        region_name=region
    )

    vpcs = ec2.describe_vpcs(
        Filters=[
            {
                "Name": "isDefault",
                "Values": ["true"],
            }
        ]
    )

    return vpcs["Vpcs"][0]["VpcId"]


# ==========================================================
# DEFAULT SUBNET
# ==========================================================
def get_default_subnet(region):
    ec2 = boto3.client(
        "ec2",
        region_name=region
    )

    subnets = ec2.describe_subnets(
        Filters=[
            {
                "Name": "default-for-az",
                "Values": ["true"],
            }
        ]
    )

    return subnets["Subnets"][0][
        "SubnetId"
    ]


# ==========================================================
# SECURITY GROUP
# ==========================================================
def get_or_create_sg(region):
    ec2 = boto3.client(
        "ec2",
        region_name=region
    )

    vpc_id = get_default_vpc(
        region
    )

    groups = ec2.describe_security_groups(
        Filters=[
            {
                "Name": "group-name",
                "Values": [
                    "k8s-saas-sg"
                ],
            },
            {
                "Name": "vpc-id",
                "Values": [vpc_id],
            },
        ]
    )["SecurityGroups"]

    if groups:
        return groups[0][
            "GroupId"
        ]

    # Create SG
    sg = ec2.create_security_group(
        GroupName="k8s-saas-sg",
        Description="K8s SaaS Cluster Security Group",
        VpcId=vpc_id,
    )

    sg_id = sg["GroupId"]

    # Inbound rules
    ec2.authorize_security_group_ingress(
        GroupId=sg_id,
        IpPermissions=[
            {
                "IpProtocol": "tcp",
                "FromPort": 22,
                "ToPort": 22,
                "IpRanges": [
                    {
                        "CidrIp": "0.0.0.0/0"
                    }
                ],
            },
            {
                "IpProtocol": "tcp",
                "FromPort": 6443,
                "ToPort": 6443,
                "IpRanges": [
                    {
                        "CidrIp": "0.0.0.0/0"
                    }
                ],
            },
            {
                "IpProtocol": "-1",
                "UserIdGroupPairs": [
                    {
                        "GroupId": sg_id
                    }
                ],
            },
        ],
    )

    return sg_id


# ==========================================================
# CREATE INSTANCE
# ==========================================================
def create_instance(
    instance_type,
    name,
    region
):
    ec2 = boto3.resource(
        "ec2",
        region_name=region
    )

    ami_id = get_latest_ami(
        region
    )

    subnet_id = get_default_subnet(
        region
    )

    sg_id = get_or_create_sg(
        region
    )

    instance = ec2.create_instances(
        ImageId=ami_id,
        MinCount=1,
        MaxCount=1,
        InstanceType=instance_type,
        KeyName="aws-ue-east1-keys",
        SecurityGroupIds=[
            sg_id
        ],
        SubnetId=subnet_id,
        TagSpecifications=[
            {
                "ResourceType": "instance",
                "Tags": [
                    {
                        "Key": "Name",
                        "Value": name,
                    }
                ],
            }
        ],
    )[0]

    instance.wait_until_running()
    instance.reload()

    return {
        "id": instance.id,
        "public_ip": instance.public_ip_address,
    }
