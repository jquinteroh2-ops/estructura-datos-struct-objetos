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
