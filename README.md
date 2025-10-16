# Demo: CSV vs Parquet (Python)

Proyecto simple para demostrar cómo generar, leer y comparar archivos Parquet frente a CSV usando pandas y pyarrow.

Carpeta principal de trabajo: `parquet_demo/`.

## Estructura

- `parquet_demo/1_crear_parquet.py`: Genera un archivo Parquet grande (por defecto 1,000,000 de filas) en `parquet_demo/output/` usando compresión Snappy.
- `parquet_demo/2_leer_parquet.py`: Lee un archivo Parquet de `output/` y muestra un resumen más una lectura selectiva de columnas.
- `parquet_demo/3_comparar_csv_vs_parquet.py`: Genera CSV y Parquet del mismo dataset y compara tamaños (incluye distintas compresiones).
- `parquet_demo/4_compresiones.py`: Genera archivos Parquet con compresiones `snappy`, `gzip` y `zstd` y muestra sus tamaños.
- `parquet_demo/utils_dataset.py`: Generación del dataset y utilidades de carpeta de salida.
- `parquet_demo/utils_format.py`: Función para mostrar tamaños en formato legible.
- `parquet_demo/requirements.txt`: Dependencias de Python.
- `parquet_demo/output/`: Carpeta donde se guardan los archivos generados.

## Requisitos

- Python 3.10+ recomendado.
- Paquetes Python:
  - pandas
  - pyarrow
  - numpy

Instalación de dependencias (Windows PowerShell):

```powershell
# Crear y activar entorno virtual (opcional pero recomendado)
python -m venv .venv; .\.venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r parquet_demo/requirements.txt
```

## Uso rápido

Ubícate en la raíz del repositorio y ejecuta:

```powershell
# 1) Crear un Parquet grande (por defecto 1,000,000 filas)
python parquet_demo/1_crear_parquet.py --rows 1000000 --out personas.parquet

# 2) Leer el Parquet generado y mostrar un resumen
python parquet_demo/2_leer_parquet.py

# 3) Comparar tamaños entre CSV y Parquet (elige compresión)
python parquet_demo/3_comparar_csv_vs_parquet.py --rows 1000000 --codec snappy

# 4) Generar varias compresiones y ver tamaños
python parquet_demo/4_compresiones.py --rows 1000000
```

Notas:
- Los archivos se guardan en `parquet_demo/output/`.
- Puedes cambiar `--rows` para generar menos/más filas según tu máquina.
- Compresiones soportadas: `snappy`, `gzip`, `zstd` (requiere pyarrow).

## Resultados esperados

- Archivos como `personas.parquet`, `personas_snappy.parquet`, `personas_gzip.parquet`, `personas_zstd.parquet` y `personas.csv` dentro de `parquet_demo/output/`.
- Mensajes en consola mostrando tamaños legibles y ratio de compresión al comparar CSV vs Parquet.
