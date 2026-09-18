"""
Puerto de ENTRADA: los casos de uso que el núcleo ofrece al exterior.

Los adaptadores de entrada (el menú por consola y la demostración automática)
solo conocen esta interfaz; no saben cómo se implementa ni dónde se guardan los
datos. Se declara con abc.ABC, el equivalente en Python a una interface de Java.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from dominio.cliente import Cliente
from dominio.compra import Compra, DetalleCompra
from dominio.producto import Producto
from dominio.proveedor import Proveedor
from dominio.reporte import LineaReporte
from dominio.venta import Venta


@dataclass(frozen=True)
class ItemPedido:
    """RECORD: dato de entrada de una venta (qué producto y cuántas unidades).
    Viaja del adaptador al núcleo y, por ser inmutable, nadie lo altera en el camino."""

    codigo_producto: str
    cantidad: int


class CasosDeUsoInventario(ABC):

    @abstractmethod
    def registrar_producto(self, codigo: str, nombre: str, precio_venta: int,
                           stock_inicial: int = 0) -> Producto: ...

    @abstractmethod
    def registrar_proveedor(self, nit: str, nombre: str, telefono: str) -> Proveedor: ...

    @abstractmethod
    def registrar_cliente(self, documento: str, nombre: str, telefono: str) -> Cliente: ...

    @abstractmethod
    def actualizar_telefono_cliente(self, documento: str, nuevo_telefono: str) -> Cliente: ...

    @abstractmethod
    def registrar_compra(self, nit_proveedor: str, detalles: list[DetalleCompra]) -> Compra: ...

    @abstractmethod
    def registrar_venta(self, documento_cliente: str, items: list[ItemPedido]) -> Venta: ...

    @abstractmethod
    def buscar_producto(self, codigo: str) -> Optional[Producto]: ...

    @abstractmethod
    def buscar_proveedor(self, nit: str) -> Optional[Proveedor]: ...

    @abstractmethod
    def buscar_cliente(self, documento: str) -> Optional[Cliente]: ...

    @abstractmethod
    def listar_productos(self) -> list[Producto]: ...

    @abstractmethod
    def listar_proveedores(self) -> list[Proveedor]: ...

    @abstractmethod
    def listar_clientes(self) -> list[Cliente]: ...

    @abstractmethod
    def listar_ventas(self) -> list[Venta]: ...

    @abstractmethod
    def reporte_ventas_por_producto(self) -> list[LineaReporte]: ...
