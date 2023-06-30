import boto3

# Objeto para crear recursos
ec2 = boto3.resource('ec2',region_name='us-east-1')

################################################################################################################################
########################################### PROCESO PARA SERVICIO VPC ##########################################################
################################################################################################################################
print ("########################################### PROCESO PARA SERVICIO VPC ##########################################################")

# Creo la VPC  
vpc = ec2.create_vpc(CidrBlock='10.0.0.0/16') # Asignada a un CIDR
vpc.create_tags(Tags=[{"Key": "Name", "Value": "vpc-hw4"}]) # Asigno el tag de Name pára el nombre de la VPC.
vpc.wait_until_available() # Espera a que la vpc este disponible para continuar.
print("VPC cread: ", vpc.id)

# Creo la Subnet.
subnet = ec2.create_subnet(CidrBlock='10.0.0.0/24', VpcId=vpc.id) # Asigno la subnet a la VPC con su id, y le asigno un CIDR.
subnet.create_tags(Tags=[{"Key": "Name", "Value": "subnet-hw4"}]) # LE asigno el nombre a la Subnet con el tag.
print("Subnet creada: ",subnet.id)


# Creo el  internet Gateway
ig = ec2.create_internet_gateway()
vpc.attach_internet_gateway(InternetGatewayId=ig.id) # Se asocia el internet gateway a la vpc.
ig.create_tags(Tags=[{"Key": "Name", "Value": "igw-hw4"}]) # Asigno el nombre al IG
print("Internet Gateway creado: ", ig.id)

# Creo la tabla de enrutamiento
route_table = vpc.create_route_table()
route = route_table.create_route(DestinationCidrBlock='0.0.0.0/0', GatewayId=ig.id) # Se crea la ruta y se asocia el IG a la tabla de enrutamiento.
route_table.create_tags(Tags=[{"Key": "Name", "Value": "route-table-hw4"}]) # Le asigno el nombre a la tabla de enrutamiento.
print(route_table.id)


# Se asocia la tabla de enrutamiento a la subnet.
route_table.associate_with_subnet(SubnetId=subnet.id)
print("Termina proceso de VPC")

################################################################################################################################
########################################### PROCESO PARA SERVICIO EC2 ##########################################################
################################################################################################################################
print ("########################################### PROCESO PARA SERVICIO EC2 ##########################################################")

# Creo el key pair
outfile = open('key-pair-hw4.pem','w') # Genero un archivo localmente para almacenar el key pair.
key_pair = ec2.create_key_pair(KeyName='key-pair-hw4') # Se crea el key pair con el nombre asignado.
KeyPairOut = str(key_pair.key_material) # Capturo el contenido del keypair creado en una variable.
outfile.write(KeyPairOut) # Se escribe el key pair en el archivo.
print("Se creo key pair")

# Creo la instancia EC2
instances = ec2.create_instances(
    ImageId='ami-01e5ff16fd6e8c542', # Le indico el ami que usara
    MinCount=1,
    MaxCount=1,
    KeyName='key-pair-hw4', # Le asigno el key pair creado previamente.
    NetworkInterfaces=[{ 
        'SubnetId': subnet.id, # Lo asocio a la subnet y vpc creada.
        'DeviceIndex': 0,
        'AssociatePublicIpAddress': True
    }],
    InstanceType='t2.micro', # Le indico el tipo de instancia.
    TagSpecifications=[ # Por medio de tags le asigno el nombre.
        {
            'ResourceType': 'instance',
            'Tags': [
                {
                    'Key': 'Name',
                    'Value': 'ec2-hw4'
                },
            ]
        },
    ]
)

print("Instancia creada: ",instances[0].id)


print("***** PROCESO TERMINADO *****")
