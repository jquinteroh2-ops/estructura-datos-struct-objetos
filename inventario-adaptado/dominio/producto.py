"""
Producto -> modelado como OBJETO.

Por qué objeto y no struct/record:
  - Tiene reglas de negocio que proteger: el precio de venta debe ser mayor que
    cero y el stock nunca puede quedar negativo.
  - Su estado cambia durante el programa (entra mercancía con las compras y sale
    con las ventas), y esos cambios solo deben ocurrir a través de sus métodos,
    que validan cada operación. Por eso sus atributos son privados.
"""

from dominio.errores import ErrorInventario


class Producto:
    """Producto del inventario con su precio de venta y sus existencias (stock)."""

    def __init__(self, codigo: str, nombre: str, precio_venta: int, stock: int = 0) -> None:
        if precio_venta <= 0:
            raise ErrorInventario("el precio de venta debe ser mayor que cero")
        if stock < 0:
            raise ErrorInventario("el stock inicial no puede ser negativo")
        self.__codigo = codigo
        self.__nombre = nombre
        self.__precio_venta = precio_venta
        self.__stock = stock

    # Propiedades de solo lectura: se pueden consultar, pero no asignar desde fuera.
    @property
    def codigo(self) -> str:
        return self.__codigo

    @property
    def nombre(self) -> str:
        return self.__nombre

    @property
    def precio_venta(self) -> int:
        return self.__precio_venta

    @property
    def stock(self) -> int:
        return self.__stock

    def hay_stock(self, cantidad: int) -> bool:
        return cantidad <= self.__stock

    def valor_en_inventario(self) -> int:
        return self.__precio_venta * self.__stock

    def aumentar_stock(self, cantidad: int) -> None:
        """Entrada de mercancía (compra a un proveedor)."""
        if cantidad <= 0:
            raise ErrorInventario("la cantidad que entra debe ser mayor que cero")
        self.__stock += cantidad

    def disminuir_stock(self, cantidad: int) -> None:
        """Salida de mercancía (venta a un cliente)."""
        if cantidad <= 0:
            raise ErrorInventario("la cantidad que sale debe ser mayor que cero")
        if not self.hay_stock(cantidad):
            raise ErrorInventario(
                f"stock insuficiente de '{self.__nombre}': hay {self.__stock} y se piden {cantidad}"
            )
        self.__stock -= cantidad
