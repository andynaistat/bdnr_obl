import os
import argparse
from typing import Literal, cast

from utils_dataset import make_personas_df, ensure_out_dir
from utils_format import human_bytes


def main():
    parser = argparse.ArgumentParser(description="Comparar compresiones de Parquet con un dataset grande.")
    parser.add_argument("--rows", type=int, default=1_000_000, help="Cantidad de filas a generar (por defecto: 1,000,000)")
    args = parser.parse_args()

    df = make_personas_df(args.rows)
    out_dir = ensure_out_dir()

    # Probar distintos algoritmos de compresión
    for codec in ["snappy", "gzip", "zstd"]:
        path = out_dir / f"personas_{codec}.parquet"
        df.to_parquet(
            str(path),
            compression=cast(Literal["snappy", "gzip", "zstd"], codec),
            engine="pyarrow",
        )
        size = os.path.getsize(str(path))
        print(f"{codec:<8} → {human_bytes(size)} ({size:,} bytes)")

    print("\n✅ Archivos Parquet generados con distintas compresiones en 'output/'")


if __name__ == "__main__":
    main()
