# Iac_Pulumi_EC2


---

# Infraestructura con Pulumi en AWS

Este repositorio contiene un único archivo `__main__.py` que define una infraestructura mínima en Amazon Web Services (AWS) utilizando la herramienta **Pulumi** con Python. El objetivo es crear una instancia EC2 con una AMI específica (`Cloud9Ubuntu22`), configurar sus recursos asociados y exponer sus datos relevantes.

## Descripción detallada del archivo `__main__.py`

A continuación, se describe paso a paso lo que realiza el código:

### 1. Importación de librerías

```python
import pulumi
import pulumi_aws as aws
```

Se importan los módulos necesarios de Pulumi y su proveedor para AWS, lo cual permite interactuar con los servicios de Amazon mediante código Python.

---

### 2. Búsqueda de la AMI "Cloud9Ubuntu22"

```python
ami = aws.ec2.get_ami(
    most_recent=True,
    owners=["amazon"],
    filters=[
        {"name": "name", "values": ["*Cloud9Ubuntu22*"]},
        {"name": "virtualization-type", "values": ["hvm"]},
    ]
)
```

Se consulta a AWS por la imagen de máquina (AMI) más reciente que coincida con el patrón `"*Cloud9Ubuntu22*"`, ofrecida por Amazon y con virtualización del tipo HVM.

---

### 3. Creación del Security Group

```python
sec_group = aws.ec2.SecurityGroup("web-sec-group",
    description="Enable SSH and HTTP",
    ingress=[
        {"protocol": "tcp", "from_port": 22, "to_port": 22, "cidr_blocks": ["0.0.0.0/0"]},
        {"protocol": "tcp", "from_port": 80, "to_port": 80, "cidr_blocks": ["0.0.0.0/0"]},
    ],
    egress=[{"protocol": "-1", "from_port": 0, "to_port": 0, "cidr_blocks": ["0.0.0.0/0"]}]
)
```

Se crea un grupo de seguridad que permite el acceso a la instancia EC2 por los puertos:

- **22 (SSH)**: para poder acceder remotamente a través de una terminal.
- **80 (HTTP)**: para recibir tráfico web.
- También se permite salida hacia cualquier destino por cualquier puerto (regla `egress`).

---

### 4. Creación de la instancia EC2

```python
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
```

Aquí se crea una instancia EC2 con las siguientes características:

- **Tipo de instancia**: `t2.micro`, dentro del nivel gratuito de AWS.
- **AMI**: la encontrada anteriormente (`Cloud9Ubuntu22`).
- **Par de claves**: se especifica `vockey`, necesario para acceso SSH.
- **Grupo de seguridad**: se asocia el creado anteriormente.
- **Volumen raíz**: se configura con un tamaño de **20 GB**.
- **Etiqueta (tag)**: se asigna el nombre `"Pulumi_VM"` para facilitar su identificación.

---

### 5. Exportación de salidas

```python
pulumi.export("public_ip", vm.public_ip)
pulumi.export("public_dns", vm.public_dns)
pulumi.export("instance_id", vm.id)
```

Al final, el código exporta datos útiles una vez que la infraestructura se ha creado:

- **Dirección IP pública** de la instancia.
- **Nombre DNS público**.
- **ID de la instancia EC2**.

---

Este script permite automatizar el aprovisionamiento de una máquina virtual lista para desarrollo, utilizando buenas prácticas de infraestructura como código (IaC) y aprovechando el poder de Pulumi sobre AWS.

---
