"""
Comparativa Struct/Record vs Objeto en Python - Estructura de Datos, Unidad 1.

Se resuelve EL MISMO PROBLEMA con el mismo Estudiante modelado de tres formas,
en un solo archivo, para señalar las diferencias directamente en el código.

  Problema: registrar 3 estudiantes, mostrarlos, cambiar el promedio de uno,
  intentar asignarle un promedio inválido (7.5) y copiar un estudiante.

  A) Struct -> @dataclass (mutable). Las operaciones son funciones EXTERNAS.
  B) Record -> @dataclass(frozen=True) (inmutable).
  C) Objeto -> clase con el promedio privado y métodos que validan el dato.

Ejecución:
    python python/comparativa.py
"""

from dataclasses import FrozenInstanceError, dataclass, replace

NOMBRE_A_MODIFICAR = "Luis Pérez"
NUEVO_PROMEDIO = 4.1
PROMEDIO_INVALIDO = 7.5


# A) Struct: solo datos, mutable.
@dataclass
class EstudianteStruct:
    nombre: str
    edad: int
    promedio: float


# B) Record: solo datos, inmutable.
@dataclass(frozen=True)
class EstudianteRecord:
    nombre: str
    edad: int
    promedio: float


# C) Objeto: datos + comportamiento, con el promedio encapsulado.
class Estudiante:
    PROMEDIO_MINIMO = 0.0
    PROMEDIO_MAXIMO = 5.0

    def __init__(self, nombre: str, edad: int, promedio: float) -> None:
        self.nombre = nombre
        self.edad = edad
        self.__promedio = 0.0
        self.setPromedio(promedio)

    def getPromedio(self) -> float:
        return self.__promedio

    def setPromedio(self, nuevo_promedio: float) -> None:
        if not Estudiante.PROMEDIO_MINIMO <= nuevo_promedio <= Estudiante.PROMEDIO_MAXIMO:
            raise ValueError(f"promedio inválido ({nuevo_promedio}): debe estar entre 0.0 y 5.0")
        self.__promedio = nuevo_promedio

    def mostrarInfo(self) -> None:
        print(formatear(self.nombre, self.edad, self.__promedio))


# Con el struct y el record, "mostrar" y "cambiar" son funciones EXTERNAS que
# reciben los datos como parámetro: el struct no sabe hacer nada por sí mismo.
def formatear(nombre: str, edad: int, promedio: float) -> str:
    return f"       {nombre:<14} | edad: {edad:>2} | promedio: {promedio:.1f}"


def mostrar_info(estudiante) -> None:
    print(formatear(estudiante.nombre, estudiante.edad, estudiante.promedio))


def buscar(arreglo: list, nombre: str):
    """Búsqueda lineal por nombre (sirve para los tres modelos)."""
    for elemento in arreglo:
        if elemento.nombre == nombre:
            return elemento
    return None


def declaracion() -> None:
    print("\n1. Declaración: el mismo Estudiante tres veces")
    print("  A) Struct -> @dataclass              : nombre, edad, promedio | sin métodos propios")
    print("  B) Record -> @dataclass(frozen=True) : nombre, edad, promedio | sin métodos, inmutable")
    print("  C) Objeto -> class Estudiante        : nombre, edad, __promedio (privado)"
          " | getPromedio, setPromedio, mostrarInfo")


def crear_y_mostrar() -> tuple[list[EstudianteStruct], list[EstudianteRecord], list[Estudiante]]:
    datos = [("Ana Martínez", 19, 4.2), ("Luis Pérez", 21, 3.6), ("Sofía Gómez", 20, 4.7)]
    structs = [EstudianteStruct(*d) for d in datos]
    records = [EstudianteRecord(*d) for d in datos]
    objetos = [Estudiante(*d) for d in datos]

    print("\n2. Crear los 3 estudiantes, guardarlos en un arreglo y mostrarlos")
    print("  A) Struct -> función externa: mostrar_info(estudiante)")
    for estudiante in structs:
        mostrar_info(estudiante)
    print("  B) Record -> la misma función externa: mostrar_info(estudiante)")
    for estudiante in records:
        mostrar_info(estudiante)
    print("  C) Objeto -> método propio: estudiante.mostrarInfo()")
    for estudiante in objetos:
        estudiante.mostrarInfo()
    return structs, records, objetos


def modificar(structs: list[EstudianteStruct], records: list[EstudianteRecord],
              objetos: list[Estudiante]) -> None:
    print(f"\n3. Cambiar el promedio de {NOMBRE_A_MODIFICAR} a {NUEVO_PROMEDIO}")

    luis_struct = buscar(structs, NOMBRE_A_MODIFICAR)
    luis_struct.promedio = NUEVO_PROMEDIO
    print(f"  A) Struct: luis.promedio = {NUEVO_PROMEDIO} -> promedio = {luis_struct.promedio}"
          " (cualquier parte del programa puede cambiarlo)")

    posicion = records.index(buscar(records, NOMBRE_A_MODIFICAR))
    luis_record = records[posicion]
    try:
        luis_record.promedio = NUEVO_PROMEDIO
    except FrozenInstanceError as error:
        print(f"  B) Record: luis.promedio = {NUEVO_PROMEDIO} -> FrozenInstanceError: {error}")
    records[posicion] = replace(luis_record, promedio=NUEVO_PROMEDIO)
    print(f"             replace(luis, promedio={NUEVO_PROMEDIO}) -> record NUEVO con promedio ="
          f" {records[posicion].promedio} (¿es otro objeto? {records[posicion] is not luis_record})")

    luis_objeto = buscar(objetos, NOMBRE_A_MODIFICAR)
    luis_objeto.setPromedio(NUEVO_PROMEDIO)
    print(f"  C) Objeto: luis.setPromedio({NUEVO_PROMEDIO}) -> getPromedio() = {luis_objeto.getPromedio()}")


def dato_invalido(structs: list[EstudianteStruct], records: list[EstudianteRecord],
                  objetos: list[Estudiante]) -> None:
    print(f"\n4. Intentar asignar un promedio inválido ({PROMEDIO_INVALIDO}, la escala es de 0.0 a 5.0)")

    luis_struct = buscar(structs, NOMBRE_A_MODIFICAR)
    luis_struct.promedio = PROMEDIO_INVALIDO
    print(f"  A) Struct: se acepta sin avisar -> promedio = {luis_struct.promedio}"
          " (el dato queda inconsistente)")

    luis_record = replace(buscar(records, NOMBRE_A_MODIFICAR), promedio=PROMEDIO_INVALIDO)
    print(f"  B) Record: replace() también lo acepta -> promedio = {luis_record.promedio}"
          " (habría que validar en __post_init__)")

    luis_objeto = buscar(objetos, NOMBRE_A_MODIFICAR)
    try:
        luis_objeto.setPromedio(PROMEDIO_INVALIDO)
    except ValueError as error:
        print(f"  C) Objeto: ValueError: {error}")
    print(f"             el promedio sigue siendo {luis_objeto.getPromedio()} (el objeto protege su estado)")


def igualdad() -> None:
    print("\n5. Igualdad: dos instancias con los MISMOS datos, ¿son iguales (==)?")
    print(f"  A) Struct: {EstudianteStruct('Ana Martínez', 19, 4.2) == EstudianteStruct('Ana Martínez', 19, 4.2)}"
          " -> @dataclass compara campo por campo (igualdad por valor)")
    print(f"  B) Record: {EstudianteRecord('Ana Martínez', 19, 4.2) == EstudianteRecord('Ana Martínez', 19, 4.2)}"
          " -> igualdad por valor")
    print(f"  C) Objeto: {Estudiante('Ana Martínez', 19, 4.2) == Estudiante('Ana Martínez', 19, 4.2)}"
          " -> sin __eq__, compara la identidad (¿es el mismo objeto?)")


def tipado() -> None:
    print("\n6. Tipado: Python es dinámico; las anotaciones de tipo no se verifican al ejecutar")
    struct = EstudianteStruct("Ana Martínez", "diecinueve", 4.2)
    print(f"  A) Struct: EstudianteStruct('Ana Martínez', 'diecinueve', 4.2) se crea sin error"
          f" -> edad = {struct.edad!r} ({type(struct.edad).__name__})")
    try:
        Estudiante("Ana Martínez", 19, "4.2")
    except TypeError as error:
        print(f"  C) Objeto: Estudiante('Ana Martínez', 19, '4.2') -> TypeError: {error}")
    print("             (setPromedio compara el valor con 0.0 y 5.0, y un texto no se puede comparar)")


def memoria() -> None:
    print("\n7. Memoria: en Python las variables guardan REFERENCIAS a objetos del heap")
    original = EstudianteStruct("Sofía Gómez", 20, 4.7)
    alias = original                      # no copia: las dos variables apuntan al mismo struct
    alias.promedio = 0.0
    print(f"  alias = original; alias.promedio = 0.0 -> original.promedio = {original.promedio}"
          f" (¿mismo objeto? {alias is original})")
    copia = replace(original, promedio=4.7)  # copia real: un struct nuevo en otra posición de memoria
    print(f"  copia = replace(original, promedio=4.7) -> original.promedio = {original.promedio},"
          f" copia.promedio = {copia.promedio} (¿mismo objeto? {copia is original})")
    print("  En C#, C o Go un struct es un VALOR: asignarlo copia todos sus campos (normalmente en el")
    print("  stack). En Python y JavaScript structs y objetos viven en el heap y se comparten por referencia.")


def resumen() -> None:
    print("\n8. Resumen")
    filas = [
        ("", "Struct", "Record", "Objeto"),
        ("Mutabilidad", "mutable", "inmutable", "mutable controlada"),
        ("Valida datos", "no", "solo si se agrega", "sí (setPromedio)"),
        ("Comportamiento", "funciones externas", "funciones externas", "métodos propios"),
        ("Igualdad (==)", "por valor", "por valor", "por identidad"),
        ("Encapsulamiento", "no", "no", "sí (__promedio)"),
    ]
    for criterio, struct, record, objeto in filas:
        print(f"  {criterio:<16}| {struct:<19}| {record:<19}| {objeto}")


def main() -> None:
    print("=== COMPARATIVA STRUCT / RECORD vs OBJETO EN PYTHON ===")
    print("Problema: registrar 3 estudiantes, mostrarlos, cambiar un promedio,")
    print("intentar un promedio inválido y copiar un estudiante.")
    declaracion()
    structs, records, objetos = crear_y_mostrar()
    modificar(structs, records, objetos)
    dato_invalido(structs, records, objetos)
    igualdad()
    tipado()
    memoria()
    resumen()


if __name__ == "__main__":
    main()
