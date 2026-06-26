<<<<<<< HEAD
# RetailMax Big Data — Manual Técnico

Manual técnico end-to-end del proyecto **RetailMax Big Data**, que documenta la arquitectura
e implementación de un pipeline de datos completo: ingestión, procesamiento distribuido,
generación de KPIs y visualización en dashboard.

## 📋 Contenido del manual

- **Sección 00** — Introducción / requisitos previos
- **Fase 01** — Configuración del entorno (Docker / clúster)
- **Fase 02** — Ingesta de datos en HDFS
- **Fase 03** — Procesamiento ETL con PySpark
- **Fase 04** — Generación de KPIs (kpi_sales.csv)
- **Fase 05** — Dashboard interactivo con Streamlit
- **Sección 17** — Despliegue y acceso externo
- **Solución de problemas** — Errores comunes y cómo resolverlos

## 📊 Dataset

`data/retail_sales_dataset.csv` — 120,000 transacciones de venta retail con campos como
cliente, producto, categoría, marca, canal de venta, región, método de pago, etc.
Usado como input para el pipeline ETL (PySpark) y la generación de KPIs.

## 🔧 Stack tecnológico

- **HDFS** — Almacenamiento distribuido
- **Apache Spark (PySpark)** — Procesamiento ETL
- **Streamlit** — Dashboard de visualización
- **Docker** — Contenerización del entorno

## 📂 Estructura del repositorio

\`\`\`
retailmax-bigdata/
├── README.md
├── docs/
│   └── manual_retailmax_bigdata.html
├── data/
│   └── retail_sales_dataset.csv
└── .gitignore
\`\`\`

## 🚀 Cómo ver el manual

\`\`\`bash
git clone https://github.com/yolibueno/retailmax-bigdata.git
cd retailmax-bigdata
start docs/manual_retailmax_bigdata.html
\`\`\`

## 👤 Autor

**Yoli Bueno Tulumba** — Universidad Peruana Unión, Ciclo 9, Curso de Big Data
=======
# retailmax-bigdata
Manual técnico y pipeline Big Data del proyecto RetailMax
>>>>>>> f73ad762892931cd1272c27bd38df3c8b30732b1
