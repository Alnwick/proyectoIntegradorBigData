# Proyecto Integrador Final - Big Data y Toma de Decisiones

## Datos generales
- **Alumno:** Yael Alejandro Trujillo Godoy
- **Unidad de Aprendizaje:** Big Data y Toma de Decisiones
- **Proyecto:** Proyecto Integrador Final
- **Profesor:** Marco Fernando Andrade Cedillo
- **Fecha:** 27/04/2026

## Descripción del proyecto
Este repositorio documenta el diseño e implementación simulada de un pipeline de datos para un entorno **Smart City**. El caso de estudio integra datos telemáticos de transporte público, sensores de calidad del aire y cámaras de seguridad simuladas, con el objetivo de procesar anomalías en tiempo real y conservar históricos para análisis posterior y machine learning.

El proyecto se construyó de forma incremental, siguiendo las fases propuestas en la unidad de aprendizaje:
1. **Fase de evaluación:** identificación de las 6 V's del Big Data y análisis normativo con base en ISO/IEC 20547.
2. **Fase de arquitectura:** diseño de la solución usando el modelo C4, incluyendo contexto y contenedores.
3. **Fase de ingesta y procesamiento:** implementación simulada de streaming para abordar velocidad, variedad y controles básicos de veracidad.
4. **Fase de almacenamiento y visualización:** organización lógica del almacenamiento y generación de métricas operativas para tableros.

## Objetivo técnico
Diseñar una arquitectura de datos escalable y modular capaz de:
- ingerir datos urbanos heterogéneos;
- procesar eventos en tiempo casi real;
- detectar anomalías básicas;
- almacenar datos operativos e históricos;
- transformar los datos en información útil para operadores y analistas urbanos.

## Arquitectura propuesta
La solución está basada en una arquitectura lógica de Big Data con los siguientes bloques:
- **Fuentes de datos:** transporte público, sensores ambientales y cámaras simuladas.
- **Ingesta:** API/Gateway para recepción y validación mínima.
- **Streaming:** Kafka como bus de eventos.
- **Procesamiento:** Spark Streaming para transformación y detección de anomalías.
- **Almacenamiento operativo:** base NoSQL para consulta rápida.
- **Almacenamiento histórico:** Data Lake para datos crudos, procesados e históricos.
- **Consumo analítico:** dashboards para alertas, KPIs y análisis urbano.

## Estructura sugerida del repositorio
```text
.
├── README.md
├── docs/
│   ├── fase-1-evaluacion.docx
│   ├── arquitectura-smart-city.png
│   └── almacenamiento-visualizacion.md
├── src/
│   ├── streaming_smart_city.py
│   └── resumen_dashboard_smart_city.py
├── data/
│   ├── eventos_validos.jsonl
│   ├── anomalias.jsonl
│   ├── eventos_rechazados.jsonl
│   └── resumen_dashboard.json
└── assets/
    └── diagramas/
```

## Implementación realizada
### 1. Ingesta y procesamiento
Se desarrolló un script en Python para simular eventos de múltiples fuentes urbanas. Cada evento es validado, clasificado y procesado mediante reglas simples para detectar anomalías como:
- velocidad excesiva en unidades de transporte;
- altos niveles de contaminación;
- eventos críticos detectados por cámaras.

### 2. Almacenamiento lógico
Los resultados del pipeline se separan en tres tipos de salida:
- **eventos_validos.jsonl**: eventos aceptados por el proceso de validación;
- **anomalias.jsonl**: eventos que activan reglas de alerta;
- **eventos_rechazados.jsonl**: registros con inconsistencias o valores fuera de rango.

Esta organización representa, de forma simplificada, la separación entre datos procesados, alertas operativas y registros descartados.

### 3. Visualización resumida
Se desarrolló un segundo script para leer los archivos generados por la fase de procesamiento y construir métricas agregadas, tales como:
- total de eventos procesados;
- porcentaje de eventos válidos y rechazados;
- anomalías por tipo y por fuente;
- eventos y alertas por zona.

Estas métricas sirven como base para un dashboard operativo orientado a la toma de decisiones en un entorno Smart City.

## Instrucciones de ejecución
### Requisitos
- Python 3.10 o superior

### Ejecutar la simulación de streaming
```bash
python src/streaming_smart_city.py
```

### Ejecutar el resumen para dashboard
```bash
python src/resumen_dashboard_smart_city.py
```

## Relación con Big Data
El proyecto responde a las dimensiones principales del Big Data de la siguiente manera:
- **Volumen:** almacenamiento de grandes cantidades de eventos urbanos.
- **Velocidad:** procesamiento continuo de eventos mediante streaming simulado.
- **Variedad:** integración de múltiples fuentes con estructuras distintas.
- **Veracidad:** validación básica de estructura y rangos aceptables.
- **Viabilidad:** separación entre operación en tiempo real y análisis posterior.
- **Visualización:** generación de indicadores útiles para tableros de monitoreo.

## Relación con ISO/IEC 20547
La propuesta toma como referencia la familia **ISO/IEC 20547**, especialmente:
- **Parte 3:** arquitectura de referencia para Big Data;
- **Parte 4:** seguridad y privacidad en entornos distribuidos.

A partir de ello, se justifica una arquitectura modular, la separación por capas, la necesidad de trazabilidad del dato y la incorporación de controles mínimos de validación y gobierno de la información.

## Resultados esperados
Al ejecutar el proyecto se obtiene:
- evidencia de simulación de ingesta continua;
- clasificación de eventos válidos, anómalos y rechazados;
- métricas operativas resumidas para visualización;
- base técnica para futuras extensiones hacia almacenamiento más robusto, dashboards interactivos y modelos de machine learning.

## Conclusión
Este proyecto demuestra, en un contexto académico, cómo una arquitectura de Big Data puede diseñarse e implementarse de forma progresiva para resolver un problema urbano realista. La propuesta integra arquitectura, procesamiento, almacenamiento y visualización bajo una lógica coherente con las 6 V's del Big Data y con lineamientos de la serie ISO/IEC 20547.
