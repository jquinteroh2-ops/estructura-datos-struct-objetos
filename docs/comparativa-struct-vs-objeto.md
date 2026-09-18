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

## 3. Tabla comparativa: Struct/Record vs Objeto

| Criterio | Struct / Record | Objeto (clase e instancia) |
|---|---|---|
| **Definición** | Tipo compuesto que agrupa datos relacionados en campos con nombre. Solo guarda datos. Un *record* es un struct inmutable. | Instancia de una clase: agrupa datos (atributos) **y** comportamiento (métodos), y protege su estado (encapsulamiento). |
| **Mutabilidad** | Struct: mutable, cualquier parte del programa cambia sus campos directamente. Record: inmutable; para "cambiarlo" se crea una copia con el campo nuevo. | Mutable, pero de forma **controlada**: el estado solo cambia a través de sus métodos (`setPromedio`), que validan el dato. |
| **Tipado** | En lenguajes estáticos (C, C#, Go, TypeScript) cada campo tiene un tipo fijo que el compilador verifica. En Python los tipos se anotan pero no se verifican al ejecutar; en JavaScript no se declaran. | Mismas reglas del lenguaje para sus atributos; además, sus métodos pueden validar tipos y rangos en tiempo de ejecución (`setPromedio` rechaza `7.5` o `'4.2'`). |
| **Uso en memoria (stack/heap)** | En C, C# y Go el struct es un **tipo valor**: una variable local vive en el **stack** (o dentro del arreglo u objeto que la contiene) y asignarla **copia todos los campos**. En Python y JavaScript el struct/record también es un objeto del **heap** y las variables guardan referencias. | Vive en el **heap**; las variables guardan una **referencia**. Asignar (`b = a`) no copia el objeto: las dos variables apuntan al mismo. Lo libera el recolector de basura cuando nadie lo referencia. |
| **Igualdad** | Normalmente **por valor**: dos registros con los mismos datos son iguales (`@dataclass`, `NamedTuple`, `record` de C#). En JS, `===` compara referencias incluso en objetos planos. | **Por identidad**: dos objetos con los mismos datos son distintos, salvo que la clase redefina la igualdad (`__eq__`, `Equals`). |
| **Comportamiento** | Ninguno propio: las operaciones son funciones externas que reciben el struct. | Métodos propios: el objeto sabe mostrarse (`mostrarInfo`) y cambiarse (`setPromedio`). |
| **Ejemplo en lenguaje estático** | TypeScript: `interface EstudianteRecord { readonly nombre: string; readonly edad: number; readonly promedio: number; }` · C#: `struct EstudianteStruct { ... }` | TypeScript: `class Estudiante { #promedio: number; setPromedio(p: number): void { ... } }` |
| **Ejemplo en lenguaje dinámico** | Python: `@dataclass class EstudianteStruct` · JavaScript: `{ nombre, edad, promedio }` | Python: `class Estudiante` con `__promedio` · JavaScript: `class Estudiante` con `#promedio` |

### Ejemplo en un lenguaje estático: TypeScript (`js/tipado-estatico.ts`)

TypeScript se usa **solo en este ejemplo puntual**, para mostrar qué cambia cuando los tipos se
declaran y se verifican antes de ejecutar. El archivo trae comentadas tres líneas con errores de
tipo; al quitarles el comentario, VS Code las subraya en rojo sin ejecutar el programa:

```ts
interface EstudianteRecord {          // record: solo datos, campos de solo lectura
  readonly nombre: string;
  readonly edad: number;
  readonly promedio: number;
}

const invalido: EstudianteRecord = { nombre: 'Ana Martínez', edad: 'diecinueve', promedio: 4.2 };
// error TS2322: Type 'string' is not assignable to type 'number'.

registros[1].promedio = 4.1;
// error TS2540: Cannot assign to 'promedio' because it is a read-only property.

estudiantes[1].setPromedio('4.1');
// error TS2345: Argument of type 'string' is not assignable to parameter of type 'number'.
```

En Python y JavaScript esos mismos errores **no se detectan hasta ejecutar** (o no se detectan
nunca): `EstudianteStruct("Ana Martínez", "diecinueve", 4.2)` se crea sin ningún aviso.

### Stack vs heap con un tipo valor: C# (solo como referencia teórica)

Python y JavaScript no tienen tipos valor definidos por el usuario, así que la diferencia de
memoria entre struct y objeto se ve mejor en C#, donde `struct` es un tipo valor y `class` un
tipo referencia:

```csharp
struct EstudianteStruct { public string Nombre; public int Edad; public double Promedio; }
class  EstudianteClase  { public string Nombre; public int Edad; public double Promedio; }

var s1 = new EstudianteStruct { Nombre = "Ana", Edad = 19, Promedio = 4.2 };
var s2 = s1;          // se COPIAN todos los campos (tipo valor, en el stack)
s2.Promedio = 0.0;    // s1.Promedio sigue siendo 4.2

var o1 = new EstudianteClase { Nombre = "Ana", Edad = 19, Promedio = 4.2 };
var o2 = o1;          // se copia solo la REFERENCIA (el objeto está en el heap)
o2.Promedio = 0.0;    // o1.Promedio también pasa a 0.0
```

En Python y JavaScript ocurre siempre lo segundo, sea struct u objeto; por eso los programas de
comparativa muestran que `alias = original` comparte el mismo dato y que para copiarlo hay que
crear uno nuevo explícitamente (`replace(...)` en Python, `{ ...original }` en JavaScript).

## 4. El mismo problema con struct/record y con objeto (`comparativa.py` / `comparativa.js`)

Los dos programas resuelven el mismo problema con el mismo `Estudiante` modelado tres veces
(struct, record y objeto) en un solo archivo por lenguaje: registrar 3 estudiantes, mostrarlos,
cambiar el promedio de uno, intentar un promedio inválido y copiar un estudiante.

| Situación | Struct | Record | Objeto |
|---|---|---|---|
| Mostrar los datos | Función externa `mostrar_info(est)` | La misma función externa | Método propio `est.mostrarInfo()` |
| Cambiar el promedio a 4.1 | `est.promedio = 4.1` (directo) | Error al asignar; se crea uno nuevo (`replace` / spread) | `est.setPromedio(4.1)` |
| Promedio inválido 7.5 | Se acepta sin avisar: dato inconsistente | La copia también lo acepta (habría que validar al construir) | Excepción; el promedio no cambia |
| Mismos datos, ¿iguales? | Python: sí (por valor) · JS: no (por referencia) | Python: sí · JS: no | No (por identidad) |
| Tipo incorrecto (`edad = "diecinueve"`) | Se acepta | Se acepta | `setPromedio` rechaza un promedio de tipo texto |

### Ventajas y desventajas

**Struct / Record**

- ✅ Declaración mínima y lectura directa: ideal para agrupar y transportar datos.
- ✅ Igualdad por valor e impresión automática (en Python, gracias a `@dataclass`/`NamedTuple`).
- ✅ El record, al ser inmutable, se puede compartir entre partes del programa sin miedo a que
  alguien lo cambie; es seguro como dato histórico (por ejemplo, el detalle de una venta ya hecha).
- ❌ No protege sus datos: el struct acepta cualquier valor y la validación queda repartida en
  cada lugar donde se modifica.
- ❌ El comportamiento queda en funciones sueltas, separadas de los datos que manipulan.

**Objeto**

- ✅ Encapsula el estado: las reglas (promedio entre 0.0 y 5.0) viven en un solo lugar y siempre
  se cumplen.
- ✅ Datos y comportamiento juntos: cada objeto sabe mostrarse y modificarse.
- ✅ Se puede extender con herencia y polimorfismo.
- ❌ Más código para el mismo dato (constructor, getters, setters).
- ❌ La igualdad por identidad obliga a redefinir `__eq__`/`equals` si se quiere comparar por datos.

**Criterio práctico:** si el dato **no tiene reglas propias** y solo se guarda o se transporta,
un struct (o un record, si no debe cambiar) es suficiente y más simple. Si el dato **tiene reglas
que proteger o acciones propias**, conviene un objeto.
