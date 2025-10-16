def human_bytes(num_bytes: int, decimals: int = 2) -> str:
    """Return a human-readable size using KB/MB/GB units (base 1024)."""
    if num_bytes is None:
        return "0 B"
    n = float(num_bytes)
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    i = 0
    while n >= 1024 and i < len(units) - 1:
        n /= 1024.0
        i += 1
    if units[i] == "B":
        return f"{int(n)} {units[i]}"
    return f"{n:.{decimals}f} {units[i]}"
