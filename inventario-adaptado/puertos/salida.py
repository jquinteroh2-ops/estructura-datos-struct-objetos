"""
Puerto de SALIDA: lo que el núcleo necesita para guardar y consultar los datos.

El núcleo solo conoce esta interfaz; no sabe si detrás hay arreglos en memoria,
un archivo o una base de datos real. Hoy la implementa el adaptador
RepositorioArreglos, que guarda todo en arreglos de tamaño fijo.
"""

from abc import ABC, abstractmethod
from typing import Optional

from dominio.cliente import Cliente
from dominio.compra import Compra
from dominio.producto import Producto
from dominio.proveedor import Proveedor
from dominio.venta import Venta


class RepositorioInventario(ABC):

    # Productos
    @abstractmethod
    def guardar_producto(self, producto: Producto) -> None: ...

    @abstractmethod
    def buscar_producto(self, codigo: str) -> Optional[Producto]: ...

    @abstractmethod
    def listar_productos(self) -> list[Producto]: ...

    # Proveedores
    @abstractmethod
    def guardar_proveedor(self, proveedor: Proveedor) -> None: ...

    @abstractmethod
    def buscar_proveedor(self, nit: str) -> Optional[Proveedor]: ...

    @abstractmethod
    def listar_proveedores(self) -> list[Proveedor]: ...

    # Clientes
    @abstractmethod
    def guardar_cliente(self, cliente: Cliente) -> None: ...

    @abstractmethod
    def buscar_cliente(self, documento: str) -> Optional[Cliente]: ...

    @abstractmethod
    def reemplazar_cliente(self, cliente: Cliente) -> None: ...

    @abstractmethod
    def listar_clientes(self) -> list[Cliente]: ...

    # Compras
    @abstractmethod
    def guardar_compra(self, compra: Compra) -> None: ...

    @abstractmethod
    def contar_compras(self) -> int: ...

    # Ventas
    @abstractmethod
    def guardar_venta(self, venta: Venta) -> None: ...

    @abstractmethod
    def contar_ventas(self) -> int: ...

    @abstractmethod
    def listar_ventas(self) -> list[Venta]: ...
