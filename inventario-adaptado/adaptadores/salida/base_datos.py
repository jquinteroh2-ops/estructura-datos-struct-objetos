"""
BaseDatos -> modelada como STRUCT (dataclass mutable).

Representa la "base de datos" del programa igual que en la versión en Java: cada
tabla es un ARREGLO DE TAMAÑO FIJO y lleva un contador con las posiciones
ocupadas. No se usan append, remove ni diccionarios: los elementos se escriben
en la posición del contador, como en un arreglo de Java.

Por qué struct: solo agrupa las tablas y sus contadores; no decide nada ni valida
nada. Quien inserta, busca y recorre es el adaptador RepositorioArreglos.
"""

from dataclasses import dataclass, field

MAX_PRODUCTOS = 100
MAX_PROVEEDORES = 30
MAX_CLIENTES = 100
MAX_COMPRAS = 200
MAX_VENTAS = 200


def _tabla(capacidad: int):
    """Crea un arreglo nuevo de `capacidad` posiciones vacías para cada BaseDatos."""
    return field(default_factory=lambda: [None] * capacidad, repr=False)


@dataclass
class BaseDatos:
    productos: list = _tabla(MAX_PRODUCTOS)
    total_productos: int = 0
    proveedores: list = _tabla(MAX_PROVEEDORES)
    total_proveedores: int = 0
    clientes: list = _tabla(MAX_CLIENTES)
    total_clientes: int = 0
    compras: list = _tabla(MAX_COMPRAS)
    total_compras: int = 0
    ventas: list = _tabla(MAX_VENTAS)
    total_ventas: int = 0
