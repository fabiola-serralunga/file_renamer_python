def build_new_name(original_name, index, prefix="file"):
    """
    Normaliza nombres según convención Python (snake_case):
    - minúsculas
    - espacios → _
    - guiones - → _
    """
    # Separa nombre de archivo de extensión
    name, ext = original_name.rsplit(".", 1)

    # Normaliza nombre: minúsculas y reemplaza espacios/guiones por _
    name = name.lower()
    name = name.replace(" ", "_")
    name = name.replace("-", "_")

    # Normaliza extensión a minúsculas
    ext = ext.lower()

    # Devuelve el nombre formateado con padding de 3 dígitos
    return f"{prefix}_{name}_{index:03d}.{ext}"