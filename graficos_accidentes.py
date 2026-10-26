import os
import glob
import pandas as pd
import matplotlib.pyplot as plt

# Carpeta con los resultados de Spark
carpeta = "resultados_accidentes"

# Crear carpeta para guardar graficos
os.makedirs("graficos", exist_ok=True)

# Analisis disponibles
analisis = {
    "zona": "Accidentes por zona",
    "dia": "Accidentes por dia de la semana",
    "jornada": "Accidentes por jornada",
    "barrio": "Barrios con mayor numero de accidentes"
}

for nombre, titulo in analisis.items():

    archivos = glob.glob(f"{carpeta}/{nombre}/part-*.csv")

    if not archivos:
        print(f"No se encontraron datos para {nombre}")
        continue

    # Leer los resultados
    df = pd.read_csv(archivos[0])

    if "cantidad" not in df.columns:
        print(f"No existe la columna cantidad en {nombre}")
        continue

    # Obtener columna de categoria
    categoria = [c for c in df.columns if c != "cantidad"][0]

    # Seleccionar los primeros 10 registros
    df = df.head(10)

    # Crear grafico
    plt.figure(figsize=(11, 6))
    plt.bar(df[categoria].astype(str), df["cantidad"], color="steelblue")

    plt.title(titulo)
    plt.xlabel(categoria)
    plt.ylabel("Cantidad de accidentes")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    # Guardar imagen
    salida = f"graficos/{nombre}.png"
    plt.savefig(salida, dpi=150)
    plt.close()

    print(f"Grafico generado: {salida}")

print("\n=== GRAFICOS FINALIZADOS ===")
