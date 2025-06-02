def ascii_bar(label: str, current: int, maximum: int, length: int = 20, fill_char: str = "#") -> str:
    """Render an ASCII bar: Label [#####-----] cur/max."""
    ratio = max(0, min(1, current / maximum)) if maximum else 0
    filled = int(ratio * length)
    empty = length - filled
    bar = fill_char * filled + "-" * empty
    return f"{label:12} [{bar}] {current}/{maximum}"