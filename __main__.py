import pulumi
import pulumi_aws as aws

# 1. Buscar la última AMI de "Cloud9ubuntu22"
ami = aws.ec2.get_ami(
    most_recent=True,
    owners=["amazon"],  # AWS
    filters=[
        {"name": "name", "values": ["*Cloud9Ubuntu22*"]},
        {"name": "virtualization-type", "values": ["hvm"]},
    ]
)

# 2. Crear un Security Group que permita SSH (22) y HTTP (80)
sec_group = aws.ec2.SecurityGroup("web-sec-group",
    description="Enable SSH and HTTP",
    ingress=[
        {"protocol": "tcp", "from_port": 22, "to_port": 22, "cidr_blocks": ["0.0.0.0/0"]},
        {"protocol": "tcp", "from_port": 80, "to_port": 80, "cidr_blocks": ["0.0.0.0/0"]},
    ],
    egress=[{"protocol": "-1", "from_port": 0, "to_port": 0, "cidr_blocks": ["0.0.0.0/0"]}]
)

# 3. Crear la instancia EC2 con 20GB de disco
vm = aws.ec2.Instance("dev-vm",
    instance_type="t2.micro",
    ami=ami.id,
    key_name="vockey",
    vpc_security_group_ids=[sec_group.id],
    root_block_device={
        "volume_size": 20,
        "volume_type": "gp2",
    },
    tags={"Name": "Pulumi_VM"}
)

# 4. Exportar IP pública, DNS y también el ID de la instancia
pulumi.export("public_ip", vm.public_ip)
pulumi.export("public_dns", vm.public_dns)
pulumi.export("instance_id", vm.id)
