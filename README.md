# Estructura de Datos — Struct/Record y Objetos

Actividad de aprendizaje individual de la Unidad 1 de la asignatura **Estructura de Datos**.
Implementación de **structs/records** y **objetos (clases e instancias)** en **Python** y
**JavaScript**, con una comparativa entre ambos modelos y la adaptación de un ejercicio de
inventario que usa structs, records y objetos como elementos guardados en arreglos.

## Autor

- **Nombre:** Jose Antonio Quintero Herrera
- **Código:** 7502510055
- **Programa:** Ingeniería de Software — Universidad de Cartagena
- **Asignatura:** Estructura de Datos

## Requisitos

- **Python 3.9** o superior.
- **Node.js 18** o superior.
- No se necesita instalar dependencias: solo se usa la librería estándar de cada lenguaje.

## Cómo ejecutar

Desde la raíz del repositorio:

### Struct / Record

```bash
python python/structs.py         # struct (@dataclass) y record (NamedTuple) en Python
node js/structs.js               # struct (objeto literal) y record (Object.freeze) en JavaScript
```

### Objetos (clases e instancias)

```bash
python python/objetos.py         # clase Estudiante con mostrarInfo() y setPromedio() en Python
node js/objetos.js               # clase Estudiante con mostrarInfo() y setPromedio() en JavaScript
```

### Comparativa struct/record vs objeto

```bash
python python/comparativa.py     # el mismo Estudiante como struct, record y objeto en Python
node js/comparativa.js           # el mismo Estudiante como struct, record y objeto en JavaScript
node js/tipado-estatico.ts       # ejemplo de tipado estático con TypeScript (Node.js 22.18 o superior)
```

### Inventario adaptado (actividad práctica)

```bash
python inventario-adaptado/main.py --demo    # demostración automática, sin escribir nada
python inventario-adaptado/main.py           # menú interactivo con datos de ejemplo
```
