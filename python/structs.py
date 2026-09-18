"""
Struct / Record en Python - Estructura de Datos, Unidad 1.

Python no tiene la palabra reservada `struct`, pero su librería estándar ofrece
dos formas de declarar un registro de datos con campos con nombre:

  - @dataclass  -> genera __init__, __repr__ y __eq__ a partir de los campos.
                   Es MUTABLE: un campo se puede cambiar después de crearlo.
  - NamedTuple  -> es una tupla con nombre para cada campo.
                   Es INMUTABLE: para "cambiar" un dato se crea un registro nuevo.

Ejecución:
    python python/structs.py
"""

from dataclasses import dataclass
from typing import NamedTuple, get_type_hints


# 1. Declaración
@dataclass
class EstudianteStruct:
    """Struct (mutable): solo agrupa datos relacionados, no tiene comportamiento."""

    nombre: str
    edad: int
    promedio: float


class EstudianteRecord(NamedTuple):
    """Record (inmutable): una vez creado, sus campos no se pueden cambiar."""

    nombre: str
    edad: int
    promedio: float


def describir_campos(tipo: type) -> str:
    """Devuelve los campos declarados y su tipo, p. ej. 'nombre: str, edad: int'."""
    return ", ".join(f"{campo}: {t.__name__}" for campo, t in get_type_hints(tipo).items())


def declaracion() -> None:
    print("\n1. Declaración")
    print(f"  EstudianteStruct (@dataclass, mutable)  -> {describir_campos(EstudianteStruct)}")
    print(f"  EstudianteRecord (NamedTuple, inmutable) -> {describir_campos(EstudianteRecord)}")


# 2. Inicialización
def inicializacion() -> tuple[list[EstudianteStruct], list[EstudianteRecord]]:
    """Crea 3 instancias de cada tipo con datos ficticios y las guarda en arreglos."""
    print("\n2. Inicialización (3 instancias con datos ficticios)")
    # Los campos se pueden pasar por posición o por nombre.
    ana = EstudianteStruct("Ana Martínez", 19, 4.2)
    luis = EstudianteStruct(nombre="Luis Pérez", edad=21, promedio=3.6)
    sofia = EstudianteStruct("Sofía Gómez", 20, 4.7)
    estudiantes = [ana, luis, sofia]

    registros = [
        EstudianteRecord("Ana Martínez", 19, 4.2),
        EstudianteRecord(nombre="Luis Pérez", edad=21, promedio=3.6),
        EstudianteRecord("Sofía Gómez", 20, 4.7),
    ]

    # @dataclass y NamedTuple generan __repr__: al imprimir se ven los datos.
    print("  a) Structs (@dataclass):")
    for estudiante in estudiantes:
        print(f"    {estudiante}")
    print("  b) Records (NamedTuple):")
    for registro in registros:
        print(f"    {registro}")
    return estudiantes, registros


# 3. Recorrido
def imprimir_estudiante(posicion: int, nombre: str, edad: int, promedio: float) -> None:
    print(f"    [{posicion}] {nombre:<14} | edad: {edad:>2} | promedio: {promedio:.1f}")


def recorrido(estudiantes: list[EstudianteStruct], registros: list[EstudianteRecord]) -> None:
    print("\n3. Recorrido del arreglo")
    print("  a) Structs, por índice y accediendo a cada campo por su nombre:")
    for i in range(len(estudiantes)):
        estudiante = estudiantes[i]
        imprimir_estudiante(i, estudiante.nombre, estudiante.edad, estudiante.promedio)

    print("  b) Records, desempaquetando los campos (un NamedTuple también es una tupla):")
    for i, (nombre, edad, promedio) in enumerate(registros):
        imprimir_estudiante(i, nombre, edad, promedio)
    print(f"     Acceso por posición: registros[0][0] = {registros[0][0]!r}")

    suma = 0.0
    for estudiante in estudiantes:
        suma += estudiante.promedio
    print(f"  Promedio del grupo: {suma / len(estudiantes):.2f}")


def main() -> None:
    print("=== STRUCT / RECORD EN PYTHON ===")
    declaracion()
    estudiantes, registros = inicializacion()
    recorrido(estudiantes, registros)


if __name__ == "__main__":
    main()
