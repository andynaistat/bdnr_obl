import os
import argparse
from pathlib import Path

from utils_dataset import make_personas_df, ensure_out_dir
from utils_format import human_bytes


def main():
    parser = argparse.ArgumentParser(description="Comparar tamaños entre CSV y Parquet para un dataset grande.")
    parser.add_argument("--rows", type=int, default=1_000_000, help="Cantidad de filas a generar (por defecto: 1,000,000)")
    parser.add_argument("--codec", type=str, choices=["snappy", "gzip", "zstd"], default="snappy", help="Compresión para Parquet")
    args = parser.parse_args()

    df = make_personas_df(args.rows)
    out_dir = ensure_out_dir()
    csv_path = out_dir / "personas.csv"
    parquet_path = out_dir / f"personas_{args.codec}.parquet"

    # Guardar en CSV y Parquet
    df.to_csv(str(csv_path), index=False)
    df.to_parquet(str(parquet_path), engine="pyarrow", compression=args.codec)

    # Comparar tamaños
    csv_size = os.path.getsize(str(csv_path))
    parquet_size = os.path.getsize(str(parquet_path))

    ratio = csv_size / parquet_size if parquet_size else float("inf")
    print(f"📊 Filas: {len(df):,}")
    print(f"📊 Tamaño CSV: {human_bytes(csv_size)} ({csv_size:,} bytes)")
    print(f"📦 Tamaño Parquet ({args.codec}): {human_bytes(parquet_size)} ({parquet_size:,} bytes)")
    print(f"💡 Parquet es aproximadamente {ratio:.1f}x más compacto.")


if __name__ == "__main__":
    main()
