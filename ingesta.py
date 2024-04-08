from faker import Faker
from sqlalchemy import create_engine
import random

# Conexión a la base de datos transaccional
engine = create_engine('mysql+mysqlconnector://user:password@hostname/transactional_db')
#database por definir

# Instanciar Faker
fake = Faker('es_ES')

# Generar datos para la tabla Laboratorio (catálogo)
laboratorios = []
for _ in range(20):
    laboratorio = {
        'id_laboratorio': fake.unique.random_int(min=1, max=9999),
        'nombre': fake.company(),
        'direccion': fake.address(),
        'telefono': fake.phone_number(),
        'correo': fake.email()
    }
    laboratorios.append(laboratorio)

# Generar datos para la tabla Persona (al menos 1000 registros)
personas = []
for _ in range(1000):
    persona = {
        'id_persona': fake.unique.random_int(min=1, max=999999),
        'nombre': fake.first_name(),
        'apellido': fake.last_name(),
        'identificacion': fake.unique.random_int(min=1000000, max=9999999),
        'tipo_identificacion': random.choice(['DNI', 'NIE', 'Pasaporte']),
        'correo': fake.email(),
        'telefono': fake.phone_number()
    }
    personas.append(persona)

# Generar datos para la tabla DocumentoPersona (al menos 1000 registros)
documentos_persona = []
for persona in personas:
    num_documentos = random.randint(1, 5)
    for _ in range(num_documentos):
        documento_persona = {
            'id_documento_persona': fake.unique.random_int(min=1, max=999999),
            'id_persona': persona['id_persona'],
            'tipo_documento': random.choice(['DNI', 'Pasaporte', 'Certificado de Nacimiento']),
            'ruta_documento': fake.file_path(depth=3, extension='pdf')
        }
        documentos_persona.append(documento_persona)

# Generar datos para la tabla Empresa (al menos 1000 registros)
empresas = []
for _ in range(1000):
    empresa = {
        'id_empresa': fake.unique.random_int(min=1, max=999999),
        'nombre': fake.company(),
        'identificacion': fake.unique.random_int(min=1000000, max=9999999),
        'tipo_identificacion': random.choice(['CIF', 'NIF']),
        'direccion': fake.address(),
        'telefono': fake.phone_number(),
        'correo': fake.email(),
        'registro': fake.random_int(min=1000, max=9999),
        'libro': fake.random_int(min=1, max=999),
        'folio': fake.random_int(min=1, max=999),
        'id_representante_legal': random.choice(personas)['id_persona']
    }
    empresas.append(empresa)

# Generar datos para la tabla DocumentoEmpresa (al menos 1000 registros)
documentos_empresa = []
for empresa in empresas:
    num_documentos = random.randint(1, 5)
    for _ in range(num_documentos):
        documento_empresa = {
            'id_documento_empresa': fake.unique.random_int(min=1, max=999999),
            'id_empresa': empresa['id_empresa'],
            'tipo_documento': random.choice(['Escritura', 'Acta', 'Certificado']),
            'ruta_documento': fake.file_path(depth=3, extension='pdf')
        }
        documentos_empresa.append(documento_empresa)

# Generar datos para la tabla PersonaEmpresa (al menos 1000 registros)
personas_empresa = []
for _ in range(1000):
    persona_empresa = {
        'id_persona': random.choice(personas)['id_persona'],
        'id_empresa': random.choice(empresas)['id_empresa']
    }
    personas_empresa.append(persona_empresa)

# Generar datos para la tabla Producto (al menos 1000 registros)
productos = []
for _ in range(1000):
    producto = {
        'id_producto': fake.unique.random_int(min=1, max=999999),
        'nombre': fake.word(),
        'descripcion': fake.sentence(),
        'tipo_consumo': random.choice(['Humano', 'Animal']),
        'id_laboratorio': random.choice(laboratorios)['id_laboratorio']
    }
    productos.append(producto)

# Generar datos para la tabla Medicamento (al menos 1000 registros)
medicamentos = []
for _ in range(1000):
    medicamento = {
        'id_medicamento': fake.unique.random_int(min=1, max=999999),
        'nombre': fake.word(),
        'descripcion': fake.sentence(),
        'concentracion_maxima': fake.pyfloat(min_value=0, max_value=100),
        'id_laboratorio': random.choice(laboratorios)['id_laboratorio']
    }
    medicamentos.append(medicamento)

# Generar datos para la tabla Concentracion (catálogo)
concentraciones = []
for _ in range(20):
    concentracion = {
        'id_concentracion': fake.unique.random_int(min=1, max=9999),
        'descripcion': fake.sentence(),
        'cantidad': fake.pyfloat(min_value=0, max_value=100),
        'unidad_medida': random.choice(['mg', 'ml', 'g'])
    }
    concentraciones.append(concentracion)

# Generar datos para la tabla ProductoConcentracion (al menos 1000 registros)
productos_concentracion = []
for _ in range(1000):
    producto_concentracion = {
        'id_producto': random.choice(productos)['id_producto'],
        'id_concentracion': random.choice(concentraciones)['id_concentracion']
    }
    productos_concentracion.append(producto_concentracion)

# Generar datos para la tabla MedicamentoConcentracion (al menos 1000 registros)
medicamentos_concentracion = []
for _ in range(1000):
    medicamento_concentracion = {
        'id_medicamento': random.choice(medicamentos)['id_medicamento'],
        'id_concentracion': random.choice(concentraciones)['id_concentracion']
    }
    medicamentos_concentracion.append(medicamento_concentracion)

# Generar datos para la tabla Enfermedad (catálogo)
enfermedades = []
for _ in range(20):
    enfermedad = {
        'id_enfermedad': fake.unique.random_int(min=1, max=9999),
        'nombre': fake.word(),
        'descripcion': fake.sentence()
    }
    enfermedades.append(enfermedad)

# Generar datos para la tabla MedicamentoEnfermedad (al menos 1000 registros)
medicamentos_enfermedad = []
for _ in range(1000):
    medicamento_enfermedad = {
        'id_medicamento': random.choice(medicamentos)['id_medicamento'],
        'id_enfermedad': random.choice(enfermedades)['id_enfermedad']
    }
    medicamentos_enfermedad.append(medicamento_enfermedad)

# Generar datos para la tabla Plaga (catálogo)
plagas = []
for _ in range(20):
    plaga = {
        'id_plaga': fake.unique.random_int(min=1, max=9999),
        'nombre': fake.word(),
        'descripcion': fake.sentence()
    }
    plagas.append(plaga)

# Generar datos para la tabla MedicamentoPlaga (al menos 1000 registros)
medicamentos_plaga = []
for _ in range(1000):
    medicamento_plaga = {
        'id_medicamento': random.choice(medicamentos)['id_medicamento'],
        'id_plaga': random.choice(plagas)['id_plaga']
    }
    medicamentos_plaga.append(medicamento_plaga)

# Generar datos para la tabla Regente (al menos 1000 registros)
regentes = []
for _ in range(1000):
    regente = {
        'id_regente': fake.unique.random_int(min=1, max=999999),
        'id_persona': random.choice(personas)['id_persona'],
        'numero_colegiatura': fake.unique.random_int(min=1000, max=9999),
        'especialidad': fake.job()
    }
    regentes.append(regente)

# Generar datos para la tabla CertificacionProducto (al menos 1000 registros)
certificaciones_producto = []
for _ in range(1000):
    certificacion_producto = {
        'id_certificacion': fake.unique.random_int(min=1, max=999999),
        'id_regente': random.choice(regentes)['id_regente'],
        'id_producto': random.choice(productos)['id_producto'],
        'id_empresa': random.choice(empresas)['id_empresa'],
        'fecha_inicio': fake.date_between(start_date='-1y', end_date='today'),
        'fecha_vencimiento': fake.date_between(start_date='today', end_date='+1y'),
        'observaciones': fake.sentence()
    }
    certificaciones_producto.append(certificacion_producto)

# Generar datos para la tabla CertificacionImportacionMedicamento (al menos 1000 registros)
certificaciones_importacion_medicamento = []
for _ in range(1000):
    certificacion_importacion_medicamento = {
        'id_certificacion_importacion': fake.unique.random_int(min=1, max=999999),
        'id_regente': random.choice(regentes)['id_regente'],
        'id_medicamento': random.choice(medicamentos)['id_medicamento'],
        'id_empresa': random.choice(empresas)['id_empresa'],
        'fecha_inicio': fake.date_between(start_date='-1y', end_date='today'),
        'fecha_vencimiento': fake.date_between(start_date='today', end_date='+1y'),
        'observaciones': fake.sentence()
    }
    certificaciones_importacion_medicamento.append(
        certificacion_importacion_medicamento)

# Generar datos para la tabla CertificacionRegente (al menos 1000 registros)
certificaciones_regente = []
for _ in range(1000):
    certificacion_regente = {
        'id_certificacion_regente': fake.unique.random_int(min=1, max=999999),
        'id_regente': random.choice(regentes)['id_regente'],
        'id_empresa': random.choice(empresas)['id_empresa'],
        'fecha_inicio': fake.date_between(start_date='-1y', end_date='today'),
        'fecha_vencimiento': fake.date_between(start_date='today', end_date='+1y'),
        'observaciones': fake.sentence()
    }
    certificaciones_regente.append(certificacion_regente)

# Generar datos para la tabla Importacion (al menos 1000 registros)
importaciones = []
for _ in range(1000):
    importacion = {
        'id_importacion': fake.unique.random_int(min=1, max=999999),
        'id_empresa': random.choice(empresas)['id_empresa'],
        'fecha_salida': fake.date_between(start_date='-1y', end_date='today'),
        'fecha_llegada': fake.date_between(start_date='today', end_date='+1y'),
        'valor_flete': fake.pydecimal(min_value=1000, max_value=10000, right_digits=2),
        'valor_total': fake.pydecimal(min_value=10000, max_value=100000, right_digits=2)
    }
    importaciones.append(importacion)

# Generar datos para la tabla DocumentoImportacion (al menos 1000 registros)
documentos_importacion = []
for importacion in importaciones:
    num_documentos = random.randint(1, 5)
    for _ in range(num_documentos):
        documento_importacion = {
            'id_documento_importacion': fake.unique.random_int(min=1, max=999999),
            'id_importacion': importacion['id_importacion'],
            'tipo_documento': random.choice(['Factura', 'Guía', 'Certificado']),
            'ruta_documento': fake.file_path(depth=3, extension='pdf')
        }
        documentos_importacion.append(documento_importacion)

# Generar datos para la tabla ImportacionProducto (al menos 1000 registros)
importaciones_producto = []
for _ in range(1000):
    importacion_producto = {
        'id_importacion': random.choice(importaciones)['id_importacion'],
        'id_producto': random.choice(productos)['id_producto'],
        'cantidad': fake.random_int(min=1, max=100)
    }
    importaciones_producto.append(importacion_producto)

# Generar datos para la tabla ImportacionMedicamento (al menos 1000 registros)
importaciones_medicamento = []
for _ in range(1000):
    importacion_medicamento = {
        'id_importacion': random.choice(importaciones)['id_importacion'],
        'id_medicamento': random.choice(medicamentos)['id_medicamento'],
        'cantidad': fake.random_int(min=1, max=100)
    }
    importaciones_medicamento.append(importacion_medicamento)

# Generar datos para la tabla Exportacion (al menos 1000 registros)
exportaciones = []
for _ in range(1000):
    exportacion = {
        'id_exportacion': fake.unique.random_int(min=1, max=999999),
        'id_empresa': random.choice(empresas)['id_empresa'],
        'fecha_salida': fake.date_between(start_date='-1y', end_date='today'),
        'fecha_llegada': fake.date_between(start_date='today', end_date='+1y'),
        'valor_flete': fake.pydecimal(min_value=1000, max_value=10000, right_digits=2),
        'valor_total': fake.pydecimal(min_value=10000, max_value=100000, right_digits=2)
    }
    exportaciones.append(exportacion)

# Generar datos para la tabla DocumentoExportacion (al menos 1000 registros)
documentos_exportacion = []
for exportacion in exportaciones:
    num_documentos = random.randint(1, 5)
    for _ in range(num_documentos):
        documento_exportacion = {
            'id_documento_exportacion': fake.unique.random_int(min=1, max=999999),
            'id_exportacion': exportacion['id_exportacion'],
            'tipo_documento': random.choice(['Factura', 'Guía', 'Certificado']),
            'ruta_documento': fake.file_path(depth=3, extension='pdf')
        }
        documentos_exportacion.append(documento_exportacion)

# Generar datos para la tabla ExportacionProducto (al menos 1000 registros)
exportaciones_producto = []
for _ in range(1000):
    exportacion_producto = {
        'id_exportacion': random.choice(exportaciones)['id_exportacion'],
        'id_producto': random.choice(productos)['id_producto'],
        'cantidad': fake.random_int(min=1, max=100)
    }
    exportaciones_producto.append(exportacion_producto)

# Generar datos para la tabla ExportacionMedicamento(al menos 1000 registros)
exportaciones_medicamento = []
for _ in range(1000):
    exportacion_medicamento = {
        'id_exportacion': random.choice(exportaciones)['id_exportacion'],
        'id_medicamento': random.choice(medicamentos)['id_medicamento'],
        'cantidad': fake.random_int(min=1, max=100)
    }
    exportaciones_medicamento.append(exportacion_medicamento)

# Insertar los datos generados en las tablas correspondientes
with engine.begin() as connection:
    connection.execute(
        'INSERT INTO Laboratorio (id_laboratorio, nombre, direccion, telefono, correo) VALUES (:id_laboratorio, :nombre, :direccion, :telefono, :correo)', laboratorios)
    connection.execute('INSERT INTO Persona (id_persona, nombre, apellido, identificacion, tipo_identificacion, correo, telefono) VALUES (:id_persona, :nombre, :apellido, :identificacion, :tipo_identificacion, :correo, :telefono)', personas)
    connection.execute('INSERT INTO DocumentoPersona (id_documento_persona, id_persona, tipo_documento, ruta_documento) VALUES (:id_documento_persona, :id_persona, :tipo_documento, :ruta_documento)', documentos_persona)
    connection.execute('INSERT INTO Empresa (id_empresa, nombre, identificacion, tipo_identificacion, direccion, telefono, correo, registro, libro, folio, id_representante_legal) VALUES (:id_empresa, :nombre, :identificacion, :tipo_identificacion, :direccion, :telefono, :correo, :registro, :libro, :folio, :id_representante_legal)', empresas)
    connection.execute('INSERT INTO DocumentoEmpresa (id_documento_empresa, id_empresa, tipo_documento, ruta_documento) VALUES (:id_documento_empresa, :id_empresa, :tipo_documento, :ruta_documento)', documentos_empresa)
    connection.execute(
        'INSERT INTO PersonaEmpresa (id_persona, id_empresa) VALUES (:id_persona, :id_empresa)', personas_empresa)
    connection.execute(
        'INSERT INTO Producto (id_producto, nombre, descripcion, tipo_consumo, id_laboratorio) VALUES (:id_producto, :nombre, :descripcion, :tipo_consumo, :id_laboratorio)', productos)
    connection.execute('INSERT INTO Medicamento (id_medicamento, nombre, descripcion, concentracion_maxima, id_laboratorio) VALUES (:id_medicamento, :nombre, :descripcion, :concentracion_maxima, :id_laboratorio)', medicamentos)
    connection.execute(
        'INSERT INTO Concentracion (id_concentracion, descripcion, cantidad, unidad_medida) VALUES (:id_concentracion, :descripcion, :cantidad, :unidad_medida)', concentraciones)
    connection.execute(
        'INSERT INTO ProductoConcentracion (id_producto, id_concentracion) VALUES (:id_producto, :id_concentracion)', productos_concentracion)
    connection.execute(
        'INSERT INTO MedicamentoConcentracion (id_medicamento, id_concentracion) VALUES (:id_medicamento, :id_concentracion)', medicamentos_concentracion)
    connection.execute(
        'INSERT INTO Enfermedad (id_enfermedad, nombre, descripcion) VALUES (:id_enfermedad, :nombre, :descripcion)', enfermedades)
    connection.execute(
        'INSERT INTO MedicamentoEnfermedad (id_medicamento, id_enfermedad) VALUES (:id_medicamento, :id_enfermedad)', medicamentos_enfermedad)
    connection.execute(
        'INSERT INTO Plaga (id_plaga, nombre, descripcion) VALUES (:id_plaga, :nombre, :descripcion)', plagas)
    connection.execute(
        'INSERT INTO MedicamentoPlaga (id_medicamento, id_plaga) VALUES (:id_medicamento, :id_plaga)', medicamentos_plaga)
    connection.execute(
        'INSERT INTO Regente (id_regente, id_persona, numero_colegiatura, especialidad) VALUES (:id_regente, :id_persona, :numero_colegiatura, :especialidad)', regentes)
    connection.execute('INSERT INTO CertificacionProducto (id_certificacion, id_regente, id_producto, id_empresa, fecha_inicio, fecha_vencimiento, observaciones) VALUES (:id_certificacion, :id_regente, :id_producto, :id_empresa, :fecha_inicio, :fecha_vencimiento, :observaciones)', certificaciones_producto)
    connection.execute('INSERT INTO CertificacionImportacionMedicamento (id_certificacion_importacion, id_regente, id_medicamento, id_empresa, fecha_inicio, fecha_vencimiento, observaciones) VALUES (:id_certificacion_importacion, :id_regente, :id_medicamento, :id_empresa, :fecha_inicio, :fecha_vencimiento, :observaciones)', certificaciones_importacion_medicamento)
    connection.execute('INSERT INTO CertificacionRegente (id_certificacion_regente, id_regente, id_empresa, fecha_inicio, fecha_vencimiento, observaciones) VALUES (:id_certificacion_regente, :id_regente, :id_empresa, :fecha_inicio, :fecha_vencimiento, :observaciones)', certificaciones_regente)
    connection.execute('INSERT INTO Importacion (id_importacion, id_empresa, fecha_salida, fecha_llegada, valor_flete, valor_total) VALUES (:id_importacion, :id_empresa, :fecha_salida, :fecha_llegada, :valor_flete, :valor_total)', importaciones)
    connection.execute('INSERT INTO DocumentoImportacion (id_documento_importacion, id_importacion, tipo_documento, ruta_documento) VALUES (:id_documento_importacion, :id_importacion, :tipo_documento, :ruta_documento)', documentos_importacion)
    connection.execute(
        'INSERT INTO ImportacionProducto (id_importacion, id_producto, cantidad) VALUES (:id_importacion, :id_producto, :cantidad)', importaciones_producto)
    connection.execute(
        'INSERT INTO ImportacionMedicamento (id_importacion, id_medicamento, cantidad) VALUES (:id_importacion, :id_medicamento, :cantidad)', importaciones_medicamento)
    connection.execute('INSERT INTO Exportacion (id_exportacion, id_empresa, fecha_salida, fecha_llegada, valor_flete, valor_total) VALUES (:id_exportacion, :id_empresa, :fecha_salida, :fecha_llegada, :valor_flete, :valor_total)', exportaciones)
    connection.execute('INSERT INTO DocumentoExportacion (id_documento_exportacion, id_exportacion, tipo_documento, ruta_documento) VALUES (:id_documento_exportacion, :id_exportacion, :tipo_documento, :ruta_documento)', documentos_exportacion)
    connection.execute(
        'INSERT INTO ExportacionProducto (id_exportacion, id_producto, cantidad) VALUES (:id_exportacion, :id_producto, :cantidad)', exportaciones_producto)
    connection.execute(
        'INSERT INTO ExportacionMedicamento (id_exportacion, id_medicamento, cantidad) VALUES (:id_exportacion, :id_medicamento, :cantidad)', exportaciones_medicamento)

print("Datos generados e insertados correctamente en la base de datos.")
