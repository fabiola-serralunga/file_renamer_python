#!/bin/bash
# full_stats.sh - Estadísticas completas por versión
# Ubicación: file_renamer_python/stats/full_stats.sh

echo "📊 FILE RENAMER PYTHON - ESTADÍSTICAS COMPLETAS"
echo "========================================"
echo ""

# Verificar ubicación
if [ ! -d "app" ]; then
    echo "❌ ERROR: Ejecuta desde la raíz del proyecto"
    echo "   Actual: $(pwd)"
    exit 1
fi

# Archivo para resultados
RESULTS="stats/version_comparison.csv"
echo "Versión,Líneas,Archivos,Args_CLI,Ejemplos,Fecha" > $RESULTS

echo "🔍 ANALIZANDO CADA VERSIÓN..."
echo ""

# Obtener todas las tags
TAGS=$(git tag --sort=version:refname)

if [ -z "$TAGS" ]; then
    echo "⚠️  No hay tags disponibles"
    echo "   Crea tags con: git tag v1.0.0, etc."
    exit 0
fi

# Guardar estado actual
CURRENT_BRANCH=$(git branch --show-current 2>/dev/null || echo "main")

for TAG in $TAGS; do
    echo "📌 $TAG..."
    
    # Cambiar a la tag
    git checkout $TAG 2>/dev/null
    
    if [ $? -eq 0 ]; then
        # 1. CONTAR LÍNEAS
        LINES=$(find app -name "*.py" -type f -exec cat {} + 2>/dev/null | wc -l)
        
        # 2. CONTAR ARCHIVOS PYTHON
        FILES=$(find app -name "*.py" -type f 2>/dev/null | wc -l)
        
        # 3. CONTAR ARGUMENTOS CLI
        if [ -f "app/main.py" ]; then
            ARGS=$(grep -c "parser.add_argument" app/main.py 2>/dev/null || echo "0")
        else
            ARGS="0"
        fi
        
        # 4. CONTAR CARPETAS DE EJEMPLO
        if [ -d "examples" ]; then
            EXAMPLES=$(find examples -type d -mindepth 1 -maxdepth 1 2>/dev/null | wc -l)
        else
            EXAMPLES="0"
        fi
        
        # 5. FECHA DEL COMMIT
        DATE=$(git log -1 --format=%cd --date=short 2>/dev/null)
        
        # Guardar en CSV
        echo "$TAG,$LINES,$FILES,$ARGS,$EXAMPLES,$DATE" >> $RESULTS
        
        # Mostrar en pantalla
        echo "   ✓ Líneas: $LINES"
        echo "   ✓ Archivos: $FILES"
        echo "   ✓ Args CLI: $ARGS"
        echo "   ✓ Ejemplos: $EXAMPLES"
        echo "   ✓ Fecha: $DATE"
    else
        echo "   ❌ No se pudo cambiar a $TAG"
    fi
    
    echo ""
done

# Volver al estado original
git checkout $CURRENT_BRANCH 2>/dev/null
echo "✅ De vuelta en: $CURRENT_BRANCH"

echo ""
echo "📈 TABLA RESUMEN:"
echo "================="
column -t -s "," $RESULTS

echo ""
echo "📊 GRÁFICO ASCII:"
echo "================="

# Gráfico de líneas
echo "LÍNEAS DE CÓDIGO:"
cat $RESULTS | tail -n +2 | while IFS=, read TAG LINES FILES ARGS EXAMPLES DATE; do
    BAR=$(printf "%0.s▇" $(seq 1 $((LINES/50))))
    printf "%-8s %5d %s\n" "$TAG" "$LINES" "$BAR"
done

echo ""
echo "📁 ARCHIVOS PYTHON:"
cat $RESULTS | tail -n +2 | while IFS=, read TAG LINES FILES ARGS EXAMPLES DATE; do
    BAR=$(printf "%0.s▇" $(seq 1 $((FILES*5))))
    printf "%-8s %2d %s\n" "$TAG" "$FILES" "$BAR"
done

echo ""
echo "⚙️  ARGUMENTOS CLI:"
cat $RESULTS | tail -n +2 | while IFS=, read TAG LINES FILES ARGS EXAMPLES DATE; do
    BAR=$(printf "%0.s▇" $(seq 1 $((ARGS*3))))
    printf "%-8s %2d %s\n" "$TAG" "$ARGS" "$BAR"
done

echo ""
echo "💾 Resultados guardados en: $RESULTS"
echo "📋 Copia esta tabla para tu README.md"