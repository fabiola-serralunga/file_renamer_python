import os
from rules import build_new_name

def rename_files(folder_path, prefix="file", dry_run=False):
    files = os.listdir(folder_path)
    files = [f for f in files if os.path.isfile(os.path.join(folder_path, f))]

    for index, filename in enumerate(files, start=1):
        new_name = build_new_name(filename, index, prefix)

        old_path = os.path.join(folder_path, filename)
        new_path = os.path.join(folder_path, new_name)

        if dry_run:
            print(f"[DRY-RUN] {filename} → {new_name}")
        else:
            os.rename(old_path, new_path)
            print(f"{filename} → {new_name}")
