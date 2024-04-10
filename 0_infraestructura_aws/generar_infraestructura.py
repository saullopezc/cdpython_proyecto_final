import boto3
import pandas as pd
import numpy as np
import pymysql
import psycopg2
import configparser
from sqlalchemy import create_engine

# Leer el archivo de configuración
config = configparser.ConfigParser()
try:
    config.read('config.conf')
    if not config.sections():
        print("No se encontraron secciones en el archivo de configuración.")
    else:
        print("Archivo de configuración cargado correctamente.")
except Exception as e:
    print("Ocurrió un error al leer el archivo de configuración:", e)

# Configurar el cliente de AWS
aws_rds_conn = boto3.client('rds',
                             aws_access_key_id=config.get('IAM', 'ACCESS_KEY'),
                             aws_secret_access_key=config.get('IAM', 'SECRET_ACCESS_KEY'),
                             region_name=config.get('IAM', 'REGION'))

aws_ec2_conn = boto3.client('ec2',
                             aws_access_key_id=config.get('IAM', 'ACCESS_KEY'),
                             aws_secret_access_key=config.get('IAM', 'SECRET_ACCESS_KEY'),
                             region_name=config.get('IAM', 'REGION'))

# Crear la base de datos MySQL de transacciones
try:
    response = aws_rds_conn.create_db_instance(
        DBInstanceIdentifier=config.get('TRANSACC', 'DB_INSTANCE_ID'),
        DBName=config.get('TRANSACC', 'DB_NAME'),
        DBInstanceClass='db.t2.micro',
        Engine='mysql',
        MasterUsername=config.get('TRANSACC', 'DB_USER'),
        MasterUserPassword=config.get('TRANSACC', 'DB_PASSWORD'),
        Port=int(config.get('TRANSACC', 'DB_PORT')),
        PubliclyAccessible=True,
        VpcSecurityGroupIds=[config.get('VPC', 'SECURITY_GROUP')],
        AllocatedStorage=20
    )
    print(response)
except aws_rds_conn.exceptions.DBInstanceAlreadyExistsFault as ex:
    print("La instancia de base de datos MySQL ya existe.")
except Exception as ex:
    print("Error al crear la base de datos MySQL:", ex)

# Crear la base de datos PostgreSQL para DWH
try:
    response = aws_rds_conn.create_db_instance(
        DBInstanceIdentifier=config.get('DWH', 'DB_INSTANCE_ID'),
        DBName=config.get('DWH', 'DB_NAME'),
        DBInstanceClass='db.t2.micro',
        Engine='postgres',
        MasterUsername=config.get('DWH', 'DB_USER'),
        MasterUserPassword=config.get('DWH', 'DB_PASSWORD'),
        Port=int(config.get('DWH', 'DB_PORT')),
        PubliclyAccessible=True,
        VpcSecurityGroupIds=[config.get('VPC', 'SECURITY_GROUP')],
        AllocatedStorage=20
    )
    print(response)
except aws_rds_conn.exceptions.DBInstanceAlreadyExistsFault as ex:
    print("La instancia de base de datos PostgreSQL ya existe.")
except Exception as ex:
    print("Error al crear la base de datos PostgreSQL:", ex)

# Crear la instancia EC2
try:
    response = aws_ec2_conn.run_instances(
        ImageId=config.get('EC2', 'IMAGE_ID'),
        InstanceType='t2.micro',
        KeyName=config.get('EC2', 'KEY_PAIR'),
        MinCount=1,
        MaxCount=1,
        SecurityGroupIds=[config.get('VPC', 'SECURITY_GROUP')]
    )
    instance_id = response['Instances'][0]['InstanceId']
    print("Instancia EC2 creada con ID:", instance_id)
except Exception as ex:
    print("Error al crear la instancia EC2:", ex)

# Obtener el hostname de la base de datos MySQL
try:
    instance = aws_rds_conn.describe_db_instances(DBInstanceIdentifier=config.get('TRANSACC', 'DB_INSTANCE_ID'))
    mysql_hostname = instance.get('DBInstances')[0].get('Endpoint').get('Address')
    print("Hostname de la base de datos MySQL:", mysql_hostname)
except Exception as ex:
    print("Error al obtener el hostname de la base de datos MySQL:", ex)

# Obtener el hostname de la base de datos PostgreSQL
try:
    instance = aws_rds_conn.describe_db_instances(DBInstanceIdentifier=config.get('DWH', 'DB_INSTANCE_ID'))
    postgresql_hostname = instance.get('DBInstances')[0].get('Endpoint').get('Address')
    print("Hostname de la base de datos PostgreSQL:", postgresql_hostname)
except Exception as ex:
    print("Error al obtener el hostname de la base de datos PostgreSQL:", ex)
    
"""
# Configurar la conexión a la base de datos MySQL
mysql_conn_string = f"mysql+pymysql://{config.get('TRANSACC', 'DB_USER')}:{config.get('TRANSACC', 'DB_PASSWORD')}@{mysql_hostname}:{config.get('TRANSACC', 'DB_PORT')}/{config.get('TRANSACC', 'DB_NAME')}"
mysql_engine = create_engine(mysql_conn_string)

# Configurar la conexión a la base de datos PostgreSQL
postgresql_conn_string = f"postgresql://{config.get('DWH', 'DB_USER')}:{config.get('DWH', 'DB_PASSWORD')}@{postgresql_hostname}:{config.get('DWH', 'DB_PORT')}/{config.get('DWH', 'DB_NAME')}"
postgresql_engine = create_engine(postgresql_conn_string)

# Insertar datos en la base de datos MySQL
data = pd.DataFrame({'column1': [1, 2, 3], 'column2': ['a', 'b', 'c']})
data.to_sql('table_name', mysql_engine, if_exists='replace', index=False)

# Insertar datos en la base de datos PostgreSQL
data = pd.DataFrame({'column1': [4, 5, 6], 'column2': ['d', 'e', 'f']})
data.to_sql('table_name', postgresql_engine, if_exists='replace', index=False)
"""