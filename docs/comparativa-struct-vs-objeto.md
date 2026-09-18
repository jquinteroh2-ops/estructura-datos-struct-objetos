# Comparativa: Struct/Record vs Objetos en Python y JavaScript

Documento de apoyo de la actividad individual de la Unidad 1 de **Estructura de Datos**.
Se va completando bloque a bloque, a medida que se implementa cada parte en el repositorio.

## 1. Struct / Record

Un **struct** (o **registro**) agrupa varios datos relacionados bajo un mismo nombre, cada uno
en un **campo** con nombre propio. Sirve para tratar como una sola unidad datos que siempre van
juntos, por ejemplo el nombre, la edad y el promedio de un estudiante. Un struct **solo guarda
datos**: no tiene comportamiento propio.

Un **record** es un struct **inmutable**: una vez creado no se pueden cambiar sus campos; para
"modificarlo" se crea un registro nuevo con el valor cambiado.

### Python (`python/structs.py`)

Python no tiene la palabra reservada `struct`, pero la librería estándar trae dos formas nativas
de declarar registros:

```python
from dataclasses import dataclass
from typing import NamedTuple

@dataclass
class EstudianteStruct:          # struct mutable
    nombre: str
    edad: int
    promedio: float

class EstudianteRecord(NamedTuple):   # record inmutable
    nombre: str
    edad: int
    promedio: float
```

| Actividad | `@dataclass` (struct) | `NamedTuple` (record) |
|---|---|---|
| Declaración | Clase con anotaciones de tipo; el decorador genera `__init__`, `__repr__` y `__eq__` | Clase que hereda de `NamedTuple`; también genera `__init__` y `__repr__` |
| Inicialización | `EstudianteStruct("Ana Martínez", 19, 4.2)` o por nombre de campo | Igual: `EstudianteRecord(nombre="Luis Pérez", edad=21, promedio=3.6)` |
| Acceso a campos | Por nombre: `est.promedio` | Por nombre (`reg.promedio`), por posición (`reg[2]`) o desempaquetando (`nombre, edad, promedio = reg`) |
| Recorrido | `for i in range(len(estudiantes))` accediendo a `estudiantes[i].nombre` | `for i, (nombre, edad, promedio) in enumerate(registros)` |
| Modificación | Asignación directa: `est.promedio = 4.1` | `reg.promedio = 4.1` lanza `AttributeError`; se crea uno nuevo con `reg._replace(promedio=4.1)` |
| Mutabilidad | Mutable | Inmutable |

**Tipado:** las anotaciones (`nombre: str`, `edad: int`) documentan el tipo de cada campo y las
usan el editor y herramientas como `mypy`, pero **Python no las verifica al ejecutar**: el
tipado sigue siendo dinámico.

**Igualdad por valor:** `@dataclass` genera `__eq__`, así que dos structs con los mismos datos
son iguales (`==`) aunque sean dos instancias distintas en memoria.

### JavaScript (`js/structs.js`)

JavaScript **no tiene struct nativo**. La forma más cercana es un **objeto literal plano**:

```js
// "Struct" (mutable): factory function que devuelve un objeto plano
function crearEstudiante(nombre, edad, promedio) {
  return { nombre, edad, promedio };
}

// "Record" (inmutable): el mismo objeto, congelado
function crearEstudianteRecord(nombre, edad, promedio) {
  return Object.freeze({ nombre, edad, promedio });
}
```

**¿Por qué un objeto literal plano es lo más parecido a un struct en JS?**

- Agrupa datos relacionados en **campos con nombre** (`est.nombre`, `est.promedio`), igual que un struct.
- **No tiene clase ni métodos propios**: solo hereda de `Object.prototype`, así que es "solo datos".
- No hay que declarar un tipo antes de usarlo: la forma del objeto existe en el momento de crearlo.
  Por eso se usa una **factory function**: garantiza que todas las instancias tengan los mismos
  campos, en el mismo orden, sin repetir el literal en cada creación (hace el papel de la
  "declaración" del struct).
- `Object.freeze()` impide agregar, borrar o cambiar campos, lo que lo convierte en un **record**.
  En modo estricto (`'use strict'`) intentar cambiar un campo lanza `TypeError`; sin modo estricto
  la asignación se ignora en silencio, sin avisar.

### Diferencias de implementación Python vs JavaScript (struct/record)

| Aspecto | Python | JavaScript |
|---|---|---|
| ¿Struct nativo? | Sí, en la librería estándar: `@dataclass` y `NamedTuple` | No; se usa un objeto literal plano `{ ... }` |
| Declaración del tipo | Clase con campos anotados (`nombre: str`) | No existe; la factory function define la forma del objeto |
| Tipos de los campos | `str`, `int`, `float` (anotados, no verificados al ejecutar) | `string`, `number`, `number` (no distingue enteros de decimales) |
| Inicialización | Por posición o por nombre: `EstudianteStruct(nombre="Luis Pérez", ...)` | `crearEstudiante("Luis Pérez", 21, 3.6)` o el literal `{ nombre: ..., ... }` |
| Mostrar los datos | `print(est)` usa el `__repr__` generado | `JSON.stringify(est)` o `console.log(est)` |
| Acceso a campos | `est.nombre`; en `NamedTuple` también `reg[0]` | `est.nombre` o `est["nombre"]` |
| Recorrido con desempaquetado | `for nombre, edad, promedio in registros` (por posición) | `for (const { nombre, edad, promedio } of registros)` (por nombre) |
| Record inmutable | `NamedTuple` (o `@dataclass(frozen=True)`) | `Object.freeze(objeto)` |
| Error al modificar un record | `AttributeError: can't set attribute` | `TypeError: Cannot assign to read only property` (solo en modo estricto) |
| Crear una copia con un campo cambiado | `reg._replace(promedio=4.1)` | `Object.freeze({ ...reg, promedio: 4.1 })` |
| Igualdad por valor | `==` compara campo por campo (`__eq__` generado) | `===` compara referencias: dos objetos con los mismos datos son distintos |

**Conclusión del bloque:** Python ofrece un struct/record "real" (un tipo declarado, con campos
tipados, igualdad por valor e inmutabilidad verificada), mientras que en JavaScript el struct es
una **convención**: un objeto plano sin métodos, cuya forma la garantiza una factory function y
cuya inmutabilidad se consigue congelándolo.
