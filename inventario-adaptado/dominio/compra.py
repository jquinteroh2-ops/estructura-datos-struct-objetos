"""
DetalleCompra -> modelado como RECORD (dataclass congelada, inmutable).
  - Es una línea de la compra: qué producto entró, cuántas unidades y a qué costo.
  - No tiene reglas propias y, una vez registrado, es un hecho histórico que no
    debe cambiar; frozen=True lo garantiza (asignar un campo lanza un error).
  - Su subtotal es un dato DERIVADO de sus propios campos (una propiedad de solo
    lectura): no cambia el estado, así que sigue siendo "solo datos".

Compra -> modelada como OBJETO.
  - Guarda sus detalles en un arreglo de tamaño fijo, controla que no se llene
    y calcula el total recorriéndolo: tiene comportamiento propio.
"""

from dataclasses import dataclass

from dominio.errores import ErrorInventario

MAX_DETALLES_POR_COMPRA = 20


@dataclass(frozen=True)
class DetalleCompra:
    codigo_producto: str
    cantidad: int
    costo_unitario: int

    @property
    def subtotal(self) -> int:
        return self.cantidad * self.costo_unitario


class Compra:
    """Compra de mercancía a un proveedor (entrada al inventario)."""

    def __init__(self, numero: int, nit_proveedor: str, fecha: str) -> None:
        self.__numero = numero
        self.__nit_proveedor = nit_proveedor
        self.__fecha = fecha
        self.__detalles = [None] * MAX_DETALLES_POR_COMPRA
        self.__total_detalles = 0

    @property
    def numero(self) -> int:
        return self.__numero

    @property
    def nit_proveedor(self) -> str:
        return self.__nit_proveedor

    @property
    def fecha(self) -> str:
        return self.__fecha

    def agregar_detalle(self, detalle: DetalleCompra) -> None:
        if self.__total_detalles == len(self.__detalles):
            raise ErrorInventario(f"una compra admite máximo {len(self.__detalles)} productos")
        self.__detalles[self.__total_detalles] = detalle
        self.__total_detalles += 1

    def obtener_detalles(self) -> list[DetalleCompra]:
        copia = [None] * self.__total_detalles
        for i in range(self.__total_detalles):
            copia[i] = self.__detalles[i]
        return copia

    def calcular_total(self) -> int:
        total = 0
        for i in range(self.__total_detalles):
            total += self.__detalles[i].subtotal
        return total
