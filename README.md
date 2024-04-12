# Proyecto Final: Postgrado en Análisis y Predicción de Datos

## Ciencia de Datos en Python

**Instructor:** Ing. Preng Biba Solares

**Estudiantes:**
- Saul Alexander López Contreras | Carné: 24000138
- Josias Emanuel Chocooj Azmitia | Carné: 24000705
- Erick Manuel Andrade Zuñiga | Carné: 24000165

**Sección:** U

**Ciudad de Guatemala, 12 de abril 2024**

## Índice

1. [Introducción](#introducción)
2. [Objetivos](#objetivos)
   - [Objetivo General](#objetivo-general)
   - [Objetivos Específicos](#objetivos-específicos)
3. [Contenido](#contenido)
   - [Infraestructura de AWS](#infraestructura-de-aws)
   - [Base de Datos Transaccional](#base-de-datos-transaccional)
   - [Data Warehouse](#data-warehouse)
   - [Proceso ETL](#proceso-etl)
   - [Visualización y Análisis](#visualización-y-análisis)
   - [Código y Tecnología Utilizadas](#código-y-tecnología-utilizadas)
   - [Cumplimiento de Requerimientos](#cumplimiento-de-requerimientos)
   - [Preguntas de Negocio](#preguntas-de-negocio)
4. [Conclusiones](#conclusiones)

## Introducción

Como proyecto final del curso Ciencia de Datos en Python, se desarrolla el presente sistema de ingeniería de datos. Este consta de crear una infraestructura de base de datos transaccional, cargar datos de prueba y emplear una estructura de Datawarehouse para realizar análisis de datos del mismo y responder preguntas de negocio. Se utiliza Python en cada uno de estos pasos como principal sistema de programación.

## Objetivos

### Objetivo General

- Desarrollar un sistema de ingeniería de datos que integre Python, SQL, y AWS para automatizar el flujo de datos desde la ingestión hasta el análisis y la visualización.

### Objetivos Específicos

- Implementar un sistema transaccional automatizado en AWS.
- Crear y poblar una base de datos utilizando Python.
- Diseñar y construir un data warehouse que responda a preguntas de negocio específicas.
- Desarrollar un proceso ETL para integrar, transformar y cargar datos.
- Realizar análisis de datos y visualización para responder a preguntas de negocio.

## Contenido

### Infraestructura de AWS

Utilizado la infraestructura de capa gratuita de AWS, utilizando RDS para el uso de MySQL y Postgres, EC2, VPC y la respectiva configuración para únicamente utilizar los puertos asignados con credenciales previamente configuradas para acceder a recursos predefinidos.

### Base de Datos Transaccional

Diseñada para gestionar las operaciones diarias y facilitar la recolección de datos en tiempo real.

### Data Warehouse

Estructurado para apoyar el análisis de datos y la toma de decisiones, almacenando datos históricos estructurados de forma que faciliten la ejecución de consultas complejas y análisis multidimensionales.

### Proceso ETL

Implementado para extraer datos del sistema transaccional, transformarlos según los requerimientos del data warehouse y cargarlos en la estructura definida del data warehouse.

### Visualización y Análisis

Realizado utilizando herramientas como Pandas, NumPy, Matplotlib, y Seaborn en Python, para responder a las preguntas de negocio planteadas.

### Código y Tecnología Utilizadas

Se apoyó en una variedad de tecnologías y lenguajes de programación para construir un sistema de ingeniería de datos completo y robusto.

### Cumplimiento de Requerimientos

Cumplió con los siguientes requisitos técnicos y funcionales, incluyendo el uso de AWS para infraestructura y la separación de sistemas transaccionales y data warehouse.

### Preguntas de Negocio

Incluyeron preguntas sobre ventas por categoría, rendimiento de vendedores, y evolución del volumen de ventas.

## Conclusiones

* El proyecto de ingeniería de datos alcanzó con éxito sus objetivos, desarrollando un pipeline eficiente utilizando Python, SQL, y AWS que mejoró significativamente la capacidad de análisis y toma de decisiones basadas en datos dentro de la organización. 
* Las soluciones adoptadas han enriquecido el conocimiento técnico del equipo y han establecido una base sólida para futuras mejoras y escalabilidad del sistema. Esto reitera la importancia de la adaptabilidad y el aprendizaje continuo en el campo de la ciencia de datos y la ingeniería de sistemas.