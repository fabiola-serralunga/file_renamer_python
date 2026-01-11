from pathlib import Path
import argparse
import sys
from app.renamer import rename_files
from app.config_loader import ConfigLoader  

def main():
    parser = argparse.ArgumentParser(
        description="Renombrador de archivos con CLI y configuración externa",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
        Casos de uso:
            # Modo original (sigue funcionando):
                python -m app.main --path ./examples/test_files --prefix doc --recursive
  
            # Con archivo de configuración (v4.0.0):
                python -m app.main --config config/basic_v4.json
                python -m app.main --config config/basic_v4.yaml

            # Con archivo de configuración (desde v5.0.0):
                python -m app.main --config config/renamer.json
                python -m app.main --config config/renamer.yaml
  
              # Ver plantilla de configuración:
                python -m app.main --show-template yaml
                python -m app.main --show-template json
  
            # Ayuda completa:
                python -m app.main --help
        """
    )

    # Incorporado desde v.4.0.0 - modos mutuamente excluyentes
    
    mode_group = parser.add_mutually_exclusive_group()
    
    mode_group.add_argument(
        "--config", "-c",
        metavar="ARCHIVO",
        help="Cargar configuración desde archivo YAML/JSON"
    )
    
    mode_group.add_argument(
        "--show-template",
        choices=["yaml", "json"],
        help="Mostrar plantilla de configuración"
    )
    
    # Modos originales - hasta v.3.0.0
    parser.add_argument(
        "--path",
        required=False,
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

    # ===== OPCIONES DE USUARIO =====
    
    # 1. Uso de plantilla
    if args.show_template:
        print("#" * 60)
        print("# PLANTILLA DE CONFIGURACIÓN")
        print("#" * 60)
        print()
        template = ConfigLoader.create_template(args.show_template)
        print(template)
        return
    
    # 2. Uso de --config
    if args.config:
        print(f"📂 Cargando configuración desde: {args.config}")
        
        # Cargar configuración desde archivo
        config = ConfigLoader.from_file(args.config)
        
        # Validar que tenga path
        if "path" not in config:
            print("❌ Error: La configuración debe incluir 'path'")
            sys.exit(1)
        
        # Verificar si se sobrescriben valores con argumentos CLI
        if args.path:
            config["path"] = args.path
            print("⚠️  Nota: --path sobrescribe el valor del archivo de configuración")
        
        if args.execute:
            config["dry_run"] = False
            print("⚠️  Nota: --execute sobrescribe 'dry_run'")
        
        # Llamar a renamer con configuración
        _run_with_config(config)
        return
    
    # 3. Uso original (solo argumentos CLI)
    # Validaciones originales
    if not args.path:
        print("❌ Error: Se requiere --path o --config")
        parser.print_help()
        return
    
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
    
    # Crear configuración desde argumentos CLI
    config = ConfigLoader.from_cli_args(args)
    config["path"] = str(folder_path)
    
    # Asegurarse de copiar flags importantes a config
    config["recursive"] = getattr(args, "recursive", config.get("recursive", False))
    config["global_index"] = getattr(args, "global_index", config.get("global_index", False))
    config["start_index"] = getattr(args, "start_index", config.get("start_index", 1))
    config["dry_run"] = not getattr(args, "execute", not config.get("dry_run", True))

    _run_with_config(config)


def _run_with_config(config: dict):
    """Función auxiliar para ejecutar con configuración."""
    rules_config = config.get("rules", {})

    effective_prefix = rules_config.get(
    "prefix",
    config.get("prefix", "file")
    )

    print(f"\n🎯 CONFIGURACIÓN:")
    print(f"   Ruta: {config.get('path')}")
    print(f"   Prefijo: {effective_prefix}")
    print(f"   Índice inicio: {config.get('start_index', 1)}")
    print(f"   Recursivo: {'Sí' if config.get('recursive') else 'No'}")
    if config.get('recursive'):
        print(f"   Índice global: {'Sí' if config.get('global_index') else 'No'}")
    print(f"   Modo: {'Dry-run' if config.get('dry_run', True) else 'Ejecución real'}")
    print("-" * 40)
    
    
    # Llamar a la función existente rename_files con los nuevos parámetros
    rename_files(
        folder_path=config["path"],
        prefix=effective_prefix,
        dry_run=config.get("dry_run", True),
        rules_config=config.get("rules", {}),
        start_index=config.get("start_index", 1),
        recursive=config.get("recursive", False),
        global_index=config.get("global_index", False)
    )

if __name__ == "__main__":
    main()