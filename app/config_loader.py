
"""
Carga configuración desde archivos YAML/JSON.
Versión mínima para Fase A.
"""
import json
import yaml
from pathlib import Path
from typing import Dict, Any
import sys


class ConfigLoader:
    """Carga y valida configuraciones."""
    
    # Configuración por defecto (versión simple para empezar)
    DEFAULT_CONFIG = {
        "prefix": "file",
        "start_index": 1,
        "recursive": False,
        "global_index": False,
        "dry_run": True,
    }
    
    @classmethod
    def from_file(cls, config_path: str) -> Dict[str, Any]:
        """
        Carga configuración desde archivo.
        """
        path = Path(config_path).resolve()
        
        if not path.exists():
            print(f"❌ Error: Archivo no encontrado: {config_path}")
            sys.exit(1)
        
        # Cargar según formato
        if path.suffix.lower() in ['.yaml', '.yml']:
            config_data = cls._load_yaml(path)
        elif path.suffix.lower() == '.json':
            config_data = cls._load_json(path)
        else:
            print(f"❌ Error: Formato no soportado: {path.suffix}")
            sys.exit(1)
        
        # Combinar con defaults
        merged = cls.DEFAULT_CONFIG.copy()
        merged.update(config_data)
        
        return merged
    
    @classmethod
    def _load_yaml(cls, path: Path) -> Dict[str, Any]:
        """Carga YAML."""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f) or {}
        except yaml.YAMLError as e:
            print(f"❌ Error YAML: {e}")
            sys.exit(1)
    
    @classmethod
    def _load_json(cls, path: Path) -> Dict[str, Any]:
        """Carga JSON."""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"❌ Error JSON: {e}")
            sys.exit(1)
    
    @classmethod
    def from_cli_args(cls, args) -> Dict[str, Any]:
        """
        Crea configuración desde argumentos CLI.
        """
        config = cls.DEFAULT_CONFIG.copy()
        
        # Mapear argumentos (solo los básicos por ahora)
        if hasattr(args, 'path') and args.path:
            config['path'] = args.path
        
        if hasattr(args, 'prefix'):
            config['prefix'] = args.prefix
        
        if hasattr(args, 'start_index'):
            config['start_index'] = args.start_index
        
        if hasattr(args, 'recursive'):
            config['recursive'] = args.recursive
        
        if hasattr(args, 'global_index'):
            config['global_index'] = args.global_index
        
        if hasattr(args, 'execute'):
            config['dry_run'] = not args.execute
        
        return config
    
    @classmethod
    def create_template(cls, format: str = "yaml") -> str:
        """Crea plantilla simple."""
        template = {
            "path": "./ruta/a/tu/carpeta",
            "execute": False,
            "prefix": "document",
            "start_index": 1,
            "recursive": False,
            "global_index": False,
        }
        
        if format.lower() == "yaml":
            import yaml
            return yaml.dump(template, default_flow_style=False, allow_unicode=True)
        else:
            import json
            return json.dumps(template, indent=2, ensure_ascii=False)