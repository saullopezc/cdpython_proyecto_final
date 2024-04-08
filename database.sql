-- Tabla: Laboratorio
CREATE TABLE Laboratorio (
    id_laboratorio INT PRIMARY KEY,
    nombre VARCHAR(100),
    direccion VARCHAR(200),
    telefono VARCHAR(20),
    correo VARCHAR(100)
);

-- Tabla: Persona
CREATE TABLE Persona (
    id_persona INT PRIMARY KEY,
    nombre VARCHAR(100),
    apellido VARCHAR(100),
    identificacion VARCHAR(20),
    tipo_identificacion VARCHAR(20),
    correo VARCHAR(100),
    telefono VARCHAR(20)
);

-- Tabla: DocumentoPersona
CREATE TABLE DocumentoPersona (
    id_documento_persona INT PRIMARY KEY,
    id_persona INT,
    tipo_documento VARCHAR(100),
    ruta_documento VARCHAR(200),
    FOREIGN KEY (id_persona) REFERENCES Persona(id_persona)
);

-- Tabla: Empresa
CREATE TABLE Empresa (
    id_empresa INT PRIMARY KEY,
    nombre VARCHAR(100),
    identificacion VARCHAR(20),
    tipo_identificacion VARCHAR(20),
    direccion VARCHAR(200),
    telefono VARCHAR(20),
    correo VARCHAR(100),
    registro VARCHAR(50),
    libro VARCHAR(50),
    folio VARCHAR(50),
    id_representante_legal INT,
    FOREIGN KEY (id_representante_legal) REFERENCES Persona(id_persona)
);

-- Tabla: DocumentoEmpresa
CREATE TABLE DocumentoEmpresa (
    id_documento_empresa INT PRIMARY KEY,
    id_empresa INT,
    tipo_documento VARCHAR(100),
    ruta_documento VARCHAR(200),
    FOREIGN KEY (id_empresa) REFERENCES Empresa(id_empresa)
);

-- Tabla: PersonaEmpresa (Relación muchos a muchos entre Persona y Empresa)
CREATE TABLE PersonaEmpresa (
    id_persona INT,
    id_empresa INT,
    PRIMARY KEY (id_persona, id_empresa),
    FOREIGN KEY (id_persona) REFERENCES Persona(id_persona),
    FOREIGN KEY (id_empresa) REFERENCES Empresa(id_empresa)
);

-- Tabla: Producto
CREATE TABLE Producto (
    id_producto INT PRIMARY KEY,
    nombre VARCHAR(100),
    descripcion VARCHAR(500),
    tipo_consumo VARCHAR(20), -- Valores posibles: 'Humano', 'Animal'
    id_laboratorio INT,
    FOREIGN KEY (id_laboratorio) REFERENCES Laboratorio(id_laboratorio)
);

-- Tabla: Medicamento
CREATE TABLE Medicamento (
    id_medicamento INT PRIMARY KEY,
    nombre VARCHAR(100),
    descripcion VARCHAR(500),
    concentracion_maxima DECIMAL(10, 2),
    id_laboratorio INT,
    FOREIGN KEY (id_laboratorio) REFERENCES Laboratorio(id_laboratorio)
);

-- Tabla: Concentracion
CREATE TABLE Concentracion (
    id_concentracion INT PRIMARY KEY,
    descripcion VARCHAR(100),
    cantidad DECIMAL(10, 2),
    unidad_medida VARCHAR(20)
);

-- Tabla: ProductoConcentracion (Relación muchos a muchos entre Producto y Concentracion)
CREATE TABLE ProductoConcentracion (
    id_producto INT,
    id_concentracion INT,
    PRIMARY KEY (id_producto, id_concentracion),
    FOREIGN KEY (id_producto) REFERENCES Producto(id_producto),
    FOREIGN KEY (id_concentracion) REFERENCES Concentracion(id_concentracion)
);

-- Tabla: MedicamentoConcentracion (Relación muchos a muchos entre Medicamento y Concentracion)
CREATE TABLE MedicamentoConcentracion (
    id_medicamento INT,
    id_concentracion INT,
    PRIMARY KEY (id_medicamento, id_concentracion),
    FOREIGN KEY (id_medicamento) REFERENCES Medicamento(id_medicamento),
    FOREIGN KEY (id_concentracion) REFERENCES Concentracion(id_concentracion)
);

-- Tabla: Enfermedad
CREATE TABLE Enfermedad (
    id_enfermedad INT PRIMARY KEY,
    nombre VARCHAR(100),
    descripcion VARCHAR(500)
);

-- Tabla: MedicamentoEnfermedad (Relación muchos a muchos entre Medicamento y Enfermedad)
CREATE TABLE MedicamentoEnfermedad (
    id_medicamento INT,
    id_enfermedad INT,
    PRIMARY KEY (id_medicamento, id_enfermedad),
    FOREIGN KEY (id_medicamento) REFERENCES Medicamento(id_medicamento),
    FOREIGN KEY (id_enfermedad) REFERENCES Enfermedad(id_enfermedad)
);

-- Tabla: Plaga
CREATE TABLE Plaga (
    id_plaga INT PRIMARY KEY,
    nombre VARCHAR(100),
    descripcion VARCHAR(500)
);

-- Tabla: MedicamentoPlaga (Relación muchos a muchos entre Medicamento y Plaga)
CREATE TABLE MedicamentoPlaga (
    id_medicamento INT,
    id_plaga INT,
    PRIMARY KEY (id_medicamento, id_plaga),
    FOREIGN KEY (id_medicamento) REFERENCES Medicamento(id_medicamento),
    FOREIGN KEY (id_plaga) REFERENCES Plaga(id_plaga)
);

-- Tabla: Regente
CREATE TABLE Regente (
    id_regente INT PRIMARY KEY,
    id_persona INT,
    numero_colegiatura VARCHAR(20),
    especialidad VARCHAR(100),
    FOREIGN KEY (id_persona) REFERENCES Persona(id_persona)
);

-- Tabla: CertificacionProducto
CREATE TABLE CertificacionProducto (
    id_certificacion INT PRIMARY KEY,
    id_regente INT,
    id_producto INT,
    id_empresa INT,
    fecha_inicio DATE,
    fecha_vencimiento DATE,
    observaciones VARCHAR(500),
    FOREIGN KEY (id_regente) REFERENCES Regente(id_regente),
    FOREIGN KEY (id_producto) REFERENCES Producto(id_producto),
    FOREIGN KEY (id_empresa) REFERENCES Empresa(id_empresa)
);

-- Tabla: CertificacionImportacionMedicamento
CREATE TABLE CertificacionImportacionMedicamento (
    id_certificacion_importacion INT PRIMARY KEY,
    id_regente INT,
    id_medicamento INT,
    id_empresa INT,
    fecha_inicio DATE,
    fecha_vencimiento DATE,
    observaciones VARCHAR(500),
    FOREIGN KEY (id_regente) REFERENCES Regente(id_regente),
    FOREIGN KEY (id_medicamento) REFERENCES Medicamento(id_medicamento),
    FOREIGN KEY (id_empresa) REFERENCES Empresa(id_empresa)
);

-- Tabla: CertificacionRegente
CREATE TABLE CertificacionRegente (
    id_certificacion_regente INT PRIMARY KEY,
    id_regente INT,
    id_empresa INT,
    fecha_inicio DATE,
    fecha_vencimiento DATE,
    observaciones VARCHAR(500),
    FOREIGN KEY (id_regente) REFERENCES Regente(id_regente),
    FOREIGN KEY (id_empresa) REFERENCES Empresa(id_empresa)
);

-- Tabla: Importacion
CREATE TABLE Importacion (
    id_importacion INT PRIMARY KEY,
    id_empresa INT,
    fecha_salida DATE,
    fecha_llegada DATE,
    valor_flete DECIMAL(10, 2),
    valor_total DECIMAL(10, 2),
    FOREIGN KEY (id_empresa) REFERENCES Empresa(id_empresa)
);

-- Tabla: DocumentoImportacion
CREATE TABLE DocumentoImportacion (
    id_documento_importacion INT PRIMARY KEY,
    id_importacion INT,
    tipo_documento VARCHAR(100),
    ruta_documento VARCHAR(200),
    FOREIGN KEY (id_importacion) REFERENCES Importacion(id_importacion)
);

-- Tabla: ImportacionProducto
CREATE TABLE ImportacionProducto (
    id_importacion INT,
    id_producto INT,
    cantidad INT,
    PRIMARY KEY (id_importacion, id_producto),
    FOREIGN KEY (id_importacion) REFERENCES Importacion(id_importacion),
    FOREIGN KEY (id_producto) REFERENCES Producto(id_producto)
);

-- Tabla: ImportacionMedicamento
CREATE TABLE ImportacionMedicamento (
    id_importacion INT,
    id_medicamento INT,
    cantidad INT,
    PRIMARY KEY (id_importacion, id_medicamento),
    FOREIGN KEY (id_importacion) REFERENCES Importacion(id_importacion),
    FOREIGN KEY (id_medicamento) REFERENCES Medicamento(id_medicamento)
);

-- Tabla: Exportacion
CREATE TABLE Exportacion (
    id_exportacion INT PRIMARY KEY,
    id_empresa INT,
    fecha_salida DATE,
    fecha_llegada DATE,
    valor_flete DECIMAL(10, 2),
    valor_total DECIMAL(10, 2),
    FOREIGN KEY (id_empresa) REFERENCES Empresa(id_empresa)
);

-- Tabla: DocumentoExportacion
CREATE TABLE DocumentoExportacion (
    id_documento_exportacion INT PRIMARY KEY,
    id_exportacion INT,
    tipo_documento VARCHAR(100),
    ruta_documento VARCHAR(200),
    FOREIGN KEY (id_exportacion) REFERENCES Exportacion(id_exportacion)
);

-- Tabla: ExportacionProducto
CREATE TABLE ExportacionProducto (
    id_exportacion INT,
    id_producto INT,
    cantidad INT,
    PRIMARY KEY (id_exportacion, id_producto),
    FOREIGN KEY (id_exportacion) REFERENCES Exportacion(id_exportacion),
    FOREIGN KEY (id_producto) REFERENCES Producto(id_producto)
);

-- Tabla: ExportacionMedicamento
CREATE TABLE ExportacionMedicamento (
    id_exportacion INT,
    id_medicamento INT,
    cantidad INT,
    PRIMARY KEY (id_exportacion, id_medicamento),
    FOREIGN KEY (id_exportacion) REFERENCES Exportacion(id_exportacion),
    FOREIGN KEY (id_medicamento) REFERENCES Medicamento(id_medicamento)
);