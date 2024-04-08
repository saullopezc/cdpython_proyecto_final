import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# Conexión a la base de datos del DWH
engine = create_engine('postgresql://user:password@hostname/dwh_db')

# Consultas SQL para obtener los datos de las tablas relevantes
df_dim_empresa = pd.read_sql('SELECT * FROM dim_empresa', engine)
df_dim_producto = pd.read_sql('SELECT * FROM dim_producto', engine)
df_dim_medicamento = pd.read_sql('SELECT * FROM dim_medicamento', engine)
df_fact_importacion = pd.read_sql('SELECT * FROM fact_importacion', engine)
df_fact_exportacion = pd.read_sql('SELECT * FROM fact_exportacion', engine)

# Pregunta 1: ¿Cuál es el total de importaciones y exportaciones por empresa en un periodo de tiempo específico?
df_importaciones_exportaciones = pd.merge(df_fact_importacion, df_dim_empresa, on='id_empresa')
df_importaciones_exportaciones = pd.merge(df_importaciones_exportaciones, df_fact_exportacion, on='id_empresa')
df_importaciones_exportaciones = df_importaciones_exportaciones.groupby('nombre')['valor_total_x', 'valor_total_y'].sum().reset_index()
df_importaciones_exportaciones.columns = ['empresa', 'total_importaciones', 'total_exportaciones']

plt.figure(figsize=(10, 6))
sns.barplot(x='empresa', y='total_importaciones', data=df_importaciones_exportaciones, label='Importaciones')
sns.barplot(x='empresa', y='total_exportaciones', data=df_importaciones_exportaciones, label='Exportaciones')
plt.title('Total de importaciones y exportaciones por empresa')
plt.xlabel('Empresa')
plt.ylabel('Valor total')
plt.legend()
plt.show()

# Pregunta 2: ¿Cuáles son los productos y medicamentos más importados y exportados?
df_productos_importados = pd.merge(df_fact_importacion, df_dim_producto, left_on='id_producto', right_on='id_producto')
df_productos_exportados = pd.merge(df_fact_exportacion, df_dim_producto, left_on='id_producto', right_on='id_producto')
df_productos_importados_exportados = pd.concat([df_productos_importados, df_productos_exportados])
df_productos_importados_exportados = df_productos_importados_exportados.groupby('nombre').size().reset_index(name='cantidad')

plt.figure(figsize=(10, 6))
sns.barplot(x='nombre', y='cantidad', data=df_productos_importados_exportados)
plt.title('Productos y medicamentos más importados y exportados')
plt.xlabel('Producto')
plt.ylabel('Cantidad')
plt.xticks(rotation=45)
plt.show()

# Pregunta 3: ¿Cuál es el valor total de las importaciones y exportaciones por país de origen y destino?
df_pais_importacion = pd.read_sql('SELECT * FROM dim_pais', engine)
df_pais_exportacion = pd.read_sql('SELECT * FROM dim_pais', engine)
df_importaciones_pais = pd.merge(df_fact_importacion, df_pais_importacion, left_on='id_pais_origen', right_on='id_pais')
df_exportaciones_pais = pd.merge(df_fact_exportacion, df_pais_exportacion, left_on='id_pais_destino', right_on='id_pais')
df_importaciones_pais = df_importaciones_pais.groupby('nombre')['valor_total'].sum().reset_index()
df_exportaciones_pais = df_exportaciones_pais.groupby('nombre')['valor_total'].sum().reset_index()

plt.figure(figsize=(10, 6))
sns.barplot(x='nombre', y='valor_total', data=df_importaciones_pais, label='Importaciones')
sns.barplot(x='nombre', y='valor_total', data=df_exportaciones_pais, label='Exportaciones')
plt.title('Valor total de importaciones y exportaciones por país')
plt.xlabel('País')
plt.ylabel('Valor total')
plt.xticks(rotation=45)
plt.legend()
plt.show()

# Pregunta 4: ¿Cuáles son las enfermedades y plagas más tratadas con los medicamentos importados y exportados?
df_enfermedad = pd.read_sql('SELECT * FROM dim_enfermedad', engine)
df_plaga = pd.read_sql('SELECT * FROM dim_plaga', engine)
df_medicamento_enfermedad = pd.read_sql('SELECT * FROM medicamento_enfermedad', engine)
df_medicamento_plaga = pd.read_sql('SELECT * FROM medicamento_plaga', engine)
df_enfermedades_tratadas = pd.merge(df_medicamento_enfermedad, df_enfermedad, on='id_enfermedad')
df_plagas_tratadas = pd.merge(df_medicamento_plaga, df_plaga, on='id_plaga')
df_enfermedades_tratadas = df_enfermedades_tratadas.groupby('nombre')['id_medicamento'].count().reset_index()
df_plagas_tratadas = df_plagas_tratadas.groupby('nombre')['id_medicamento'].count().reset_index()

plt.figure(figsize=(10, 6))
sns.barplot(x='nombre', y='id_medicamento', data=df_enfermedades_tratadas, label='Enfermedades')
sns.barplot(x='nombre', y='id_medicamento', data=df_plagas_tratadas, label='Plagas')
plt.title('Enfermedades y plagas más tratadas con medicamentos importados y exportados')
plt.xlabel('Enfermedad/Plaga')
plt.ylabel('Cantidad de medicamentos')
plt.xticks(rotation=45)
plt.legend()
plt.show()

# Pregunta 5: ¿Cuál es el porcentaje de productos y medicamentos certificados por cada empresa?
df_certificacion_producto = pd.read_sql('SELECT * FROM certificacion_producto', engine)
df_certificacion_medicamento = pd.read_sql('SELECT * FROM certificacion_importacion_medicamento', engine)
df_productos_certificados = pd.merge(df_certificacion_producto, df_dim_producto, on='id_producto')
df_medicamentos_certificados = pd.merge(df_certificacion_medicamento, df_dim_medicamento, on='id_medicamento')
df_productos_certificados = df_productos_certificados.groupby('id_empresa').agg({'id_producto': 'nunique'}).reset_index()
df_medicamentos_certificados = df_medicamentos_certificados.groupby('id_empresa').agg({'id_medicamento': 'nunique'}).reset_index()
df_productos_certificados = pd.merge(df_productos_certificados, df_dim_empresa, on='id_empresa')
df_medicamentos_certificados = pd.merge(df_medicamentos_certificados, df_dim_empresa, on='id_empresa')
df_productos_certificados['porcentaje_certificados'] = df_productos_certificados['id_producto'] / df_productos_certificados['id_producto'].sum() * 100
df_medicamentos_certificados['porcentaje_certificados'] = df_medicamentos_certificados['id_medicamento'] / df_medicamentos_certificados['id_medicamento'].sum() * 100

plt.figure(figsize=(10, 6))
sns.barplot(x='nombre', y='porcentaje_certificados', data=df_productos_certificados, label='Productos')
sns.barplot(x='nombre', y='porcentaje_certificados', data=df_medicamentos_certificados, label='Medicamentos')
plt.title('Porcentaje de productos y medicamentos certificados por empresa')
plt.xlabel('Empresa')
plt.ylabel('Porcentaje')
plt.xticks(rotation=45)
plt.legend()
plt.show()

# Pregunta 6: ¿Cuáles son los laboratorios con mayor participación en las importaciones y exportaciones?
df_laboratorio = pd.read_sql('SELECT * FROM dim_laboratorio', engine)
df_importaciones_laboratorio = pd.merge(df_fact_importacion, df_dim_producto, on='id_producto')
df_importaciones_laboratorio = pd.merge(df_importaciones_laboratorio, df_laboratorio, on='id_laboratorio')
df_exportaciones_laboratorio = pd.merge(df_fact_exportacion, df_dim_producto, on='id_producto')
df_exportaciones_laboratorio = pd.merge(df_exportaciones_laboratorio, df_laboratorio, on='id_laboratorio')
df_importaciones_laboratorio = df_importaciones_laboratorio.groupby('nombre')['valor_total'].sum().reset_index()
df_exportaciones_laboratorio = df_exportaciones_laboratorio.groupby('nombre')['valor_total'].sum().reset_index()

plt.figure(figsize=(10, 6))
sns.barplot(x='nombre', y='valor_total', data=df_importaciones_laboratorio, label='Importaciones')
sns.barplot(x='nombre', y='valor_total', data=df_exportaciones_laboratorio, label='Exportaciones')
plt.title('Laboratorios con mayor participación en importaciones y exportaciones')
plt.xlabel('Laboratorio')
plt.ylabel('Valor total')
plt.xticks(rotation=45)
plt.legend()
plt.show()

# Pregunta 7: ¿Cuál es la evolución mensual del valor total de las importaciones y exportaciones?
df_importaciones_mensuales = df_fact_importacion.groupby(pd.Grouper(key='fecha_llegada', freq='M'))['valor_total'].sum().reset_index()
df_importaciones_mensuales.columns = ['mes', 'valor_total_importaciones']
df_exportaciones_mensuales = df_fact_exportacion.groupby(pd.Grouper(key='fecha_llegada', freq='M'))['valor_total'].sum().reset_index()
df_exportaciones_mensuales.columns = ['mes', 'valor_total_exportaciones']
df_evolucion_mensual = pd.merge(df_importaciones_mensuales, df_exportaciones_mensuales, on='mes')

plt.figure(figsize=(10, 6))
sns.lineplot(x='mes', y='valor_total_importaciones', data=df_evolucion_mensual, label='Importaciones')
sns.lineplot(x='mes', y='valor_total_exportaciones', data=df_evolucion_mensual, label='Exportaciones')
plt.title('Evolución mensual del valor total de las importaciones y exportaciones')
plt.xlabel('Mes')
plt.ylabel('Valor total')
plt.legend()
plt.show()

# Pregunta 8: ¿Cuáles son los regentes con mayor número de certificaciones emitidas?
df_regente = pd.read_sql('SELECT * FROM dim_regente', engine)
df_certificacion_regente = pd.read_sql('SELECT * FROM certificacion_regente', engine)
df_certificaciones_regente = pd.merge(df_certificacion_regente, df_regente, on='id_regente')
df_certificaciones_regente = df_certificaciones_regente.groupby(['id_regente', 'nombre', 'apellido']).size().reset_index(name='cantidad_certificaciones')
df_certificaciones_regente = df_certificaciones_regente.sort_values('cantidad_certificaciones', ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(x='nombre', y='cantidad_certificaciones', data=df_certificaciones_regente)
plt.title('Regentes con mayor número de certificaciones emitidas')
plt.xlabel('Regente')
plt.ylabel('Cantidad de certificaciones')
plt.xticks(rotation=45)
plt.show()

# Pregunta 9: ¿Cuál es la relación entre el valor total de las importaciones y exportaciones y el número de productos y medicamentos involucrados?
df_importaciones_total = df_fact_importacion.groupby('id_importacion').agg({'valor_total': 'sum', 'id_producto': 'nunique'}).reset_index()
df_exportaciones_total = df_fact_exportacion.groupby('id_exportacion').agg({'valor_total': 'sum', 'id_producto': 'nunique'}).reset_index()

plt.figure(figsize=(10, 6))
sns.scatterplot(x='id_producto', y='valor_total', data=df_importaciones_total, label='Importaciones')
sns.scatterplot(x='id_producto', y='valor_total', data=df_exportaciones_total, label='Exportaciones')
plt.title('Relación entre valor total y número de productos/medicamentos')
plt.xlabel('Número de productos/medicamentos')
plt.ylabel('Valor total')
plt.legend()
plt.show()

# Pregunta 10: ¿Cuáles son las empresas con mayor crecimiento en términos de valor total de importaciones y exportaciones en un periodo de tiempo específico?
df_importaciones_empresa = df_fact_importacion.groupby(['id_empresa', pd.Grouper(key='fecha_llegada', freq='Y')])['valor_total'].sum().reset_index()
df_exportaciones_empresa = df_fact_exportacion.groupby(['id_empresa', pd.Grouper(key='fecha_llegada', freq='Y')])['valor_total'].sum().reset_index()
df_importaciones_empresa = pd.merge(df_importaciones_empresa, df_dim_empresa, on='id_empresa')
df_exportaciones_empresa = pd.merge(df_exportaciones_empresa, df_dim_empresa, on='id_empresa')
df_importaciones_empresa['crecimiento_importaciones'] = df_importaciones_empresa.groupby('id_empresa')['valor_total'].pct_change()
df_exportaciones_empresa['crecimiento_exportaciones'] = df_exportaciones_empresa.groupby('id_empresa')['valor_total'].pct_change()

plt.figure(figsize=(10, 6))
sns.lineplot(x='fecha_llegada', y='crecimiento_importaciones', hue='nombre', data=df_importaciones_empresa)
plt.title('Crecimiento de las importaciones por empresa')
plt.xlabel('Año')
plt.ylabel('Crecimiento')
plt.xticks(rotation=45)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()

plt.figure(figsize=(10, 6))
sns.lineplot(x='fecha_llegada', y='crecimiento_exportaciones', hue='nombre', data=df_exportaciones_empresa)
plt.title('Crecimiento de las exportaciones por empresa')
plt.xlabel('Año')
plt.ylabel('Crecimiento')
plt.xticks(rotation=45)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()

