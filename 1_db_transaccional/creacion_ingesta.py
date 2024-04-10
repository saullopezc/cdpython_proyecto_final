from sqlalchemy import create_engine, Column, Integer, String, DECIMAL, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from faker import Faker
import random

db_url = 'mysql+pymysql://root:password@localhost/transactional_db'
engine = create_engine(db_url)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

fake = Faker()

class Categoria(Base):
    __tablename__ = 'categoria'
    idcategoria = Column(Integer, primary_key=True)
    nombre = Column(String(50), unique=True)
    descripcion = Column(String(255))
    estado = Column(Integer)

class Rol(Base):
    __tablename__ = 'rol'
    idrol = Column(Integer, primary_key=True)
    nombre = Column(String(30), unique=True)
    descripcion = Column(String(255))
    estado = Column(Integer)

class Persona(Base):
    __tablename__ = 'persona'
    idpersona = Column(Integer, primary_key=True)
    tipo_persona = Column(String(20), unique=True)
    nombre = Column(String(100))
    tipo_documento = Column(String(20))
    num_documento = Column(String(20))
    direccion = Column(String(70))
    telefono = Column(String(20))
    email = Column(String(50))

class Articulo(Base):
    __tablename__ = 'articulo'
    idarticulo = Column(Integer, primary_key=True)
    codigo = Column(String(50))
    nombre = Column(String(100))
    precio_venta = Column(DECIMAL(11, 2))
    stock = Column(Integer)
    descripcion = Column(String(255))
    imagen = Column(String(20))
    estado = Column(Integer)
    idcategoria = Column(Integer, ForeignKey('categoria.idcategoria'))
    categoria = relationship("Categoria")

class Usuario(Base):
    __tablename__ = 'usuario'
    idusuario = Column(Integer, primary_key=True)
    nombre = Column(String(100))
    tipo_documento = Column(String(20))
    num_documento = Column(String(20))
    direccion = Column(String(70))
    telefono = Column(String(20))
    email = Column(String(50))
    clave = Column(String(255))
    estado = Column(Integer)
    idrol = Column(Integer, ForeignKey('rol.idrol'))
    rol = relationship("Rol")

class Ingreso(Base):
    __tablename__ = 'ingreso'
    idingreso = Column(Integer, primary_key=True)
    nombre = Column(String(100))
    tipo_comprobante = Column(String(20))
    serie_comprobante = Column(String(7))
    num_comprobante = Column(String(10))
    fecha = Column(DateTime)
    impuesto = Column(DECIMAL(4, 2))
    total = Column(DECIMAL(11, 2))
    estado = Column(String(20))
    idpersona = Column(Integer, ForeignKey('persona.idpersona'))
    idusuario = Column(Integer, ForeignKey('usuario.idusuario'))
    persona = relationship("Persona")
    usuario = relationship("Usuario")

class DetalleIngreso(Base):
    __tablename__ = 'detalle_ingreso'
    iddetalle_ingreso = Column(Integer, primary_key=True)
    cantidad = Column(Integer)
    precio = Column(DECIMAL(11, 2))
    idingreso = Column(Integer, ForeignKey('ingreso.idingreso'))
    idarticulo = Column(Integer, ForeignKey('articulo.idarticulo'))
    ingreso = relationship("Ingreso")
    articulo = relationship("Articulo")

class Venta(Base):
    __tablename__ = 'venta'
    idventa = Column(Integer, primary_key=True)
    tipo_comprobante = Column(String(20))
    serie_comprobante = Column(String(7))
    num_comprobante = Column(String(10))
    fecha = Column(DateTime)
    impuesto = Column(DECIMAL(4, 2))
    total = Column(DECIMAL(11, 2))
    estado = Column(String(20))
    idcliente = Column(Integer, ForeignKey('persona.idpersona'))
    idusuario = Column(Integer, ForeignKey('usuario.idusuario'))
    cliente = relationship("Persona")
    usuario = relationship("Usuario")

class DetalleVenta(Base):
    __tablename__ = 'detalle_venta'
    iddetalle_venta = Column(Integer, primary_key=True)
    cantidad = Column(Integer)
    precio = Column(DECIMAL(11, 2))
    descuento = Column(DECIMAL(11, 2))
    idventa = Column(Integer, ForeignKey('venta.idventa'))
    idarticulo = Column(Integer, ForeignKey('articulo.idarticulo'))
    venta = relationship("Venta")
    articulo = relationship("Articulo")

Base.metadata.create_all(engine)

categorias = []
for _ in range(20):
    categoria = Categoria(
        nombre=fake.unique.word(),
        descripcion=fake.sentence(),
        estado=random.choice([0, 1])
    )
    categorias.append(categoria)
session.add_all(categorias)

roles = []
for _ in range(20):
    rol = Rol(
        nombre=fake.unique.job(),
        descripcion=fake.sentence(),
        estado=random.choice([0, 1])
    )
    roles.append(rol)
session.add_all(roles)

personas = []
for _ in range(1000):
    persona = Persona(
        tipo_persona=fake.random_element(elements=('Cliente', 'Proveedor')),
        nombre=fake.name(),
        tipo_documento=fake.random_element(elements=('DNI', 'RUC')),
        num_documento=fake.unique.random_number(digits=8),
        direccion=fake.address(),
        telefono=fake.phone_number(),
        email=fake.email()
    )
    personas.append(persona)
session.add_all(personas)

articulos = []
for _ in range(1000):
    articulo = Articulo(
        codigo=fake.unique.ean13(),
        nombre=fake.product_name(),
        precio_venta=round(random.uniform(10, 1000), 2),
        stock=random.randint(1, 1000),
        descripcion=fake.sentence(),
        imagen=fake.file_name(extension='jpg'),
        estado=random.choice([0, 1]),
        idcategoria=random.choice(categorias).idcategoria
    )
    articulos.append(articulo)
session.add_all(articulos)

usuarios = []
for _ in range(1000):
    usuario = Usuario(
        nombre=fake.name(),
        tipo_documento=fake.random_element(elements=('DNI', 'RUC')),
        num_documento=fake.unique.random_number(digits=8),
        direccion=fake.address(),
        telefono=fake.phone_number(),
        email=fake.email(),
        clave=fake.password(),
        estado=random.choice([0, 1]),
        idrol=random.choice(roles).idrol
    )
    usuarios.append(usuario)
session.add_all(usuarios)

ingresos = []
for _ in range(1000):
    ingreso = Ingreso(
        nombre=fake.sentence(),
        tipo_comprobante=fake.random_element(elements=('Factura', 'Boleta')),
        serie_comprobante=fake.unique.random_number(digits=7),
        num_comprobante=fake.unique.random_number(digits=10),
        fecha=fake.date_time_between(start_date='-2y', end_date='now'),
        impuesto=round(random.uniform(0, 100), 2),
        total=round(random.uniform(100, 10000), 2),
        estado=fake.random_element(elements=('Aceptado', 'Anulado')),
        idpersona=random.choice(personas).idpersona,
        idusuario=random.choice(usuarios).idusuario
    )
    ingresos.append(ingreso)
session.add_all(ingresos)

detalles_ingreso = []
for ingreso in ingresos:
    for _ in range(random.randint(1, 5)):
        detalle_ingreso = DetalleIngreso(
            cantidad=random.randint(1, 10),
            precio=round(random.uniform(10, 1000), 2),
            idingreso=ingreso.idingreso,
            idarticulo=random.choice(articulos).idarticulo
        )
        detalles_ingreso.append(detalle_ingreso)
session.add_all(detalles_ingreso)

ventas = []
for _ in range(1000):
    venta = Venta(
        tipo_comprobante=fake.random_element(elements=('Factura', 'Boleta')),
        serie_comprobante=fake.unique.random_number(digits=7),
        num_comprobante=fake.unique.random_number(digits=10),
        fecha=fake.date_time_between(start_date='-2y', end_date='now'),
        impuesto=round(random.uniform(0, 100), 2),
        total=round(random.uniform(100, 10000), 2),
        estado=fake.random_element(elements=('Aceptado', 'Anulado')),
        idcliente=random.choice([persona for persona in personas if persona.tipo_persona == 'Cliente']).idpersona,
        idusuario=random.choice(usuarios).idusuario
    )
    ventas.append(venta)
session.add_all(ventas)

detalles_venta = []
for venta in ventas:
    for _ in range(random.randint(1, 5)):
        detalle_venta = DetalleVenta(
            cantidad=random.randint(1, 10),
            precio=round(random.uniform(10, 1000), 2),
            descuento=round(random.uniform(0, 100), 2),
            idventa=venta.idventa,
            idarticulo=random.choice(articulos).idarticulo
        )
        detalles_venta.append(detalle_venta)
session.add_all(detalles_venta)

session.commit()
session.close()