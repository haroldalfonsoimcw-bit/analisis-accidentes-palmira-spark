from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, trim, upper
import os

# Crear sesion de Spark
spark = SparkSession.builder \
    .appName("AnalisisAccidentesPalmira") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# Cargar conjunto de datos
archivo = "Accidentes_de_transito_Palmira_20261026.csv"

df = spark.read.csv(
    archivo,
    header=True,
    inferSchema=True
)

print("\n=== ESTRUCTURA DEL CONJUNTO DE DATOS ===")
df.printSchema()

print("\n=== COLUMNAS DISPONIBLES ===")
print(df.columns)

print("\n=== PRIMEROS REGISTROS ===")
df.show(5, truncate=False)

print("\n=== TOTAL DE REGISTROS ===")
print(df.count())

# Limpieza inicial
df = df.dropDuplicates()

# Normalizar nombres de columnas
for nombre in df.columns:
    nuevo = nombre.strip().lower().replace(" ", "_")
    df = df.withColumnRenamed(nombre, nuevo)

print("\n=== COLUMNAS NORMALIZADAS ===")
print(df.columns)

# Crear carpeta para resultados
os.makedirs("resultados_accidentes", exist_ok=True)

# Guardar resumen del conjunto de datos
with open("resultados_accidentes/resumen.txt", "w") as f:
    f.write("ANALISIS DE ACCIDENTES DE TRANSITO EN PALMIRA\n")
    f.write("Total de registros: " + str(df.count()) + "\n")
    f.write("Columnas: " + str(df.columns) + "\n")

# Analisis automatico de columnas categoricas
columnas_interes = [
    "clasificacion",
    "dia",
    "jornada",
    "zona",
    "barrio"
]

for palabra in columnas_interes:

    columnas = [
        c for c in df.columns
        if palabra in c
    ]

    if columnas:
        columna = columnas[0]

        print("\n=== ANALISIS POR", columna.upper(), "===")

        resultado = df.groupBy(columna) \
            .agg(count("*").alias("cantidad")) \
            .orderBy(col("cantidad").desc())

        resultado.show(15, truncate=False)

        resultado.coalesce(1).write \
            .mode("overwrite") \
            .option("header", True) \
            .csv("resultados_accidentes/" + palabra)

print("\n=== ANALISIS FINALIZADO ===")

spark.stop()
