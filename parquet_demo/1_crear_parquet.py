from pathlib import Path
import argparse

from utils_dataset import make_personas_df, ensure_out_dir


def main():
    parser = argparse.ArgumentParser(description="Crear archivo Parquet de ejemplo con muchas filas.")
    parser.add_argument("--rows", type=int, default=1_000_000, help="Cantidad de filas a generar (por defecto: 1,000,000)")
    parser.add_argument("--out", type=str, default="personas.parquet", help="Nombre del archivo de salida")
    args = parser.parse_args()

    df = make_personas_df(args.rows)
    out_dir = ensure_out_dir()
    out_path = out_dir / args.out

    # Guardar como Parquet (compresión Snappy por defecto)
    df.to_parquet(str(out_path), engine="pyarrow", compression="snappy")
    print(f"✅ Archivo '{out_path.name}' guardado correctamente en '{out_dir}'.")


if __name__ == "__main__":
    main()
