CREATE TABLE IF NOT EXISTS categoria(
    idcategoria INT PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE,
    descripcion VARCHAR(255),
    estado BIT
);

CREATE TABLE IF NOT EXISTS rol(
    idrol INT PRIMARY KEY,
    nombre VARCHAR(30) UNIQUE,
    descripcion VARCHAR(255),
    estado BIT
);

CREATE TABLE IF NOT EXISTS persona(
    idpersona INT PRIMARY KEY,
    tipo_persona VARCHAR(20) UNIQUE,
    nombre VARCHAR(100),
    tipo_documento VARCHAR(20),
    num_documento VARCHAR(20),
    direccion VARCHAR(70),
    telefono VARCHAR(20),
    email VARCHAR(50),
);

CREATE TABLE IF NOT EXISTS articulo(
    idarticulo INT PRIMARY KEY,
    codigo VARCHAR(50),
    nombre VARCHAR(100),
    precio_venta DECIMAL(11,2),
    stock INT,
    descripcion VARCHAR(255),
    imagen VARCHAR(20),
    estado BIT,
    idcategoria INT,

    CONSTRAINT fk_idcategoria
        FOREIGN KEY (idcategoria)
            REFERENCES categoria(idcategoria)

);

CREATE TABLE IF NOT EXISTS usuario(
    idusuario INT PRIMARY KEY,
    nombre VARCHAR(100),
    tipo_documento VARCHAR(20),
    num_documento VARCHAR(20),
    direccion VARCHAR(70),
    telefono VARCHAR(20),
    email VARCHAR(50),
    clave VARBINARY(MAX),
    estado BIT,
    idrol INT,

    CONSTRAINT fk_idrol
        FOREIGN KEY (idrol)
            REFERENCES rol(idrol)

);

CREATE TABLE IF NOT EXISTS ingreso(
    idingreso INT PRIMARY KEY,
    nombre VARCHAR(100),
    tipo_comprobante VARCHAR(20),
    serie_comprobante VARCHAR(7),
    num_comprobante VARCHAR(10),
    fecha DATETIME,
    impuesto DECIMAL(4,2),
    total DECIMAL(11,2),
    estado VARCHAR(20),
    idpersona INT,
    idusuario INT,

    CONSTRAINT fk_idpersona
        FOREIGN KEY (idpersona)
            REFERENCES persona(idpersona),

    CONSTRAINT fk_idusuario
        FOREIGN KEY (idusuario)
            REFERENCES usuario(idusuario)

);

CREATE TABLE IF NOT EXISTS detalle_ingreso(
    iddetalle_ingreso INT PRIMARY KEY,
    cantidad INT,
    precio DECIMAL(11,2),
    idingreso INT,
    idarticulo INT,

    CONSTRAINT fk_idingreso
        FOREIGN KEY (idingreso)
            REFERENCES ingreso(idingreso),

    CONSTRAINT fk_idarticulo
        FOREIGN KEY (idarticulo)
            REFERENCES articulo(idarticulo)

);

CREATE TABLE IF NOT EXISTS venta(
    idventa INT PRIMARY KEY,
    tipo_comprobante VARCHAR(20),
    serie_comprobante VARCHAR(7),
    num_comprobante VARCHAR(10),
    fecha DATETIME,
    impuesto DECIMAL(4,2),
    total DECIMAL(11,2),
    estado VARCHAR(20),
    idcliente INT,
    idusuario INT,

    CONSTRAINT fk_idcliente
        FOREIGN KEY (idcliente)
            REFERENCES cliente(idcliente),

    CONSTRAINT fk_idusuario
        FOREIGN KEY (idusuario)
            REFERENCES usuario(idusuario)

);


CREATE TABLE IF NOT EXISTS detalle_venta(
    iddetalle_venta INT PRIMARY KEY,
    cantidad INT,
    precio DECIMAL(11,2),
    descuento DECIMAL(11,2),
    idventa INT,
    idarticulo INT,

    CONSTRAINT fk_idventa
        FOREIGN KEY (idventa)
            REFERENCES venta(idventa),

    CONSTRAINT fk_idarticulo
        FOREIGN KEY (idarticulo)
            REFERENCES articulo(idarticulo)

);