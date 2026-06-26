"""
etl_kpi_pipeline.py
--------------------
ETL único y profesional: lee el dataset original de 17 columnas desde HDFS,
selecciona las 10 columnas necesarias para los KPIs, y escribe un CSV limpio
y atómico de vuelta a HDFS.

Ejecutar con:
    spark-submit --master spark://master:7077 etl_kpi_pipeline.py
"""

from pyspark.sql import SparkSession
from pyspark.sql.types import (
    StructType, StructField, StringType, IntegerType, DoubleType
)
import sys

# ----------------------------------------------------------------------
# 1. Configuracion de rutas (UNICA fuente de verdad)
# ----------------------------------------------------------------------
SOURCE_PATH = "hdfs://master:9000/retail_project/retail_sales_dataset.csv"
CLEAN_HDFS_PATH = "hdfs://master:9000/retail_project/kpi_sales_clean"

EXPECTED_SOURCE_COLUMNS = 17

# ----------------------------------------------------------------------
# 2. Spark Session
# ----------------------------------------------------------------------
spark = (
    SparkSession.builder
    .appName("RetailKPI_ETL")
    .getOrCreate()
)

# ----------------------------------------------------------------------
# 3. Esquema EXPLICITO del dataset original (17 columnas)
#    -> Nunca usar inferSchema=True en produccion: si una fila viene
#       corrupta, Spark infiere mal el tipo y desordena columnas.
# ----------------------------------------------------------------------
schema = StructType([
    StructField("transaction_id",      StringType(), True),
    StructField("transaction_date",    StringType(), True),
    StructField("customer_id",         StringType(), True),
    StructField("customer_gender",     StringType(), True),
    StructField("customer_age_group",  StringType(), True),
    StructField("customer_segment",    StringType(), True),
    StructField("product_id",          StringType(), True),
    StructField("product_name",        StringType(), True),
    StructField("category",            StringType(), True),
    StructField("brand",               StringType(), True),
    StructField("quantity",            IntegerType(), True),
    StructField("unit_price",          DoubleType(), True),
    StructField("discount_pct",        DoubleType(), True),
    StructField("sales_amount",        DoubleType(), True),
    StructField("payment_method",      StringType(), True),
    StructField("sales_channel",       StringType(), True),
    StructField("region",              StringType(), True),
])

print(f"[ETL] Leyendo dataset original desde: {SOURCE_PATH}")

df = (
    spark.read
    .option("header", "true")
    .option("mode", "PERMISSIVE")          # filas corruptas -> null, no rompe el job
    .schema(schema)
    .csv(SOURCE_PATH)
)

# ----------------------------------------------------------------------
# 4. VALIDACION DE INTEGRIDAD (obligatoria antes de transformar)
# ----------------------------------------------------------------------
actual_columns = len(df.columns)
row_count = df.count()

print(f"[ETL] Columnas leidas: {actual_columns} (esperadas: {EXPECTED_SOURCE_COLUMNS})")
print(f"[ETL] Filas leidas:    {row_count}")

if actual_columns != EXPECTED_SOURCE_COLUMNS:
    print("[ETL] ERROR: el dataset origen no tiene 17 columnas. Abortando.")
    spark.stop()
    sys.exit(1)

if row_count == 0:
    print("[ETL] ERROR: el dataset origen esta vacio o no se pudo leer "
          "(posible bloque danado en HDFS).")
    spark.stop()
    sys.exit(1)

# ----------------------------------------------------------------------
# 5. Seleccion de las 10 columnas necesarias para los 10 KPIs
# ----------------------------------------------------------------------
kpi_df = df.select(
    "transaction_id",
    "customer_segment",
    "product_name",
    "category",
    "discount_pct",
    "sales_amount",
    "payment_method",
    "sales_channel",
    "region",
    "customer_age_group",
)

# Limpieza minima: descartar filas sin sales_amount (no aportan a ningun KPI)
kpi_df = kpi_df.dropna(subset=["sales_amount"])

print(f"[ETL] Filas finales en dataset KPI: {kpi_df.count()}")
kpi_df.printSchema()

# ----------------------------------------------------------------------
# 6. Escritura ATOMICA a HDFS (overwrite completo, nunca append manual)
# ----------------------------------------------------------------------
(
    kpi_df
    .coalesce(1)                      # 1 archivo de salida -> facil de mergear/leer
    .write
    .mode("overwrite")
    .option("header", "true")
    .csv(CLEAN_HDFS_PATH)
)

print(f"[ETL] Dataset limpio escrito en: {CLEAN_HDFS_PATH}")
print("[ETL] Verificar marcador _SUCCESS antes de continuar el pipeline.")

spark.stop()