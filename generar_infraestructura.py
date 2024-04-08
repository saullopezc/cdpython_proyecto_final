import boto3
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Leer las credenciales de AWS y las configuraciones desde las variables de entorno
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_region = os.getenv('AWS_REGION')
ec2_instance_type = os.getenv('EC2_INSTANCE_TYPE')
ec2_ami_id = os.getenv('EC2_AMI_ID')
ec2_key_name = os.getenv('EC2_KEY_NAME')
rds_db_instance_class = os.getenv('RDS_DB_INSTANCE_CLASS')
rds_mysql_db_name = os.getenv('RDS_MYSQL_DB_NAME')
rds_mysql_instance_identifier = os.getenv('RDS_MYSQL_INSTANCE_IDENTIFIER')
rds_mysql_username = os.getenv('RDS_MYSQL_USERNAME')
rds_mysql_password = os.getenv('RDS_MYSQL_PASSWORD')
rds_postgres_db_name = os.getenv('RDS_POSTGRES_DB_NAME')
rds_postgres_instance_identifier = os.getenv('RDS_POSTGRES_INSTANCE_IDENTIFIER')
rds_postgres_username = os.getenv('RDS_POSTGRES_USERNAME')
rds_postgres_password = os.getenv('RDS_POSTGRES_PASSWORD')

# Configurar las credenciales de AWS
boto3.setup_default_session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=aws_region
)

# Crear una instancia de EC2
ec2 = boto3.resource('ec2')
instance = ec2.create_instances(
    ImageId=ec2_ami_id,
    InstanceType=ec2_instance_type,
    KeyName=ec2_key_name,
    MinCount=1,
    MaxCount=1
)[0]

print(f"Instancia EC2 creada con ID: {instance.id}")

# Crear una instancia de RDS MySQL
rds_mysql = boto3.client('rds')
rds_mysql.create_db_instance(
    DBName=rds_mysql_db_name,
    DBInstanceIdentifier=rds_mysql_instance_identifier,
    AllocatedStorage=20,
    DBInstanceClass=rds_db_instance_class,
    Engine='mysql',
    MasterUsername=rds_mysql_username,
    MasterUserPassword=rds_mysql_password,
    PubliclyAccessible=True
)

print("Instancia RDS MySQL creada")

# Crear una instancia de RDS PostgreSQL
rds_postgres = boto3.client('rds')
rds_postgres.create_db_instance(
    DBName=rds_postgres_db_name,
    DBInstanceIdentifier=rds_postgres_instance_identifier,
    AllocatedStorage=20,
    DBInstanceClass=rds_db_instance_class,
    Engine='postgres',
    MasterUsername=rds_postgres_username,
    MasterUserPassword=rds_postgres_password,
    PubliclyAccessible=True
)

print("Instancia RDS PostgreSQL creada")

# Esperar a que la instancia EC2 esté en estado "running"
instance.wait_until_running()

# Obtener la dirección IP pública de la instancia EC2
public_ip = instance.public_ip_address
print(f"Dirección IP pública de la instancia EC2: {public_ip}")

# Configurar SSH para conectarse a la instancia EC2
ssh = boto3.client('ssh')

# Instalar Docker en la instancia EC2
commands = [
    'sudo apt-get update',
    'sudo apt-get install -y docker.io',
    'sudo systemctl start docker',
    'sudo systemctl enable docker',
]

for command in commands:
    ssh.send_command(public_ip, command)

print("Docker instalado en la instancia EC2")

# Enviar el archivo Docker Compose a la instancia EC2
ssh.send_file(public_ip, 'docker-compose.yml', '/home/ec2-user/docker-compose.yml')

print("Archivo Docker Compose enviado a la instancia EC2")

# Ejecutar Docker Compose en la instancia EC2
command = 'docker-compose up -d'
ssh.send_command(public_ip, command)

print("Docker Compose ejecutado en la instancia EC2")

# Leer los logs de Docker Compose para obtener el enlace del Jupyter Notebook
command = 'docker-compose logs'
output = ssh.send_command(public_ip, command)

jupyter_link = None
for line in output.splitlines():
    if 'http://' in line:
        jupyter_link = line.strip()
        break

if jupyter_link:
    print(f"Enlace del Jupyter Notebook: {jupyter_link}")
else:
    print("No se pudo obtener el enlace del Jupyter Notebook desde los logs")