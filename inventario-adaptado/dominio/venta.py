"""
DetalleVenta -> modelado como RECORD (dataclass congelada, inmutable).
  - Es una línea de la venta: qué producto salió, cuántas unidades y a qué precio.
  - Guarda el precio del momento de la venta: si luego cambia el precio del
    producto, la venta ya hecha no debe cambiar. La inmutabilidad lo garantiza.

Venta -> modelada como OBJETO.
  - Guarda sus detalles en un arreglo de tamaño fijo, controla que no se llene
    y calcula el total recorriéndolo.
"""

from dataclasses import dataclass

from dominio.errores import ErrorInventario

MAX_DETALLES_POR_VENTA = 20


@dataclass(frozen=True)
class DetalleVenta:
    codigo_producto: str
    cantidad: int
    precio_unitario: int

    @property
    def subtotal(self) -> int:
        return self.cantidad * self.precio_unitario


class Venta:
    """Venta a un cliente (salida del inventario)."""

    def __init__(self, numero: int, documento_cliente: str, fecha: str) -> None:
        self.__numero = numero
        self.__documento_cliente = documento_cliente
        self.__fecha = fecha
        self.__detalles = [None] * MAX_DETALLES_POR_VENTA
        self.__total_detalles = 0

    @property
    def numero(self) -> int:
        return self.__numero

    @property
    def documento_cliente(self) -> str:
        return self.__documento_cliente

    @property
    def fecha(self) -> str:
        return self.__fecha

    def agregar_detalle(self, detalle: DetalleVenta) -> None:
        if self.__total_detalles == len(self.__detalles):
            raise ErrorInventario(f"una venta admite máximo {len(self.__detalles)} productos")
        self.__detalles[self.__total_detalles] = detalle
        self.__total_detalles += 1

    def obtener_detalles(self) -> list[DetalleVenta]:
        copia = [None] * self.__total_detalles
        for i in range(self.__total_detalles):
            copia[i] = self.__detalles[i]
        return copia

    def calcular_total(self) -> int:
        total = 0
        for i in range(self.__total_detalles):
            total += self.__detalles[i].subtotal
        return total
