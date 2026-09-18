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


def main() -> None:
    print("=== STRUCT / RECORD EN PYTHON ===")
    declaracion()


if __name__ == "__main__":
    main()
