from pathlib import Path

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

def resolve_rules_for_file(filename: str, rules_config: dict) -> dict:
    """
    Resolve the renaming rules for a given file based on its extension.

    Priority:
    1. rules.by_type (first matching rule)
    2. rules.default
    """
        
    # Regla por defecto (fallback)
    default_rule = rules_config.get("default", {})

    # Extensión normalizada
    extension = Path(filename).suffix.lower()

    # Reglas por tipo
    by_type = rules_config.get("by_type", {})

    for _, rule in by_type.items():
        extensions = rule.get("extensions", [])
        if extension in extensions:
            # Merge simple: rule overrides default
            resolved_rule = default_rule.copy()
            resolved_rule.update(rule)
            return resolved_rule

    # Si no matchea ninguna regla específica
    return default_rule.copy()
