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

---

# Implementación: Motor de Recomendaciones Duolingo

Sistema de recomendación de ejercicios basado en **Filtrado Colaborativo** usando Neo4j como base de datos de grafos. Esta implementación simula un motor de recomendaciones similar al de Duolingo, que sugiere ejercicios personalizados basándose en las dificultades del usuario y el comportamiento de usuarios similares.

### Estructura

- `duolingo-implementation/recommendation-engine/app.py`: Motor de recomendaciones que implementa el algoritmo de filtrado colaborativo.
- `duolingo-implementation/recommendation-engine/python loader.py`: Script para cargar datos de prueba en Neo4j (usuarios, habilidades, ejercicios y relaciones).

### Requisitos

- Python 3.10+
- Neo4j 5.12+ (configurado en `.devcontainer/docker-compose.yml`)
- Paquetes Python:
  - `neo4j>=5.0.0`
  - `pandas>=2.0.0`

### Configuración

El proyecto utiliza un entorno devcontainer con Docker Compose que incluye:
- Contenedor de Python para la aplicación
- Contenedor de Neo4j con autenticación `neo4j/password`
- Puerto 7687 (Bolt) y 7474 (Browser) expuestos

### Uso

1. **Cargar datos de prueba en Neo4j:**
   ```bash
   cd duolingo-implementation/recommendation-engine
   python3 "python loader.py"
   ```

2. **Ejecutar recomendaciones para un usuario:**
   ```bash
   python3 app.py [user_id]
   ```
   
   Ejemplo:
   ```bash
   python3 app.py ana_01
   ```

### Algoritmo de Recomendación

El motor implementa **Filtrado Colaborativo** con los siguientes pasos:

1. **Identificar debilidades**: Detecta las habilidades con las que el usuario tiene dificultades.
2. **Buscar usuarios similares**: Encuentra "vecinos" (usuarios con perfiles similares) usando relaciones `SIMILAR_A`.
3. **Analizar éxitos de vecinos**: Identifica ejercicios que los usuarios similares completaron exitosamente para esas mismas debilidades.
4. **Filtrar ejercicios ya realizados**: Excluye ejercicios que el usuario actual ya intentó.

### Modelo de Datos

El grafo en Neo4j contiene:

- **Nodos:**
  - `Usuario`: Representa usuarios del sistema
  - `Habilidad`: Habilidades lingüísticas (ej: Subjuntivo, Pasado Simple)
  - `Ejercicio`: Ejercicios disponibles en la plataforma

- **Relaciones:**
  - `TIENE_DIFICULTAD_CON`: Usuario → Habilidad (con tasa de error)
  - `INTENTO`: Usuario → Ejercicio (con resultado: éxito/fallo)
  - `PRUEBA`: Ejercicio → Habilidad (estructura pedagógica)
  - `SIMILAR_A`: Usuario → Usuario (score de similitud calculado por ML)

### Notas

- La conexión a Neo4j utiliza el nombre del servicio Docker (`neo4j:7687`) cuando se ejecuta dentro del devcontainer.
- Los datos de prueba incluyen usuarios de ejemplo (Ana, Luis) con historiales de ejercicios y relaciones de similitud precalculadas.
- El sistema está diseñado para funcionar en tiempo real, consultando el grafo directamente para generar recomendaciones personalizadas.
