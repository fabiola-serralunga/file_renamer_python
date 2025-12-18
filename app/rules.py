def build_new_name(original_name, index, prefix="file"):
    """
    Normaliza nombres según convención Python (snake_case):
    - minúsculas
    - espacios → _
    - guiones - → _
    """
    name, ext = original_name.rsplit(".", 1)
    " Separa nombre de archivo de extension "

    name = name.lower()
    name = name.replace(" ", "_")
    name = name.replace("-", "_")
    " Normaliza nombre "

    ext = ext.lower()
    " Normaliza extension "

    return f"{prefix}_{name}_{index:03d}.{ext}"
    " Devuelve el nombre del archivo con formatted strings literal "
    