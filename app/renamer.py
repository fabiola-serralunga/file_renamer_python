import os
import re
from app.rules import build_new_name

def rename_files(folder_path, prefix="file", dry_run=False, start_index=1):
    # Listar archivos ordenados alfabéticamente (case-insensitive)
    files = sorted(
        (f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))),
        key=lambda s: s.lower()
    )

    if not files:
        print(f"[INFO] No hay archivos para renombrar en: {folder_path}")
        return

    # Patrón para detectar archivos que ya tenían formato
    pattern = re.compile(rf"^{re.escape(prefix)}_.+_\d{{3}}\.\w+$")

    # Contador de numeración continua
    current_index = start_index

    for filename in files:
        new_name = build_new_name(filename, current_index, prefix)

        # Si ya cumple el patrón, mostramos mensaje especial pero lo seguimos renombrando
        if pattern.match(filename):
            msg = f"[DRY-RUN] Archivo previamente normalizado: {filename} → {new_name}"
        else:
            msg = f"[DRY-RUN] {filename} → {new_name}"

        if dry_run:
            print(msg)
        else:
            old_path = os.path.join(folder_path, filename)
            new_path = os.path.join(folder_path, new_name)
            os.rename(old_path, new_path)
            print(msg)

        current_index += 1
