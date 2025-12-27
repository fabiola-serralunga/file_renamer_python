import os
import re
from app.rules import build_new_name

def rename_files(folder_path, prefix="file", dry_run=False):
    # Listar solo archivos
    files = sorted(
        (f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))),
        key=lambda s: s.lower()
    )


    # Validación carpeta vacía
    if not files:
        print(f"[INFO] No hay archivos para renombrar en: {folder_path}")
        return

    # Patrón para archivos ya renombrados
    pattern = re.compile(rf"^{re.escape(prefix)}_.+_\d{{3}}\.\w+$")

    # Iterar y renombrar
    for index, filename in enumerate(files, start=1):
        # Saltar archivos ya renombrados
        if pattern.match(filename):
            print(f"[SKIP] Archivo ya renombrado: {filename}")
            continue

        # Construir nuevo nombre
        new_name = build_new_name(filename, index, prefix)

        old_path = os.path.join(folder_path, filename)
        new_path = os.path.join(folder_path, new_name)

        if dry_run:
            print(f"[DRY-RUN] {filename} → {new_name}")
        else:
            os.rename(old_path, new_path)
            print(f"{filename} → {new_name}")
