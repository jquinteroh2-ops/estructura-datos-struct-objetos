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

## ¿Qué hace el proyecto?

| Parte | Archivos | Qué muestra |
|---|---|---|
| **3. Struct / Record** | `python/structs.py`, `js/structs.js` | Declaración de un registro con nombre, edad y promedio; 3 instancias guardadas en un arreglo; recorrido; cambio del promedio de un estudiante. En Python con `@dataclass` (struct) y `NamedTuple` (record); en JavaScript con un objeto literal creado por una *factory function* (struct) y `Object.freeze` (record). |
| **4. Objetos** | `python/objetos.py`, `js/objetos.js` | Clase `Estudiante` con promedio privado y los métodos `mostrarInfo()` y `setPromedio()` (que valida la escala 0.0–5.0); 3 instancias en un arreglo; recorrido llamando a `mostrarInfo()`. |
| **5. Struct/Record vs Objeto** | `python/comparativa.py`, `js/comparativa.js`, `js/tipado-estatico.ts` | El mismo `Estudiante` resuelto como struct, record y objeto en un solo archivo: mutabilidad, validación, igualdad, tipado y memoria. Ejemplo de tipado estático con TypeScript. |
| **Actividad práctica** | `inventario-adaptado/` | Adaptación a Python del ejercicio de inventario (Java puro, arquitectura hexagonal): productos, proveedores, clientes, compras y ventas guardados en arreglos de tamaño fijo como structs, records y objetos. |
| **Mini-proyecto integrador** | `mini-proyecto/` | Arreglo de objetos `Producto` con una matriz de ventas por mes y sucursal, en Python y JavaScript. |

La explicación, las tablas comparativas y las diferencias entre lenguajes están en
[`docs/comparativa-struct-vs-objeto.md`](docs/comparativa-struct-vs-objeto.md). La decisión de
modelar cada clase del inventario como struct, record u objeto está en
[`inventario-adaptado/README.md`](inventario-adaptado/README.md).

## Requisitos

- **Python 3.9** o superior.
- **Node.js 18** o superior (22.18 o superior solo para ejecutar el ejemplo `.ts`).
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

### Mini-proyecto integrador

```bash
python mini-proyecto/ventas_sucursales.py    # arreglo de objetos con una matriz de ventas (Python)
node mini-proyecto/ventas_sucursales.js      # la misma solución en JavaScript
```

## Estructura de carpetas

```
/python/
  structs.py                    -> struct (@dataclass) y record (NamedTuple)
  objetos.py                    -> clase Estudiante con mostrarInfo() y setPromedio()
  comparativa.py                -> el mismo Estudiante como struct, record y objeto
/js/
  structs.js                    -> struct (objeto literal) y record (Object.freeze)
  objetos.js                    -> clase Estudiante con mostrarInfo() y setPromedio()
  comparativa.js                -> el mismo Estudiante como struct, record y objeto
  tipado-estatico.ts            -> ejemplo en un lenguaje de tipado estático (TypeScript)
/inventario-adaptado/           -> actividad práctica: inventario con arquitectura hexagonal
  main.py                       -> punto de entrada (menú o demostración)
  dominio/                      -> Producto, Proveedor, Cliente, Compra, Venta y sus detalles
  puertos/                      -> interfaces de entrada y salida
  aplicacion/                   -> casos de uso (ServicioInventario)
  adaptadores/                  -> consola, demostración y BaseDatos con arreglos
  README.md                     -> decisión struct/record/objeto de cada clase
/mini-proyecto/
  ventas_sucursales.py          -> arreglo de objetos con una matriz de ventas (Python)
  ventas_sucursales.js          -> la misma solución en JavaScript
/docs/
  comparativa-struct-vs-objeto.md   -> tablas comparativas y diferencias entre lenguajes
README.md
```

## Flujo de trabajo con Git

Cada bloque se desarrolló en su propia rama, con un commit por cada punto del enunciado, y se
integró a `main` con un merge:

```bash
git switch main
git pull
git switch -c rama-<bloque>
# ... commits del bloque ...
git status
git add .
git commit -m "feat(<bloque>): mensaje"
git push origin rama-<bloque>
git switch main
git pull
git merge rama-<bloque>
git push origin main
```

| Rama | Contenido |
|---|---|
| `rama-struct-python` | `python/structs.py` y comparativa de struct/record en Python |
| `rama-struct-js` | `js/structs.js` y comparativa de struct/record Python vs JavaScript |
| `rama-objetos-python` | `python/objetos.py` y explicación de clases e instancias en Python |
| `rama-objetos-js` | `js/objetos.js`, comparativa de objetos y diferencia entre clase y struct |
| `rama-comparativa` | `comparativa.py`, `comparativa.js`, `tipado-estatico.ts` y la tabla comparativa |
| `rama-inventario-adaptado` | Inventario adaptado a Python con structs, records y objetos |
| `rama-mini-proyecto` | Mini-proyecto integrador en Python y JavaScript |
| `rama-documentacion` | README final |

Para ver el historial con las ramas y sus merges:

```bash
git log --oneline --graph --all
```
