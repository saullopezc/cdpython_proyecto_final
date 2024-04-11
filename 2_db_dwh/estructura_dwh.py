from sqlalchemy import create_engine, Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

db_url = 'postgresql://usuario:contraseña@localhost/dwh_db'
engine = create_engine(db_url)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

# Tabla de dimensión para Categoría (SCD Tipo 1)
class DimCategoria(Base):
    __tablename__ = 'dim_categoria'
    idcategoria = Column(Integer, primary_key=True)
    nombre = Column(String(50))
    descripcion = Column(String(255))
    estado = Column(Integer)
    fecha_inicio = Column(DateTime)
    fecha_fin = Column(DateTime)

    def __repr__(self):
        return f"<DimCategoria(idcategoria={self.idcategoria}, nombre='{self.nombre}')>"

# Tabla de dimensión para Rol (SCD Tipo 1)
class DimRol(Base):
    __tablename__ = 'dim_rol'
    idrol = Column(Integer, primary_key=True)
    nombre = Column(String(30))
    descripcion = Column(String(255))
    estado = Column(Integer)
    fecha_inicio = Column(DateTime)
    fecha_fin = Column(DateTime)

    def __repr__(self):
        return f"<DimRol(idrol={self.idrol}, nombre='{self.nombre}')>"

# Tabla de dimensión para Persona (SCD Tipo 2)
class DimPersona(Base):
    __tablename__ = 'dim_persona'
    idpersona = Column(Integer, primary_key=True)
    idpersona_origen = Column(Integer)
    tipo_persona = Column(String(20))
    nombre = Column(String(100))
    tipo_documento = Column(String(20))
    num_documento = Column(String(20))
    direccion = Column(String(70))
    telefono = Column(String(20))
    email = Column(String(50))
    fecha_inicio = Column(DateTime)
    fecha_fin = Column(DateTime)
    version = Column(Integer)

    def __repr__(self):
        return f"<DimPersona(idpersona={self.idpersona}, nombre='{self.nombre}')>"

# Tabla de dimensión para Artículo (SCD Tipo 2)
class DimArticulo(Base):
    __tablename__ = 'dim_articulo'
    idarticulo = Column(Integer, primary_key=True)
    idarticulo_origen = Column(Integer)
    codigo = Column(String(50))
    nombre = Column(String(100))
    precio_venta = Column(Numeric(11, 2))
    stock = Column(Integer)
    descripcion = Column(String(255))
    imagen = Column(String(20))
    estado = Column(Integer)
    fecha_inicio = Column(DateTime)
    fecha_fin = Column(DateTime)
    version = Column(Integer)
    idcategoria = Column(Integer, ForeignKey('dim_categoria.idcategoria'))
    categoria = relationship("DimCategoria")

    def __repr__(self):
        return f"<DimArticulo(idarticulo={self.idarticulo}, nombre='{self.nombre}')>"

# Tabla de dimensión para Usuario (SCD Tipo 2)
class DimUsuario(Base):
    __tablename__ = 'dim_usuario'
    idusuario = Column(Integer, primary_key=True)
    idusuario_origen = Column(Integer)
    nombre = Column(String(100))
    tipo_documento = Column(String(20))
    num_documento = Column(String(20))
    direccion = Column(String(70))
    telefono = Column(String(20))
    email = Column(String(50))
    clave = Column(String(255))
    estado = Column(Integer)
    fecha_inicio = Column(DateTime)
    fecha_fin = Column(DateTime)
    version = Column(Integer)
    idrol = Column(Integer, ForeignKey('dim_rol.idrol'))
    rol = relationship("DimRol")

    def __repr__(self):
        return f"<DimUsuario(idusuario={self.idusuario}, nombre='{self.nombre}')>"

# Tabla de dimensión para Tiempo
class DimTiempo(Base):
    __tablename__ = 'dim_tiempo'
    idtiempo = Column(Integer, primary_key=True)
    fecha = Column(DateTime)
    anio = Column(Integer)
    trimestre = Column(Integer)
    mes = Column(Integer)
    dia = Column(Integer)
    dia_semana = Column(Integer)
    dia_anio = Column(Integer)
    semana_anio = Column(Integer)

    def __repr__(self):
        return f"<DimTiempo(idtiempo={self.idtiempo}, fecha='{self.fecha}')>"

# Tabla de hechos para Ventas
class FactVenta(Base):
    __tablename__ = 'fact_venta'
    idventa = Column(Integer, primary_key=True)
    idcliente = Column(Integer, ForeignKey('dim_persona.idpersona'))
    idusuario = Column(Integer, ForeignKey('dim_usuario.idusuario'))
    idtiempo = Column(Integer, ForeignKey('dim_tiempo.idtiempo'))
    tipo_comprobante = Column(String(20))
    serie_comprobante = Column(String(7))
    num_comprobante = Column(String(10))
    fecha = Column(DateTime)
    impuesto = Column(Numeric(4, 2))
    total = Column(Numeric(11, 2))
    estado = Column(String(20))
    cliente = relationship("DimPersona")
    usuario = relationship("DimUsuario")
    tiempo = relationship("DimTiempo")

    def __repr__(self):
        return f"<FactVenta(idventa={self.idventa}, fecha='{self.fecha}', total={self.total})>"

# Tabla de hechos para Detalles de Venta
class FactDetalleVenta(Base):
    __tablename__ = 'fact_detalle_venta'
    iddetalle_venta = Column(Integer, primary_key=True)
    idventa = Column(Integer, ForeignKey('fact_venta.idventa'))
    idarticulo = Column(Integer, ForeignKey('dim_articulo.idarticulo'))
    cantidad = Column(Integer)
    precio = Column(Numeric(11, 2))
    descuento = Column(Numeric(11, 2))
    venta = relationship("FactVenta")
    articulo = relationship("DimArticulo")

    def __repr__(self):
        return f"<FactDetalleVenta(iddetalle_venta={self.iddetalle_venta}, cantidad={self.cantidad}, precio={self.precio})>"

Base.metadata.create_all(engine)