# File Renamer Python

Herramienta en Python para **renombrar archivos de forma segura y controlada**, desarrollada como **proyecto de portfolio** enfocado en automatización y buenas prácticas de backend, aplicando reglas de normalización y numeración automática.

El proyecto está pensado como una utilidad simple pero profesional, orientada a automatización y buenas prácticas (diseño modular, dry-run por defecto, documentación clara).

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
├── README.md
├── requirements.txt
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── renamer.py
│   └── rules.py
└── examples/
    └── test_files/
```

---

## 🧠 Decisiones de diseño

- **Separación de responsabilidades**: cada archivo cumple una función específica (orquestación, lógica principal, reglas), lo que mejora legibilidad y mantenibilidad.
- **Dry-run por defecto**: decisión de seguridad para evitar modificaciones accidentales en archivos reales.
- **Diseño modular**: facilita testeo y extensión futura sin reescribir el núcleo del programa.

---

## 🧠 Diseño y responsabilidades

El proyecto está dividido por responsabilidades claras:

- **main.py**  
  Punto de entrada. Orquesta la ejecución y define parámetros (carpeta, prefijo, dry-run).

- **renamer.py**  
  Lógica principal: recorre archivos, construye nuevos nombres y ejecuta (o simula) el renombrado.

- **rules.py**  
  Contiene únicamente las reglas de normalización de nombres. No interactúa con el sistema de archivos.

Este diseño facilita mantenimiento, testeo y extensión futura.

---

## ▶️ Uso

Desde la raíz del proyecto:

```bash
python app/main.py
```

Por defecto el programa corre en **modo dry-run**, mostrando qué cambios se realizarían sin modificar los archivos.

Ejemplo de salida:

```
control-bucles Python.txt → doc_control_bucles_python_001.txt
Precedencia-Python.txt   → doc_precedencia_python_002.txt
```

---

## 🔐 Modo seguro (dry-run)

El proyecto prioriza la seguridad:
- No se renombran archivos accidentalmente
- El usuario puede revisar la salida antes de ejecutar cambios reales

La ejecución real se habilita explícitamente mediante un flag interno (`dry_run=False`).

---

## 📌 Requisitos

- Python 3.10 o superior
- No requiere dependencias externas

---

## 🚧 Futuras mejoras

Este proyecto está intencionalmente limitado a un alcance simple.
En versiones futuras podría incorporar:

- Interfaz de línea de comandos (CLI) con argumentos (`--execute`, `--prefix`, `--path`)
- Reglas configurables por archivo (JSON / YAML)
- Modo undo (rollback)
- Publicación como paquete pip
- Interfaz gráfica simple

Estas mejoras no se incluyen en esta versión para mantener claridad y foco.

---

## 🧩 Estado del proyecto

✔ Versión estable – funcional  
✔ Proyecto cerrado para portfolio  
✔ Enfoque en claridad, seguridad y buenas prácticas

---

## 👤 Autor

Proyecto desarrollado como parte de un proceso de formación y construcción de portfolio en Python.

