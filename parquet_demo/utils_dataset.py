from __future__ import annotations

from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd


def _choices(items: Iterable[str], n: int, rng: np.random.Generator) -> list[str]:
    arr = list(items)
    idx = rng.integers(0, len(arr), size=n, endpoint=False)
    return [arr[i] for i in idx]


def make_personas_df(n_rows: int, seed: int = 42) -> pd.DataFrame:
    """
    Generate a large, compressible demo dataset for Parquet/CSV comparisons.

    Columns
    - id: int64 sequential
    - nombre: repeated names (categorical-like)
    - edad: small-range ints
    - pais: small set of country names (highly compressible)
    - ciudad: small set of city names
    - descripcion: repeated phrases (dictionary-encodable)
    - fecha_registro: dates over ~1 year
    - ingreso: float with two decimals
    - suscriptor: boolean with ~10% True
    """
    rng = np.random.default_rng(seed)

    n = int(n_rows)
    ids = np.arange(1, n + 1, dtype=np.int64)

    nombres = [
        "Ana", "Luis", "Marta", "Juan", "Sofía", "Carlos", "Lucía", "Diego", "Valentina",
        "Pedro", "María", "Jorge", "Camila", "Andrés", "Gabriela", "Nicolás", "Paula",
        "Felipe", "Carolina", "Fernando"
    ]
    paises = [
        "Uruguay", "Argentina", "Chile", "Perú", "Brasil", "Paraguay", "Bolivia",
        "Colombia", "Ecuador", "Venezuela"
    ]
    ciudades = [
        "Montevideo", "Buenos Aires", "Santiago", "Lima", "São Paulo", "Asunción", "La Paz",
        "Bogotá", "Quito", "Caracas", "Rosario", "Córdoba", "Valparaíso", "Cusco", "Medellín"
    ]
    frases = [
        "Usuario activo con compras recientes",
        "Cliente nuevo sin historial",
        "Preferencia por envíos rápidos",
        "Participa en promociones estacionales",
        "Cuenta verificada y con reseñas",
        "Interés en productos tecnológicos",
        "Historial de devoluciones bajo",
        "Fuerte interacción con notificaciones",
        "Usa cupones con frecuencia",
        "Carrito abandonado varias veces"
    ]

    nombre_col = _choices(nombres, n, rng)
    pais_col = _choices(paises, n, rng)
    ciudad_col = _choices(ciudades, n, rng)
    frase_col = _choices(frases, n, rng)

    # edades 18..80, skewed toward 25-45
    edad_raw = rng.integers(18, 81, size=n)
    edad_col = np.clip(np.round(edad_raw * 0.7 + rng.normal(10, 8, size=n)).astype(int), 18, 80)

    # fechas dentro de ~365 días
    base = np.datetime64("2024-01-01")
    days = rng.integers(0, 366, size=n)
    fechas = base + days.astype("timedelta64[D]")

    # ingreso mensual aproximado, con 2 decimales
    ingreso = np.round(rng.normal(loc=1200.0, scale=600.0, size=n).clip(0, None), 2)

    # suscriptor premium ~10%
    suscriptor = rng.random(n) < 0.10

    # Descripción compuesta para mantener repetición pero con ligera variación
    desc = [f"{frase_col[i]}" for i in range(n)]

    df = pd.DataFrame({
        "id": ids,
        "nombre": pd.Series(nombre_col, dtype="category"),
        "edad": edad_col.astype(np.int16),
        "pais": pd.Series(pais_col, dtype="category"),
        "ciudad": pd.Series(ciudad_col, dtype="category"),
        "descripcion": pd.Series(desc, dtype="category"),
        "fecha_registro": pd.to_datetime(fechas),
        "ingreso": ingreso.astype(np.float32),
        "suscriptor": suscriptor,
    })

    return df


def ensure_out_dir() -> Path:
    out = Path(__file__).resolve().parent / "output"
    out.mkdir(parents=True, exist_ok=True)
    return out
