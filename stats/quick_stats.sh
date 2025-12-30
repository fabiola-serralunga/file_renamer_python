#!/bin/bash
# quick_stats.sh - Estadísticas rápidas desde VS Code
# Ubicación: file_renamer_python/stats/quick_stats.sh

echo "📊 FILE RENAMER PYTHON - ESTADÍSTICAS RÁPIDAS"
echo "======================================"
echo ""

# Verificar que estamos en el lugar correcto
if [ ! -d "app" ]; then
    echo "❌ ERROR: No estás en la raíz del proyecto"
    echo "   Ejecuta desde: file_renamer_python/"
    echo "   Actual: $(pwd)"
    exit 1
fi

# Versión actual primero
echo "🔍 VERSIÓN ACTUAL (main/HEAD):"
if [ -d "app" ]; then
    lines=$(find app -name "*.py" -type f -exec cat {} + 2>/dev/null | wc -l)
    files=$(find app -name "*.py" -type f 2>/dev/null | wc -l)
    echo "   • Líneas Python: $lines"
    echo "   • Archivos Python: $files"
    
    # Argumentos CLI
    if [ -f "app/main.py" ]; then
        args=$(grep -c "parser.add_argument" app/main.py 2>/dev/null || echo "0")
        echo "   • Argumentos CLI: $args"
    fi
else
    echo "   • No hay carpeta 'app'"
fi
echo ""

# Carpetas de ejemplo
echo "🧪 CARPETAS DE EJEMPLO:"
if [ -d "examples" ]; then
    examples=$(find examples -type d -mindepth 1 -maxdepth 1 | wc -l)
    echo "   • Cantidad: $examples"
    echo "   • Lista:"
    find examples -type d -mindepth 1 -maxdepth 1 | sed 's/^/     - /'
else
    echo "   • No hay carpeta 'examples'"
fi
echo ""

# Tags disponibles
echo "🏷️  VERSIONES DISPONIBLES (git tags):"
tags=$(git tag --sort=-version:refname 2>/dev/null)
if [ -n "$tags" ]; then
    echo "$tags" | sed 's/^/   • /'
    
    echo ""
    echo "📈 COMPARATIVA VERSIÓN vs LÍNEAS:"
    echo "   (esto tomará unos segundos...)"
    echo ""
    
    for tag in $tags; do
        # Solo mostrar las principales para no demorar
        if [[ "$tag" =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
            git checkout $tag 2>/dev/null
            if [ $? -eq 0 ]; then
                tag_lines=$(find app -name "*.py" -type f -exec cat {} + 2>/dev/null | wc -l)
                printf "   • %-10s: %4d líneas\n" "$tag" "$tag_lines"
            fi
        fi
    done
    
    # Volver a main
    git checkout main 2>/dev/null
    echo ""
    echo "   ✅ Volviendo a versión main..."
else
    echo "   • No hay tags disponibles"
fi

echo ""
echo "💡 USO:"
echo "   ./stats/quick_stats.sh        # Estas estadísticas"
echo "   git checkout v1.0.0           # Cambiar a versión específica"
echo "   git checkout main             # Volver a la última"