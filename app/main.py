from pathlib import Path
import argparse
from app.renamer import rename_files


def main():
    parser = argparse.ArgumentParser(
        description="Renombrador de archivos con modo seguro (dry-run)"
    )

    parser.add_argument(
        "--path",
        required=True,
        help="Ruta a la carpeta con archivos a renombrar"
    )

    parser.add_argument(
        "--prefix",
        default="file",
        help="Prefijo para los archivos renombrados"
    )

    parser.add_argument(
        "--start-index",
        type=int,
        default=1,
        help="Número inicial para la numeración"
    )
    
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Procesar archivos en subcarpetas recursivamente"
    )
    
    parser.add_argument(
        "--global-index",
        action="store_true",
        help="Usar numeración continua global (en lugar de por carpeta). Solo con --recursive"
    )
    
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Ejecuta el renombrado real (sin este flag es dry-run)"
    )

    args = parser.parse_args()

    # Validación de argumentos
    if args.global_index and not args.recursive:
        print("❌ Error: --global-index solo puede usarse con --recursive")
        return

    folder_path = Path(args.path).resolve()

    if not folder_path.exists():
        print(f"❌ Error: la ruta no existe: {folder_path}")
        return

    if not folder_path.is_dir():
        print(f"❌ Error: la ruta no es una carpeta: {folder_path}")
        return

    rename_files(
        folder_path=str(folder_path),
        prefix=args.prefix,
        dry_run=not args.execute, 
        start_index=args.start_index,
        recursive=args.recursive,
        global_index=args.global_index
    )

if __name__ == "__main__":
    main()