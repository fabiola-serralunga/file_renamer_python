# File Renamer Python

Herramienta en Python para **renombrar archivos de forma segura y controlada**, desarrollada como **proyecto de portfolio** enfocado en automatización y buenas prácticas de backend.

El proyecto implementa una **interfaz de línea de comandos (CLI)** basada en `argparse`, con modo seguro (*dry-run*) por defecto y un punto de entrada claro mediante ejecución como módulo.

---

## 🎯 Objetivo

Renombrar archivos dentro de una carpeta:
- normalizando los nombres (minúsculas, guiones bajos, limpieza básica)
- agregando un prefijo configurable
- agregando numeración incremental
- evitando cambios accidentales mediante **modo dry-run**

---

## 🧱 Estructura del proyecto

```
file_renamer_python/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── renamer.py
│   └── rules.py
├── examples/
│   ├── test_files/
│   └── test_vacia/
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

---

## 🧠 Diseño y decisiones técnicas

- **CLI explícito y predecible**: el programa se ejecuta como módulo (`python -m app.main`), evitando dependencias del directorio actual.
- **Separación de responsabilidades**: cada archivo cumple una función específica (orquestación, lógica principal, reglas).
- **Dry-run por defecto**: decisión de seguridad para evitar modificaciones accidentales.
- **Diseño modular**: facilita mantenimiento y extensión futura.

---

## 📁 Responsabilidades por módulo

- **main.py**  
  Punto de entrada del CLI. Define y parsea argumentos (`--path`, `--prefix`, `--execute`) y orquesta la ejecución.

- **renamer.py**  
  Lógica principal: recorre archivos, aplica reglas, gestiona numeración y ejecuta (o simula) el renombrado.

- **rules.py**  
  Contiene únicamente las reglas de normalización de nombres. No interactúa con el sistema de archivos.

---

## ▶️ Uso

Desde la **raíz del proyecto**:

```bash
python -m app.main --path examples/test_files
```

Por defecto el programa corre en **modo dry-run**, mostrando qué cambios se realizarían sin modificar los archivos.

Ejemplo de salida:

```
[DRY-RUN] archivo.txt → file_archivo_001.txt
```

### Ejecución real

Para aplicar los cambios:

```bash
python -m app.main --path examples/test_files --execute
```
### Numeración desde índice específico
python -m app.main --path examples/test_files --start-index 10

--start-index permite iniciar la numeración desde cualquier valor. Por defecto empieza en 1.

Ejemplo de salida con --start-index 10

```
[DRY-RUN] control-bucles Python.txt → file_control_bucles_python_010.txt
[DRY-RUN] Archivo previamente normalizado: file_control_bucles_python_002.txt → file_file_control_bucles_python_002_011.txt
[DRY-RUN] Precedencia-Python.txt → file_precedencia_python_012.txt
```

### Carpeta vacía

Si la carpeta indicada no contiene archivos (por ejemplo `examples/test_vacia`), el programa detecta automáticamente la situación, informa al usuario y no realiza ninguna acción.

```bash
python -m app.main --path examples/test_vacia
```

Salida esperada:

```
[INFO] No hay archivos para renombrar en: examples/test_vacia
```

### Archivos previamente formateados

Ahora todos los archivos se normalizan, incluso si ya tienen un formato similar. Dry-run muestra un mensaje informativo:

[DRY-RUN] Archivo previamente normalizado: file_control_bucles_python_002.txt → file_file_control_bucles_python_002_002.txt

[SKIP] fue eliminado; todos los archivos se procesan.

La numeración es continua y coherente con --start-index.

---

## 🔐 Modo seguro (dry-run)

- El programa **no modifica archivos por defecto**.
- La ejecución real requiere confirmación explícita mediante `--execute`.

---

## 📌 Requisitos

- Python 3.10 o superior
- No requiere dependencias externas

---

## 🚧 Futuras mejoras

- Procesamiento recursivo de subcarpetas
- Configuración externa de reglas (JSON / YAML)
- Modo undo (rollback)
- Publicación como paquete pip

---

## 🧩 Estado del proyecto

✔ Versión 2.0.1 – CLI funcional y documentado  
✔ Diseño modular y seguro  
✔ Proyecto preparado para portfolio

---

## 👤 Autor

Proyecto desarrollado como parte de un proceso de formación y construcción de portfolio en Python.

## 📄 Licencia

Este proyecto está licenciado bajo la licencia MIT. Ver el archivo `LICENSE` para más información.

