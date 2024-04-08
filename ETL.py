import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime

# Conexión a la base de datos transaccional
transactional_engine = create_engine('mysql+mysqlconnector://user:password@hostname/transactional_db')

# Conexión a la base de datos del DWH
dwh_engine = create_engine('postgresql://user:password@hostname/dwh_db')

# Extraer datos de la tabla Laboratorio
df_laboratorio = pd.read_sql_table('Laboratorio', transactional_engine)

# Aplicar SCD Tipo 2 a la tabla DimLaboratorio
df_dim_laboratorio = pd.read_sql_table('dim_laboratorio', dwh_engine)
df_laboratorio = pd.merge(df_laboratorio, df_dim_laboratorio[['id_laboratorio', 'fecha_fin']], on='id_laboratorio', how='left')
df_laboratorio['fecha_inicio'] = datetime.now().date()
df_laboratorio['fecha_fin'] = pd.to_datetime('9999-12-31')
df_laboratorio['es_actual'] = True

df_dim_laboratorio.loc[df_dim_laboratorio['es_actual'], 'fecha_fin'] = datetime.now().date()
df_dim_laboratorio.loc[df_dim_laboratorio['es_actual'], 'es_actual'] = False

df_dim_laboratorio = pd.concat([df_dim_laboratorio, df_laboratorio])

# Cargar los datos en la tabla DimLaboratorio del DWH
df_dim_laboratorio.to_sql('dim_laboratorio', dwh_engine, if_exists='replace', index=False)

# Extraer datos de la tabla Concentracion
df_concentracion = pd.read_sql_table('Concentracion', transactional_engine)

# Aplicar SCD Tipo 1 a la tabla DimConcentracion
df_dim_concentracion = pd.read_sql_table('dim_concentracion', dwh_engine)
df_concentracion = df_concentracion[~df_concentracion['id_concentracion'].isin(df_dim_concentracion['id_concentracion'])]

# Cargar los datos en la tabla DimConcentracion del DWH
df_concentracion.to_sql('dim_concentracion', dwh_engine, if_exists='append', index=False)

# Extraer datos de la tabla Importacion y sus tablas relacionadas
df_importacion = pd.read_sql_table('Importacion', transactional_engine)
df_importacion_producto = pd.read_sql_table('ImportacionProducto', transactional_engine)
df_importacion_medicamento = pd.read_sql_table('ImportacionMedicamento', transactional_engine)

# Transformar los datos
df_importacion_producto = df_importacion_producto.groupby('id_importacion').agg({'cantidad': 'sum'}).reset_index()
df_importacion_producto.rename(columns={'cantidad': 'cantidad_producto'}, inplace=True)

df_importacion_medicamento = df_importacion_medicamento.groupby('id_importacion').agg({'cantidad': 'sum'}).reset_index()
df_importacion_medicamento.rename(columns={'cantidad': 'cantidad_medicamento'}, inplace=True)

df_fact_importacion = pd.merge(df_importacion, df_importacion_producto, on='id_importacion', how='left')
df_fact_importacion = pd.merge(df_fact_importacion, df_importacion_medicamento, on='id_importacion', how='left')

# Cargar los datos en la tabla FactImportacion del DWH
df_fact_importacion.to_sql('fact_importacion', dwh_engine, if_exists='append', index=False)