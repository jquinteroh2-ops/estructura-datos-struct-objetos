"""
RepositorioArreglos -> adaptador de SALIDA, modelado como OBJETO.

Implementa el puerto RepositorioInventario usando las tablas (arreglos de tamaño
fijo) del struct BaseDatos. Todas las operaciones se hacen a mano, como con los
arreglos de Java: insertar en la posición del contador, búsqueda lineal y copia
elemento por elemento.
"""

from typing import Callable, Optional

from adaptadores.salida.base_datos import BaseDatos
from dominio.cliente import Cliente
from dominio.compra import Compra
from dominio.errores import ErrorInventario
from dominio.producto import Producto
from dominio.proveedor import Proveedor
from dominio.venta import Venta
from puertos.salida import RepositorioInventario


def _insertar(tabla: list, total: int, elemento, nombre_tabla: str) -> int:
    """Escribe el elemento en la primera posición libre y devuelve el nuevo total."""
    if total == len(tabla):
        raise ErrorInventario(f"la tabla de {nombre_tabla} está llena ({len(tabla)} registros)")
    tabla[total] = elemento
    return total + 1


def _posicion(tabla: list, total: int, coincide: Callable) -> int:
    """Búsqueda lineal: devuelve la posición del primer elemento que cumple la condición, o -1."""
    for i in range(total):
        if coincide(tabla[i]):
            return i
    return -1


def _copiar(tabla: list, total: int) -> list:
    """Devuelve un arreglo nuevo con solo las posiciones ocupadas."""
    copia = [None] * total
    for i in range(total):
        copia[i] = tabla[i]
    return copia


class RepositorioArreglos(RepositorioInventario):

    def __init__(self, base_datos: BaseDatos) -> None:
        self.__bd = base_datos

    # Productos
    def guardar_producto(self, producto: Producto) -> None:
        bd = self.__bd
        bd.total_productos = _insertar(bd.productos, bd.total_productos, producto, "productos")

    def buscar_producto(self, codigo: str) -> Optional[Producto]:
        bd = self.__bd
        i = _posicion(bd.productos, bd.total_productos, lambda p: p.codigo == codigo)
        return bd.productos[i] if i >= 0 else None

    def listar_productos(self) -> list[Producto]:
        return _copiar(self.__bd.productos, self.__bd.total_productos)

    # Proveedores
    def guardar_proveedor(self, proveedor: Proveedor) -> None:
        bd = self.__bd
        bd.total_proveedores = _insertar(bd.proveedores, bd.total_proveedores, proveedor, "proveedores")

    def buscar_proveedor(self, nit: str) -> Optional[Proveedor]:
        bd = self.__bd
        i = _posicion(bd.proveedores, bd.total_proveedores, lambda p: p.nit == nit)
        return bd.proveedores[i] if i >= 0 else None

    def listar_proveedores(self) -> list[Proveedor]:
        return _copiar(self.__bd.proveedores, self.__bd.total_proveedores)

    # Clientes
    def guardar_cliente(self, cliente: Cliente) -> None:
        bd = self.__bd
        bd.total_clientes = _insertar(bd.clientes, bd.total_clientes, cliente, "clientes")

    def buscar_cliente(self, documento: str) -> Optional[Cliente]:
        bd = self.__bd
        i = _posicion(bd.clientes, bd.total_clientes, lambda c: c.documento == documento)
        return bd.clientes[i] if i >= 0 else None

    def reemplazar_cliente(self, cliente: Cliente) -> None:
        """Los clientes son records inmutables: para "actualizar" uno se escribe
        el record nuevo en la misma posición del arreglo."""
        bd = self.__bd
        i = _posicion(bd.clientes, bd.total_clientes, lambda c: c.documento == cliente.documento)
        if i < 0:
            raise ErrorInventario(f"no existe un cliente con documento {cliente.documento}")
        bd.clientes[i] = cliente

    def listar_clientes(self) -> list[Cliente]:
        return _copiar(self.__bd.clientes, self.__bd.total_clientes)

    # Compras
    def guardar_compra(self, compra: Compra) -> None:
        bd = self.__bd
        bd.total_compras = _insertar(bd.compras, bd.total_compras, compra, "compras")

    def contar_compras(self) -> int:
        return self.__bd.total_compras

    # Ventas
    def guardar_venta(self, venta: Venta) -> None:
        bd = self.__bd
        bd.total_ventas = _insertar(bd.ventas, bd.total_ventas, venta, "ventas")

    def contar_ventas(self) -> int:
        return self.__bd.total_ventas

    def listar_ventas(self) -> list[Venta]:
        return _copiar(self.__bd.ventas, self.__bd.total_ventas)
