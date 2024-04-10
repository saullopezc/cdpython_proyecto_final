
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# 1. ¿Cuál es el total de ventas por categoría de artículo en un período específico?
# Extraer información de las tablas de hechos y dimensión
df_venta = pd.read_sql('SELECT * FROM fact_venta', dwh_engine)
df_detalle_venta = pd.read_sql('SELECT * FROM fact_detalle_venta', dwh_engine)
df_articulo = pd.read_sql('SELECT * FROM dim_articulo', dwh_engine)

# Realizar el join entre las tablas
df_ventas = pd.merge(df_venta, df_detalle_venta, on='idventa')
df_ventas = pd.merge(df_ventas, df_articulo, on='idarticulo')

# Filtrar por un período específico (por ejemplo, año 2023)
df_ventas_filtrado = df_ventas[df_ventas['fecha'].dt.year == 2023]

# Agrupar por categoría y sumar el total de ventas
ventas_por_categoria = df_ventas_filtrado.groupby('idcategoria')['precio'].sum().reset_index()

# Graficar los resultados
sns.barplot(x='idcategoria', y='precio', data=ventas_por_categoria)
plt.xlabel('Categoría')
plt.ylabel('Total de Ventas')
plt.title('Total de Ventas por Categoría (2023)')
plt.show()


# 2. ¿Quiénes son los clientes que generan el mayor volumen de ventas y cuál es su contribución al total de ingresos?
# Extraer información de las tablas de hechos y dimensión
df_venta = pd.read_sql('SELECT * FROM fact_venta', dwh_engine)
df_persona = pd.read_sql('SELECT * FROM dim_persona', dwh_engine)

# Realizar el join entre las tablas
df_ventas = pd.merge(df_venta, df_persona, left_on='idcliente', right_on='idpersona')

# Agrupar por cliente y sumar el total de ventas
ventas_por_cliente = df_ventas.groupby(['idpersona', 'nombre'])['total'].sum().reset_index()

# Calcular el total de ingresos
total_ingresos = ventas_por_cliente['total'].sum()

# Calcular la contribución de cada cliente al total de ingresos
ventas_por_cliente['contribucion'] = ventas_por_cliente['total'] / total_ingresos * 100

# Ordenar por total de ventas descendente
ventas_por_cliente = ventas_por_cliente.sort_values('total', ascending=False)

# Graficar los resultados
plt.figure(figsize=(10, 6))
sns.barplot(x='nombre', y='total', data=ventas_por_cliente.head(10))
plt.xlabel('Cliente')
plt.ylabel('Total de Ventas')
plt.title('Clientes con Mayor Volumen de Ventas')
plt.xticks(rotation=45)
plt.show()

# 3. ¿Cuál es el rendimiento de ventas de cada vendedor y cómo se compara con el promedio de ventas por vendedor?
# Extraer información de las tablas de hechos y dimensión
df_venta = pd.read_sql('SELECT * FROM fact_venta', dwh_engine)
df_usuario = pd.read_sql('SELECT * FROM dim_usuario', dwh_engine)

# Realizar el join entre las tablas
df_ventas = pd.merge(df_venta, df_usuario, left_on='idusuario', right_on='idusuario')

# Agrupar por vendedor y sumar el total de ventas
ventas_por_vendedor = df_ventas.groupby(['idusuario', 'nombre'])['total'].sum().reset_index()

# Calcular el promedio de ventas por vendedor
promedio_ventas = ventas_por_vendedor['total'].mean()

# Graficar los resultados
plt.figure(figsize=(10, 6))
sns.barplot(x='nombre', y='total', data=ventas_por_vendedor)
plt.axhline(promedio_ventas, color='red', linestyle='--', label='Promedio de Ventas')
plt.xlabel('Vendedor')
plt.ylabel('Total de Ventas')
plt.title('Rendimiento de Ventas por Vendedor')
plt.xticks(rotation=45)
plt.legend()
plt.show()


# 4. ¿Cuáles son los artículos más vendidos y menos vendidos en términos de cantidad y monto total de ventas?

# Extraer información de las tablas de hechos y dimensión
df_detalle_venta = pd.read_sql('SELECT * FROM fact_detalle_venta', dwh_engine)
df_articulo = pd.read_sql('SELECT * FROM dim_articulo', dwh_engine)

# Realizar el join entre las tablas
df_ventas = pd.merge(df_detalle_venta, df_articulo, on='idarticulo')

# Agrupar por artículo y sumar la cantidad y el monto total de ventas
ventas_por_articulo = df_ventas.groupby(['idarticulo', 'nombre']).agg({'cantidad': 'sum', 'precio': 'sum'}).reset_index()
ventas_por_articulo = ventas_por_articulo.rename(columns={'precio': 'monto_total'})

# Ordenar por cantidad de ventas descendente
articulos_mas_vendidos = ventas_por_articulo.sort_values('cantidad', ascending=False).head(10)

# Ordenar por cantidad de ventas ascendente
articulos_menos_vendidos = ventas_por_articulo.sort_values('cantidad').head(10)

# Graficar los resultados
plt.figure(figsize=(10, 6))
plt.subplot(1, 2, 1)
sns.barplot(x='nombre', y='cantidad', data=articulos_mas_vendidos)
plt.xlabel('Artículo')
plt.ylabel('Cantidad Vendida')
plt.title('Artículos Más Vendidos')
plt.xticks(rotation=45)

plt.subplot(1, 2, 2)
sns.barplot(x='nombre', y='cantidad', data=articulos_menos_vendidos)
plt.xlabel('Artículo')
plt.ylabel('Cantidad Vendida')
plt.title('Artículos Menos Vendidos')
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()



# 5. ¿Cómo ha evolucionado el volumen de ventas a lo largo del tiempo (por mes, trimestre, año)?
# Extraer información de las tablas de hechos y dimensión
df_venta = pd.read_sql('SELECT * FROM fact_venta', dwh_engine)
df_tiempo = pd.read_sql('SELECT * FROM dim_tiempo', dwh_engine)

# Realizar el join entre las tablas
df_ventas = pd.merge(df_venta, df_tiempo, on='idtiempo')

# Agrupar por mes y sumar el total de ventas
ventas_por_mes = df_ventas.groupby(df_ventas['fecha'].dt.to_period('M'))['total'].sum().reset_index()
ventas_por_mes = ventas_por_mes.rename(columns={'fecha': 'mes', 'total': 'ventas'})

# Agrupar por trimestre y sumar el total de ventas
ventas_por_trimestre = df_ventas.groupby(df_ventas['fecha'].dt.to_period('Q'))['total'].sum().reset_index()
ventas_por_trimestre = ventas_por_trimestre.rename(columns={'fecha': 'trimestre', 'total': 'ventas'})

# Agrupar por año y sumar el total de ventas
ventas_por_anio = df_ventas.groupby(df_ventas['fecha'].dt.to_period('Y'))['total'].sum().reset_index()
ventas_por_anio = ventas_por_anio.rename(columns={'fecha': 'año', 'total': 'ventas'})

# Graficar los resultados
plt.figure(figsize=(12, 4))

plt.subplot(1, 3, 1)
sns.lineplot(x='mes', y='ventas', data=ventas_por_mes)
plt.xlabel('Mes')
plt.ylabel('Total de Ventas')
plt.title('Ventas por Mes')
plt.xticks(rotation=45)

plt.subplot(1, 3, 2)
sns.lineplot(x='trimestre', y='ventas', data=ventas_por_trimestre)
plt.xlabel('Trimestre')
plt.ylabel('Total de Ventas')
plt.title('Ventas por Trimestre')
plt.xticks(rotation=45)

plt.subplot(1, 3, 3)
sns.lineplot(x='año', y='ventas', data=ventas_por_anio)
plt.xlabel('Año')
plt.ylabel('Total de Ventas')
plt.title('Ventas por Año')
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()





