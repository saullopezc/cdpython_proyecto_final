from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Tablas de dimensiones con SCD Tipo 2
class DimLaboratorio(Base):
    __tablename__ = 'dim_laboratorio'
    id_laboratorio = Column(Integer, primary_key=True)
    nombre = Column(String)
    direccion = Column(String)
    telefono = Column(String)
    correo = Column(String)
    fecha_inicio = Column(Date)
    fecha_fin = Column(Date)
    es_actual = Column(Boolean)

class DimPersona(Base):
    __tablename__ = 'dim_persona'
    id_persona = Column(Integer, primary_key=True)
    nombre = Column(String)
    apellido = Column(String)
    identificacion = Column(String)
    tipo_identificacion = Column(String)
    correo = Column(String)
    telefono = Column(String)
    fecha_inicio = Column(Date)
    fecha_fin = Column(Date)
    es_actual = Column(Boolean)

# Tablas de dimensiones con SCD Tipo 1
class DimConcentracion(Base):
    __tablename__ = 'dim_concentracion'
    id_concentracion = Column(Integer, primary_key=True)
    descripcion = Column(String)
    cantidad = Column(Float)
    unidad_medida = Column(String)

# Tablas de hechos
class FactImportacion(Base):
    __tablename__ = 'fact_importacion'
    id_importacion = Column(Integer, primary_key=True)
    id_empresa = Column(Integer, ForeignKey('dim_empresa.id_empresa'))
    fecha_salida = Column(Date)
    fecha_llegada = Column(Date)
    valor_flete = Column(Float)
    valor_total = Column(Float)

class FactExportacion(Base):
    __tablename__ = 'fact_exportacion'
    id_exportacion = Column(Integer, primary_key=True)
    id_empresa = Column(Integer, ForeignKey('dim_empresa.id_empresa'))
    fecha_salida = Column(Date)
    fecha_llegada = Column(Date)
    valor_flete = Column(Float)
    valor_total = Column(Float)

# Crear las tablas en la base de datos del DWH
engine = create_engine('postgresql://user:password@hostname/dwh_database')
Base.metadata.create_all(engine)