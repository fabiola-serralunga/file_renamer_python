# File Renamer Python

Herramienta en Python para renombrar archivos de forma segura, controlada y predecible, orientada a automatización y buenas prácticas de backend.

A partir de la versión 3.0.0, el proyecto incorpora procesamiento recursivo completo para renombrar archivos en árboles de directorios.

Desde la versión 4.0.0, admite configuración externa mediante archivos JSON y YAML, manteniendo compatibilidad total con el uso por línea de comandos.

---

## Tabla de Contenidos

- [🎯 Objetivo](#-objetivo)
- [🧱 Estructura del proyecto](#-estructura-del-proyecto)
- [🧠 Diseño y decisiones técnicas](#-diseño-y-decisiones-técnicas)
- [🆕 Configuración externa (v4.0.0)](#-configuraci%C3%B3n-externa-v400)
- [📁 Responsabilidades por módulo](#-responsabilidades-por-m%C3%B3dulo)
- [▶️ Uso](#-uso)
- [🚀 Ejecución real](#-ejecución-real)
- [🔢 Control de numeración](#-control-de-numeración)
- [🌳 Procesamiento recursivo](#-procesamiento-recursivo)
- [🧪 Ejemplos complejos y edge cases](#-ejemplos-complejos-y-edge-cases)
- [📂 Carpetas vacías](#-carpetas-vacías)
- [🔐 Modo seguro (dry-run)](#-modo-seguro-(dry-run))
- [📌 Requisitos](#-requisitos)
- [🧩 Estado del proyecto](#-estado-del-proyecto)
- [📊 Evolución y Métricas](#-evolución-y-métricas)
- [🚧 Posibles mejoras futuras](#-posibles-mejoras-futuras)
- [👤 Autor](#-autor)
- [📄 Licencia](#-licencia)

---

## 🎯 Objetivo

Renombrar archivos de forma consistente:

- Normalización de nombres (minúsculas, snake_case básico)
- Prefijo configurable
- Numeración incremental con padding
- Modo seguro (*dry-run*) por defecto
- Procesamiento recursivo de subcarpetas
- Control explícito de la numeración (por carpeta o global)

---

## 🧱 Estructura del proyecto

```
file_renamer_python/
├── app/
│   ├── __init__.py
│   ├── config_loader.py # Carga de JSON / YAML
│   ├── main.py          # CLI y validación de argumentos
│   ├── renamer.py       # Lógica de renombrado y recorrido de carpetas
│   └── rules.py         # Reglas de normalización de nombres
├── config/
│   ├── basic_v4.json
│   ├── basic_v4.json
│   ├── renamer.json
│   └── renamer.yaml
├── examples/
│   ├── test_docs_yaml/
│   ├── test_images_json/
│   │   ├── test_images_francia/
│   │   ├── test_images_italia/  
│   │   └── test_images_rusia/
│   ├── test_files/
│   ├── test_mixed/
│   ├── test_recursiva/
│   │   ├── recursiva_docs/
│   │   │   └── otros_docs/
│   │   └── recursiva_imagen/        
│   └── test_vacia/
│   └── stats/
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
└── stats
```

---

## 🧠 Diseño y decisiones técnicas

- **CLI explícito y predecible**: ejecución como módulo (`python -m app.main`).
- **Separación de responsabilidades**: CLI, lógica de recorrido y reglas desacopladas.
- **Dry-run por defecto**: evita modificaciones accidentales.
- **Recorrido con `pathlib`**: manejo robusto de rutas y compatibilidad multiplataforma.
- **Orden determinista**: archivos ordenados para garantizar resultados reproducibles.

---

## 🆕 Configuración externa (v4.0.0)

A partir de la versión **4.0.0**, el proyecto incorpora **configuración externa mediante archivos JSON o YAML**, manteniendo compatibilidad total con el uso por CLI.

Esta configuración permite definir de forma declarativa:

- Ruta de trabajo (`path`)
- Modo seguro (`dry_run`)
- Reglas de renombrado (`rules`)

El motor interno no distingue entre JSON o YAML: ambos formatos se cargan y normalizan como un diccionario Python antes de la ejecución.

### Ejemplo de configuración mínima (JSON)

```json
{
  "path": "./examples/test_images_json/test_images_rusia",
  "dry_run": true,
  "rules": {
    "prefix": "rusia_2025",
    "start_index": 1,
    "padding": 3
  }
}
```

### Ejemplo equivalente (YAML)

```yaml
path: ./examples/test_docs_yaml/
dry_run: true

rules:
  prefix: doc
  start_index: 1
  padding: 3
```

### Ejecución con archivo de configuración

python -m app.main --config config/test_renamer.json

ó 

python -m app.main --config config/test_renamer.yaml

### Precedencia de configuración

Los valores definidos en el archivo de configuración son la fuente principal.

Algunos argumentos CLI (--path, --execute) pueden sobrescribir valores del archivo.

El comportamiento por defecto sigue siendo dry-run seguro.

Esta incorporación sienta las bases para futuros flujos más complejos sin acoplar lógica de dominio al renombrador.

---


## 📁 Responsabilidades por módulo

### `main.py`

- Punto de entrada del CLI.
- Define y valida argumentos.
- Controla combinaciones inválidas (por ejemplo `--global-index` sin `--recursive`).
- Orquesta la ejecución.

### `renamer.py`

- Recolecta archivos (modo simple o recursivo).
- Implementa tres modos de procesamiento:
  - Carpeta única
  - Recursivo con numeración por carpeta
  - Recursivo con numeración global
- Gestiona mensajes informativos, carpetas vacías y dry-run.

### `rules.py`

- Contiene exclusivamente reglas de normalización de nombres.
- No interactúa con el sistema de archivos.

---

## ▶️ Uso

A continuación se muestran ejemplos simples. Más abajo se incluyen **escenarios complejos y edge cases** documentados a partir de la versión 3.0.0.



Desde la raíz del proyecto:

```
python -m app.main --path <ruta>
```

Por defecto el programa se ejecuta en **modo dry-run**.

Ejemplo:

```
python -m app.main --path examples/test_files
```

Salida esperada:

```
[DRY-RUN] control-bucles Python.txt → file_control_bucles_python_001.txt
[DRY-RUN] Archivo previamente normalizado: file_control_bucles_python_002.txt → file_file_control_bucles_python_002_002.txt
[DRY-RUN] Precedencia-Python.txt → file_precedencia_python_003.txt

```

---

## 🚀 Ejecución real

Para aplicar los cambios:

```
python -m app.main --path examples/test_files --execute
```

---

## 🔢 Control de numeración

### Inicio personalizado

```
python -m app.main --path examples/test_files --start-index 10
```

---

## 🌳 Procesamiento recursivo

El procesamiento recursivo permite trabajar sobre **árboles completos de directorios**, manteniendo un comportamiento determinista y explícito.



### Recursivo con numeración por carpeta

Reinicia la numeración en cada carpeta:

```
python -m app.main --path examples --recursive
```

Salida:

```
[PROCESANDO] Carpeta: test_recursiva/
  [DRY-RUN] recursiva raiz.txt → file_recursiva_raiz_001.txt
```

Las carpetas vacías se detectan y se informan.

Salida:

```
[INFO] 3 carpeta(s) vacía(s) encontrada(s):
  • ./
  • test_recursiva/recursiva_docs/otros_docs/
  • test_vacia/
```
---

### Recursivo con numeración global

Numeración continua a lo largo de todo el árbol:

```
python -m app.main --path examples --recursive --global-index
```

Salida:

```
[DRY-RUN] test_files/Precedencia-Python.txt → file_precedencia_python_003.txt
[DRY-RUN] test_recursiva/recursiva raiz.txt → file_recursiva_raiz_004.txt
```

> `--global-index` solo es válido junto con `--recursive`.

---

## 🧪 Ejemplos complejos y edge cases

### Árbol de directorios mixto

Estructura de ejemplo:

```
examples
    ├───test_docs_yaml
    ├───test_images_json
    │   ├──test_images_francia    
    │   ├──test_images_italia    
    │   └──test_images_rusia
    │         image_001.png    
    │         image_002.png    
    │         image_003.jpg
    │         [...gif, bmp]   
    ├───test_files
    │       control-bucles Python.txt
    │       file_control_bucles_python_002.txt
    │       Precedencia-Python.txt
    │
    ├───test_mixed
    │   │   borrador Apartado cortisol.txt
    │   │   image_001.gif
    │   │   image-002.png
    │   │   [...]
    │
    ├───test_recursiva
    │   │   recursiva raiz.txt
    │   │
    │   ├───recursiva_docs
    │   │   │   Historical Meta-PEPs and Informatio.txt
    │   │   │   Python-PEP8.pdf
    │   │   │
    │   │   └───otros_docs
    │   └───recursiva_imagen
    │           PEP8.PYTHON.jpg
    │           reservedPEP Numbers.jpg
    │
    └───test_vacia
```

---

### Edge case: archivos previamente normalizados

Los archivos que ya cumplen el patrón esperado **no se omiten**. Se vuelven a procesar para garantizar coherencia global:

```
 [DRY-RUN] test_files/file_control_bucles_python_002.txt (normalizado) → file_file_control_bucles_python_002_002.txt
```

Esto evita estados híbridos dentro de una misma carpeta o árbol.

---

### Edge case: extensiones múltiples

Archivos con múltiples puntos conservan la extensión completa:

```
[DRY-RUN] test_recursiva/recursiva_imagen/PEP8.PYTHON.jpg → file_pep8.python_007.jpg
```

---

### Edge case: mezcla de mayúsculas, espacios y guiones

```
[DRY-RUN] test_recursiva/recursiva_docs/Historical Meta-PEPs and Informatio.txt → file_historical_meta_peps_and_informatio_005.txt
```

---

### Edge case: carpetas vacías en modo recursivo

- Las carpetas vacías **no generan errores**.
- Se detectan automáticamente.
- En dry-run se listan al final como información adicional.
- Algunas carpetas vacías se preservan mediante .gitkeep con fines de prueba.

Ejemplo:

```
[INFO] 3 carpeta(s) vacía(s) encontrada(s):
  • ./
  • test_recursiva/recursiva_docs/otros_docs/
  • test_vacia/
```

---

### Comparación de modos de numeración

#### Numeración por carpeta

```
python -m app.main --path examples --recursive
```

Resultado esperado:

- `test_files/` comienza en 001
- `test_recursiva/` comienza en 001
- `test_recursiva/recursiva_imagen/` comienza en 001

#### Numeración global

```
python -m app.main --path examples --recursive --global-index
```

Resultado esperado:

- Numeración continua a lo largo de todo el árbol, respetando el orden determinista.

---

## 📂 Carpetas vacías

- En modo no recursivo: se informa y no se realiza ninguna acción.
- En modo recursivo:
  - Las carpetas vacías se detectan automáticamente.
  - Se listan al final del dry-run para referencia.

---

## 🔐 Modo seguro (dry-run)

- El programa **no modifica archivos por defecto**.
- La ejecución real requiere `--execute`.
- Todas las acciones se muestran antes de aplicarse.

---

## 📌 Requisitos

- Python **3.10** o superior
- Sin dependencias externas

---

## 🧩 Estado del proyecto

✔ Versión **4.0.0** – Configuración externa JSON / YAML  
✔ Compatibilidad total con uso por CLI  
✔ Reglas declarativas de renombrado  
✔ Procesamiento recursivo completo  
✔ Dry-run seguro por defecto  
✔ Diseño modular y extensible


---
## 📊 Evolución y Métricas

Este proyecto sigue **versionado semántico** y demuestra crecimiento medible a través de sus releases. La evolución técnica es transparente y cuantificable.

### 📈 Métricas por versión 
=================
| Versión | Líneas | Archivos | Args_CLI | Ejemplos | Fecha |
|:---|:---:|:---:|:---:|:---:|:---:|
| v1.0.0 | 050 | 4 | 0 | 2 | 2025-12-18 |
| v2.0.0 | 106 | 4 | 3 | 2 | 2025-12-27 |
| v2.0.1 | 324 | 4 | 6 | 3 | 2025-12-28 |
| v3.0.0 | 324 | 4 | 6 | 3 | 2025-12-28 |
| v4.0.0 | 533 | 5 | 6 | 6 | 2026-01-09 |
*Actualizado al 09/01/2026*

```bash
# Nota: Ejecuta `./stats/full_stats.sh` para métricas exactas.*
./stats/full_stats.sh
```

### 🕰️ Journey Through Versions
Experimenta la evolución en primera persona:

#### 1. Versión estable inicial con renombrador de archivos de prueba (v1.0.0)
git checkout v1.0.0
python -m app.main --help  

#### 2. Versión CLI con casos extremos documentados (v2.0.0)
git checkout v2.0.0  
python -m app.main --help  

#### 3. Versión CLI con opción -start-index para numeración personalizada y función SKIP eliminada (v2.0.1)
git checkout v2.0.1  
python -m app.main --help

#### 4. Versión actual con procesamiento recursivo (v3.0.0)
git checkout v3.0.0  
python -m app.main --help  

#### 5. – Versión actual con soporte para configuración externa en JSON y YAML (v4.0.0)
git checkout main  
python -m app.main --help  

#### 6. Siempre volver a main cuando termines
git checkout main

---

## 🚧 Posibles mejoras futuras

- Reglas avanzadas por tipo de archivo
- Filtros por extensión y patrones
- Modo undo / rollback
- Publicación como paquete pip
- Interfaz gráfica simple

---

## 👤 Autor

Proyecto desarrollado como parte de un proceso de formación y construcción de portfolio en Python.

---

## 📄 Licencia

Este proyecto está licenciado bajo la **MIT License**. Ver el archivo `LICENSE` para más información.

