import pandas as pd
from pathlib import Path

# Leer archivo Parquet desde carpeta output
OUT = Path(__file__).resolve().parent / "output"
# Preferir el archivo generado por 1_crear_parquet.py (snappy)
parquet_path = OUT / "personas.parquet"
if not parquet_path.exists():
	# Fallback a cualquiera de las variantes comprimidas si existe
	for alt in ["personas_snappy.parquet", "personas_gzip.parquet", "personas_zstd.parquet"]:
		p = OUT / alt
		if p.exists():
			parquet_path = p
			break

df = pd.read_parquet(str(parquet_path))

print("📄 Vista del archivo Parquet:")
print(f"Ruta: {parquet_path}")
print(f"Shape: {df.shape}")
print("Head():")
print(df.head(5))

# Ejemplo de lectura selectiva
subset = pd.read_parquet(str(parquet_path), columns=["nombre", "edad"])[:5]
print("\n📊 Lectura selectiva (solo nombre y edad, primeras 5 filas):")
print(subset)
