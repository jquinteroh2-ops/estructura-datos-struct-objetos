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

## 2. Objetos (clases e instancias)

Una **clase** es el molde que define qué **datos** (atributos) y qué **comportamiento** (métodos)
tendrán sus objetos. Cada **objeto** o **instancia** es un ejemplar concreto de la clase, con sus
propios valores. A diferencia de un struct, el objeto **protege su estado**: los datos se cambian
a través de sus métodos, que pueden validar las reglas del problema.

### Python (`python/objetos.py`)

```python
class Estudiante:
    PROMEDIO_MINIMO = 0.0
    PROMEDIO_MAXIMO = 5.0

    def __init__(self, nombre: str, edad: int, promedio: float) -> None:
        self.nombre = nombre
        self.edad = edad
        self.__promedio = 0.0
        self.setPromedio(promedio)          # el constructor reutiliza la validación

    def getPromedio(self) -> float:
        return self.__promedio

    def setPromedio(self, nuevo_promedio: float) -> None:
        if not Estudiante.PROMEDIO_MINIMO <= nuevo_promedio <= Estudiante.PROMEDIO_MAXIMO:
            raise ValueError(...)
        self.__promedio = nuevo_promedio

    def mostrarInfo(self) -> None:
        print(f"{self.nombre} | edad: {self.edad} | promedio: {self.__promedio:.1f}")
```

| Actividad | Implementación en Python |
|---|---|
| Declaración | `class Estudiante` con constructor `__init__`, atributos `nombre`, `edad`, `__promedio` y los métodos `getPromedio`, `setPromedio`, `mostrarInfo` |
| Inicialización | `Estudiante("Ana Martínez", 19, 4.2)`; las 3 instancias se guardan en la lista `estudiantes` |
| Recorrido | `for estudiante in estudiantes: estudiante.mostrarInfo()` — cada objeto se muestra a sí mismo |
| Modificación | `luis.setPromedio(4.1)`; `setPromedio(7.5)` lanza `ValueError` y el promedio no cambia |
| Encapsulamiento | `__promedio` (dos guiones bajos) activa el *name mangling*: `luis.__promedio` desde fuera lanza `AttributeError` |

**Notas de Python:**

- `self` es la referencia explícita al objeto actual; en Python se escribe como primer parámetro
  de cada método.
- La privacidad en Python es por **convención**: `_atributo` significa "uso interno" y
  `__atributo` renombra internamente el atributo a `_Estudiante__promedio`. No es una barrera
  absoluta, pero evita accesos accidentales desde fuera de la clase.
- Una clase normal **no genera `__repr__`** como `@dataclass`: `print(objeto)` muestra
  `<__main__.Estudiante object at 0x...>`, es decir, su tipo y su dirección en memoria. Por eso
  la clase define `mostrarInfo()`.
- Los nombres `mostrarInfo` y `setPromedio` están en *camelCase* porque así los pide el enunciado;
  la convención de Python (PEP 8) sería `mostrar_info` y `set_promedio`.

### JavaScript (`js/objetos.js`)

```js
class Estudiante {
  static PROMEDIO_MINIMO = 0.0;
  static PROMEDIO_MAXIMO = 5.0;
  #promedio = 0.0;                       // campo privado (ES2022)

  constructor(nombre, edad, promedio) {
    this.nombre = nombre;
    this.edad = edad;
    this.setPromedio(promedio);
  }

  getPromedio() { return this.#promedio; }

  setPromedio(nuevoPromedio) {
    if (typeof nuevoPromedio !== 'number'
        || nuevoPromedio < Estudiante.PROMEDIO_MINIMO
        || nuevoPromedio > Estudiante.PROMEDIO_MAXIMO) {
      throw new RangeError(...);
    }
    this.#promedio = nuevoPromedio;
  }

  mostrarInfo() {
    console.log(`${this.nombre} | edad: ${this.edad} | promedio: ${this.#promedio.toFixed(1)}`);
  }
}
```

### Diferencias de implementación Python vs JavaScript (objetos)

| Aspecto | Python | JavaScript |
|---|---|---|
| Declaración | `class Estudiante:` | `class Estudiante { ... }` |
| Constructor | `def __init__(self, ...)` | `constructor(...)` |
| Referencia al objeto actual | `self`, explícito como primer parámetro | `this`, implícito |
| Crear una instancia | `Estudiante("Ana Martínez", 19, 4.2)` | `new Estudiante('Ana Martínez', 19, 4.2)` (con `new`) |
| Atributo privado | `__promedio`: privado por convención (*name mangling*) | `#promedio`: privado real, impuesto por el lenguaje |
| Acceso al privado desde fuera | `luis.__promedio` lanza `AttributeError` en tiempo de ejecución | `luis.#promedio` ni siquiera compila (`SyntaxError`); `luis.promedio` es `undefined` |
| Constantes de clase | `PROMEDIO_MAXIMO = 5.0` en el cuerpo de la clase | `static PROMEDIO_MAXIMO = 5.0` |
| Error por dato inválido | `ValueError` | `RangeError` |
| Validación de tipo | Comparar `str` con `float` ya lanza `TypeError` | Hay que comprobar `typeof`: `'4.5' < 5` convierte el texto a número sin avisar |
| Ver el tipo del objeto | `type(obj).__name__` | `obj.constructor.name` o `obj instanceof Estudiante` |

### Diferencia entre la clase `Estudiante` y el struct/record

| Criterio | Struct / Record (bloque 1) | Clase `Estudiante` (bloque 2) |
|---|---|---|
| Qué contiene | Solo **datos** | **Datos + comportamiento** (métodos) |
| Mostrar la información | Una función externa lee los campos y los imprime | El propio objeto se muestra: `estudiante.mostrarInfo()` |
| Cambiar el promedio | Struct: asignación directa `est.promedio = 4.1`, sin control. Record: no se puede; se crea uno nuevo | Solo mediante `setPromedio()`, que valida el rango |
| Dato inválido (`7.5`) | El struct lo acepta en silencio y queda un estudiante inconsistente | Se rechaza con una excepción y el estado no cambia |
| Encapsulamiento | Ninguno: todos los campos son públicos | El promedio es privado; solo se accede por `getPromedio()`/`setPromedio()` |
| Mutabilidad | Struct mutable / record inmutable | Mutable, pero **controlada** por sus métodos |
| Igualdad | Por valor (`@dataclass`/`NamedTuple` comparan los campos) | Por identidad: dos objetos con los mismos datos son distintos |
| Cuándo usarlo | Para transportar o agrupar datos sin reglas propias | Cuando los datos tienen reglas que proteger o acciones propias |

**Conclusión del bloque:** el struct/record responde a *"¿qué datos tiene un estudiante?"*; la
clase responde además a *"¿qué puede hacer un estudiante y qué reglas debe cumplir?"*. La clase
garantiza que ningún estudiante tenga un promedio fuera de 0.0–5.0, algo que el struct no puede
asegurar por sí mismo.
