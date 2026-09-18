"""
Cliente -> modelado como RECORD (dataclass congelada, inmutable).

Por qué record:
  - Solo guarda datos de identificación y contacto; no tiene reglas de negocio
    ni acciones propias.
  - Al ser inmutable nadie puede cambiar por accidente el documento o el nombre
    de un cliente. Si un dato cambia (por ejemplo el teléfono), se crea un record
    NUEVO con dataclasses.replace() y se reemplaza en su posición del arreglo.
  - @dataclass genera __init__, __repr__ y __eq__: dos clientes con los mismos
    datos son iguales (igualdad por valor, típica de un record).
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Cliente:
    documento: str
    nombre: str
    telefono: str
