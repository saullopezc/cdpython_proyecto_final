import pandas as pd
from sqlalchemy import create_engine

# Configuración de la conexión a la base de datos transaccional (MySQL)
transactional_db_url = 'mysql+pymysql://usuario:contraseña@localhost/transactional_db'
transactional_engine = create_engine(transactional_db_url)

# Configuración de la conexión a la base de datos del DWH (PostgreSQL)
dwh_db_url = 'postgresql://usuario:contraseña@localhost/dwh_db'
dwh_engine = create_engine(dwh_db_url)

# Extracción, transformación y carga de la dimensión Categoría
def etl_dim_categoria():
    # Extracción
    df_categoria = pd.read_sql('SELECT * FROM categoria', transactional_engine)
    
    # Transformación
    df_categoria_dim = df_categoria.rename(columns={'idcategoria': 'idcategoria', 'nombre': 'nombre', 'descripcion': 'descripcion', 'estado': 'estado'})
    df_categoria_dim['fecha_inicio'] = pd.to_datetime('today')
    df_categoria_dim['fecha_fin'] = pd.to_datetime('2999-12-31')
    
    # Carga
    df_categoria_dim.to_sql('dim_categoria', dwh_engine, if_exists='append', index=False)

# Extracción, transformación y carga de la dimensión Rol
def etl_dim_rol():
    # Extracción
    df_rol = pd.read_sql('SELECT * FROM rol', transactional_engine)
    
    # Transformación
    df_rol_dim = df_rol.rename(columns={'idrol': 'idrol', 'nombre': 'nombre', 'descripcion': 'descripcion', 'estado': 'estado'})
    df_rol_dim['fecha_inicio'] = pd.to_datetime('today')
    df_rol_dim['fecha_fin'] = pd.to_datetime('2999-12-31')
    
    # Carga
    df_rol_dim.to_sql('dim_rol', dwh_engine, if_exists='append', index=False)

# Extracción, transformación y carga de la dimensión Persona
def etl_dim_persona():
    # Extracción
    df_persona = pd.read_sql('SELECT * FROM persona', transactional_engine)
    
    # Transformación
    df_persona_dim = df_persona.rename(columns={'idpersona': 'idpersona_origen', 'tipo_persona': 'tipo_persona', 'nombre': 'nombre', 'tipo_documento': 'tipo_documento', 'num_documento': 'num_documento', 'direccion': 'direccion', 'telefono': 'telefono', 'email': 'email'})
    df_persona_dim['idpersona'] = range(1, len(df_persona_dim) + 1)
    df_persona_dim['fecha_inicio'] = pd.to_datetime('today')
    df_persona_dim['fecha_fin'] = pd.to_datetime('2999-12-31')
    df_persona_dim['version'] = 1
    
    # Carga
    df_persona_dim.to_sql('dim_persona', dwh_engine, if_exists='append', index=False)

# Extracción, transformación y carga de la dimensión Artículo
def etl_dim_articulo():
    # Extracción
    df_articulo = pd.read_sql('SELECT * FROM articulo', transactional_engine)
    df_categoria = pd.read_sql('SELECT * FROM categoria', transactional_engine)
    
    # Transformación
    df_articulo_dim = pd.merge(df_articulo, df_categoria, left_on='idcategoria', right_on='idcategoria', how='left')
    df_articulo_dim = df_articulo_dim.rename(columns={'idarticulo': 'idarticulo_origen', 'codigo': 'codigo', 'nombre_x': 'nombre', 'precio_venta': 'precio_venta', 'stock': 'stock', 'descripcion_x': 'descripcion', 'imagen': 'imagen', 'estado_x': 'estado', 'idcategoria': 'idcategoria'})
    df_articulo_dim['idarticulo'] = range(1, len(df_articulo_dim) + 1)
    df_articulo_dim['fecha_inicio'] = pd.to_datetime('today')
    df_articulo_dim['fecha_fin'] = pd.to_datetime('2999-12-31')
    df_articulo_dim['version'] = 1
    df_articulo_dim = df_articulo_dim.drop(['nombre_y', 'descripcion_y', 'estado_y'], axis=1)
    
    # Carga
    df_articulo_dim.to_sql('dim_articulo', dwh_engine, if_exists='append', index=False)

# Extracción, transformación y carga de la dimensión Usuario
def etl_dim_usuario():
    # Extracción
    df_usuario = pd.read_sql('SELECT * FROM usuario', transactional_engine)
    df_rol = pd.read_sql('SELECT * FROM rol', transactional_engine)
    
    # Transformación
    df_usuario_dim = pd.merge(df_usuario, df_rol, left_on='idrol', right_on='idrol', how='left')
    df_usuario_dim = df_usuario_dim.rename(columns={'idusuario': 'idusuario_origen', 'nombre_x': 'nombre', 'tipo_documento': 'tipo_documento', 'num_documento': 'num_documento', 'direccion': 'direccion', 'telefono': 'telefono', 'email': 'email', 'clave': 'clave', 'estado_x': 'estado', 'idrol': 'idrol'})
    df_usuario_dim['idusuario'] = range(1, len(df_usuario_dim) + 1)
    df_usuario_dim['fecha_inicio'] = pd.to_datetime('today')
    df_usuario_dim['fecha_fin'] = pd.to_datetime('2999-12-31')
    df_usuario_dim['version'] = 1
    df_usuario_dim = df_usuario_dim.drop(['nombre_y', 'descripcion', 'estado_y'], axis=1)
    
    # Carga
    df_usuario_dim.to_sql('dim_usuario', dwh_engine, if_exists='append', index=False)

# Extracción, transformación y carga de la dimensión Tiempo
def etl_dim_tiempo():
    # Extracción
    df_venta = pd.read_sql('SELECT fecha FROM venta', transactional_engine)
    
    # Transformación
    df_tiempo_dim = pd.DataFrame()
    df_tiempo_dim['fecha'] = pd.to_datetime(df_venta['fecha'].unique())
    df_tiempo_dim['anio'] = df_tiempo_dim['fecha'].dt.year
    df_tiempo_dim['trimestre'] = df_tiempo_dim['fecha'].dt.quarter
    df_tiempo_dim['mes'] = df_tiempo_dim['fecha'].dt.month
    df_tiempo_dim['dia'] = df_tiempo_dim['fecha'].dt.day
    df_tiempo_dim['dia_semana'] = df_tiempo_dim['fecha'].dt.dayofweek
    df_tiempo_dim['dia_anio'] = df_tiempo_dim['fecha'].dt.dayofyear
    df_tiempo_dim['semana_anio'] = df_tiempo_dim['fecha'].dt.isocalendar().week
    df_tiempo_dim['idtiempo'] = range(1, len(df_tiempo_dim) + 1)
    
    # Carga
    df_tiempo_dim.to_sql('dim_tiempo', dwh_engine, if_exists='append', index=False)

# Extracción, transformación y carga de la tabla de hechos Venta
def etl_fact_venta():
    # Extracción
    df_venta = pd.read_sql('SELECT * FROM venta', transactional_engine)
    df_persona = pd.read_sql('SELECT * FROM persona', transactional_engine)
    df_usuario = pd.read_sql('SELECT * FROM usuario', transactional_engine)
    df_tiempo = pd.read_sql('SELECT * FROM dim_tiempo', dwh_engine)
    
    # Transformación
    df_venta_fact = pd.merge(df_venta, df_persona, left_on='idcliente', right_on='idpersona', how='left')
    df_venta_fact = pd.merge(df_venta_fact, df_usuario, left_on='idusuario', right_on='idusuario', how='left')
    df_venta_fact = pd.merge(df_venta_fact, df_tiempo, left_on='fecha', right_on='fecha', how='left')
    df_venta_fact = df_venta_fact.rename(columns={'idventa': 'idventa', 'tipo_comprobante': 'tipo_comprobante', 'serie_comprobante': 'serie_comprobante', 'num_comprobante': 'num_comprobante', 'fecha': 'fecha', 'impuesto': 'impuesto', 'total': 'total', 'estado': 'estado', 'idpersona': 'idcliente', 'idusuario': 'idusuario', 'idtiempo': 'idtiempo'})
    df_venta_fact = df_venta_fact.drop(['tipo_persona', 'nombre_x', 'tipo_documento_x', 'num_documento_x', 'direccion_x', 'telefono_x', 'email_x', 'nombre_y', 'tipo_documento_y', 'num_documento_y', 'direccion_y', 'telefono_y', 'email_y', 'clave', 'estado_y', 'idrol', 'anio', 'trimestre', 'mes', 'dia', 'dia_semana', 'dia_anio', 'semana_anio'], axis=1)
    
    # Carga
    df_venta_fact.to_sql('fact_venta', dwh_engine, if_exists='append', index=False)

# Extracción, transformación y carga de la tabla de hechos Detalle de Venta
def etl_fact_detalle_venta():
    # Extracción
    df_detalle_venta = pd.read_sql('SELECT * FROM detalle_venta', transactional_engine)
    df_venta = pd.read_sql('SELECT * FROM venta', transactional_engine)
    df_articulo = pd.read_sql('SELECT * FROM articulo', transactional_engine)
    
    # Transformación
    df_detalle_venta_fact = pd.merge(df_detalle_venta, df_venta, left_on='idventa', right_on='idventa', how='left')
    df_detalle_venta_fact = pd.merge(df_detalle_venta_fact, df_articulo, left_on='idarticulo', right_on='idarticulo', how='left')
    df_detalle_venta_fact = df_detalle_venta_fact.rename(columns={'iddetalle_venta': 'iddetalle_venta', 'idventa': 'idventa', 'idarticulo': 'idarticulo', 'cantidad': 'cantidad', 'precio': 'precio', 'descuento': 'descuento'})
    df_detalle_venta_fact = df_detalle_venta_fact.drop(['tipo_comprobante', 'serie_comprobante', 'num_comprobante', 'fecha', 'impuesto', 'total', 'estado', 'idcliente', 'idusuario', 'codigo', 'nombre', 'precio_venta', 'stock', 'descripcion', 'imagen', 'estado', 'idcategoria'], axis=1)
    
    # Carga
    df_detalle_venta_fact.to_sql('fact_detalle_venta', dwh_engine, if_exists='append', index=False)

# Ejecución de las funciones de ETL
etl_dim_categoria()
etl_dim_rol()
etl_dim_persona()
etl_dim_articulo()
etl_dim_usuario()
etl_dim_tiempo()
etl_fact_venta()
etl_fact_detalle_venta()