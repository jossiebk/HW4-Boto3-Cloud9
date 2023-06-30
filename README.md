# HW4-Boto3-Cloud9
Tarea 4, desarrollo de un programa con Boto 3 en Cloud9 para infraestructura sencilla.

● Create VPC
    ○ Name: vpc-hw4
    ○ CIDR IPv4: 10.0.0.0/16
    ○ Availability zone: us-east-1a
    
● Create subnet
    ○ VPC: vpc-hw4
    ○ Name: subnet-hw4
    ○ CIDR IPv4: 10.0.0.0/24
    ○ Availability zone: us-east-1a
    
● Create a route table
    ○ Name: route-table-hw4
    ○ VPC: vpc-hw4

● Create a internet gateway
    ○ Name: igw-hw4
    ○ Attach to vpc: vpc-hw4
● Create a key pair
    ○ Name: key-pair-hw4
● Create EC2
    ○ Name: ec2-hw4
    ○ Image Id: ami-0b54418bdd76353ce
    ○ Instance type: t2.micro
    ○ Key pair: key-pair-hw4
    ○ VPC: vpc-hw4
