import os
import re
from pathlib import Path
from app.rules import build_new_name

def rename_files(folder_path, prefix="file", dry_run=True, 
                 start_index=1, recursive=False, global_index=False,
                 rules_config=None):  
    """
    Renombra archivos en una carpeta.
    
    Args:
        folder_path: Ruta de la carpeta
        prefix: Prefijo para los nombres
        dry_run: Si True, solo muestra lo que haría
        start_index: Número inicial para la numeración
        recursive: Si True, procesa subcarpetas
        global_index: Si True, usa numeración global (solo con recursive)
        rules_config: Configuración de reglas (opcional, para futuras versiones)
    """

    # Inicializar rules_config si es None
    if rules_config is None:
        rules_config = {}
    
    # Convertir a Path para manejo más fácil
    root_path = Path(folder_path).resolve()
    
    if not root_path.exists():
        print(f"❌ Error: la ruta no existe: {root_path}")
        return
    
    if not root_path.is_dir():
        print(f"❌ Error: la ruta no es una carpeta: {root_path}")
        return
    
    # Determinar cómo recolectar archivos
    if recursive:
        # Recolectar archivos de forma recursiva
        all_files = []
        for file_path in root_path.rglob("*"):
            if file_path.is_file():
                all_files.append(file_path)
        empty_folders = _detect_empty_folders(root_path, all_files)

        # Verificar si hay archivos ANTES de continuar
        if not all_files:
            print(f"[INFO] No hay archivos para renombrar en: {folder_path} (ni en subcarpetas)")
            return
        
        # Ordenar por ruta para consistencia
        all_files.sort(key=lambda p: (str(p.parent).lower(), p.name.lower()))
        
        print(f"[INFO] Encontrados {len(all_files)} archivos en {len(set(f.parent for f in all_files))} carpetas")
        
        # Procesar según el modo de numeración
        if global_index:
            # Numeración global continua
            _process_files_global(all_files, prefix, dry_run, start_index, root_path)
        else:
            # Numeración por carpeta
            _process_files_by_folder(all_files, prefix, dry_run, start_index, root_path)
        
        if empty_folders and dry_run:
            print(f"\n[INFO] {len(empty_folders)} carpeta(s) vacía(s) encontrada(s):")
        for folder in sorted(empty_folders, key=lambda p: str(p).lower()):
            folder_name = folder.relative_to(root_path)
            print(f"  • {folder_name}/")
        
    else:
        # Modo original (solo carpeta actual)
        files = _get_files_in_folder(root_path)
        
        if not files:
            print(f"[INFO] No hay archivos para renombrar en: {folder_path}")
            return
        
        _process_single_folder(root_path, prefix, dry_run, start_index)

def _detect_empty_folders(root_path, files):
    """
    Detecta carpetas vacías en un árbol de directorios.
    
    Args:
        root_path (Path): carpeta raíz
        files (list[Path]): lista de archivos encontrados
    
    Returns:
        set[Path]: conjunto de carpetas vacías
    """
    # Todas las carpetas del árbol
    all_folders = {p for p in root_path.rglob("*") if p.is_dir()}
    all_folders.add(root_path)

    # Carpetas que contienen al menos un archivo
    folders_with_files = {file.parent for file in files}

    return all_folders - folders_with_files

def _get_files_in_folder(folder_path):
    """Obtiene lista de archivos en una carpeta."""
    files = []
    for item in folder_path.iterdir():
        if item.is_file():
            files.append(item.name)
    
    # Ordenar case-insensitive
    files.sort(key=lambda s: s.lower())
    return files


def _process_single_folder(folder_path, prefix, dry_run, start_index):
    """Procesa archivos en una sola carpeta (comportamiento original)."""
    
    files = _get_files_in_folder(folder_path)
    
    if not files:
        return

    # Patrón para detectar archivos que ya tenían formato
    pattern = re.compile(rf"^{re.escape(prefix)}_.+_\d{{3}}\.[a-zA-Z0-9]+(?:\.[a-zA-Z0-9]+)*$")

    # Contador de numeración continua
    current_index = start_index

    for filename in files:
        new_name = build_new_name(filename, current_index, prefix)

        # CASO 1: Dry-run + ya normalizado
        if dry_run and pattern.match(filename):
            print(f"  [DRY-RUN] Archivo previamente normalizado: {filename} → {new_name}")
        
        # CASO 2: Dry-run + no normalizado
        elif dry_run:
            print(f"  [DRY-RUN] {filename} → {new_name}")
        
        # CASO 3: Ejecución real + ya normalizado
        elif pattern.match(filename):
            old_path = folder_path / filename
            new_path = folder_path / new_name
            old_path.rename(new_path)
            print(f"  ✅ [RENOMBRADO] Archivo previamente normalizado: {filename} → {new_name}")
        
        # CASO 4: Ejecución real + no normalizado
        else:
            old_path = folder_path / filename
            new_path = folder_path / new_name
            old_path.rename(new_path)
            print(f"  ✅ [RENOMBRADO] {filename} → {new_name}")

        current_index += 1

def _process_files_global(all_files, prefix, dry_run, start_index, root_path):
    """Procesa archivos con numeración global continua."""
    
    pattern = re.compile(rf"^{re.escape(prefix)}_.+_\d{{3}}\.[a-zA-Z0-9]+(?:\.[a-zA-Z0-9]+)*$")
    current_index = start_index
    
    for file_path in all_files:
        filename = file_path.name
        relative_path = file_path.relative_to(root_path)
        parent_dir = file_path.parent
        
        new_name = build_new_name(filename, current_index, prefix)
        
        # Determinar si ya estaba normalizado
        already_normalized = pattern.match(filename)
        
        if dry_run:
            if already_normalized:
                print(f"  [DRY-RUN] {relative_path} (normalizado) → {new_name}")
            else:
                print(f"  [DRY-RUN] {relative_path} → {new_name}")
        else:
            new_path = parent_dir / new_name
            file_path.rename(new_path)
            
            if already_normalized:
                print(f"  ✅ [RENOMBRADO] {relative_path} (normalizado) → {new_name}")
            else:
                print(f"  ✅ [RENOMBRADO] {relative_path} → {new_name}")
        
        current_index += 1

def _process_files_by_folder(all_files, prefix, dry_run, start_index, root_path):
    """Procesa archivos reiniciando numeración en cada carpeta."""
    
    pattern = re.compile(rf"^{re.escape(prefix)}_.+_\d{{3}}\.[a-zA-Z0-9]+(?:\.[a-zA-Z0-9]+)*$")
    
    # ... (código de agrupación igual) ...
    
    for file_path in file_list:
        filename = file_path.name
        new_name = build_new_name(filename, current_index, prefix)
        
        # Determinar si ya estaba normalizado
        already_normalized = pattern.match(filename)
        
        if dry_run:
            if already_normalized:
                print(f"  [DRY-RUN] {filename} (normalizado) → {new_name}")
            else:
                print(f"  [DRY-RUN] {filename} → {new_name}")
        else:
            new_path = file_path.parent / new_name
            file_path.rename(new_path)
            
            if already_normalized:
                print(f"  ✅ [RENOMBRADO] {filename} (normalizado) → {new_name}")
            else:
                print(f"  ✅ [RENOMBRADO] {filename} → {new_name}")
        
        current_index += 1
    
    # Mostrar resumen de carpetas vacías (solo en dry_run para no sobrecargar)
    if empty_folders and dry_run:
        print(f"\n[INFO] {len(empty_folders)} carpeta(s) vacía(s) encontrada(s):")
        # Ordenar por nombre
        for folder in sorted(empty_folders):
            folder_name = Path(folder).relative_to(root_path)
            print(f"  • {folder_name}/")