"""
ServicioInventario -> núcleo de la aplicación, modelado como OBJETO.

Implementa los casos de uso del puerto de entrada usando solamente el puerto de
salida: no sabe que los datos están en arreglos ni que hay una consola.
Antes de modificar cualquier dato valida TODA la operación, para que una compra
o una venta con errores no deje el inventario a medias.
"""

from dataclasses import replace
from datetime import date
from typing import Optional

from dominio.cliente import Cliente
from dominio.compra import Compra, DetalleCompra
from dominio.errores import ErrorInventario
from dominio.producto import Producto
from dominio.proveedor import Proveedor
from dominio.reporte import LineaReporte
from dominio.venta import DetalleVenta, Venta
from puertos.entrada import CasosDeUsoInventario, ItemPedido
from puertos.salida import RepositorioInventario


def _normalizar_codigo(codigo: str) -> str:
    return codigo.strip().upper()


def _hoy() -> str:
    return date.today().isoformat()


class ServicioInventario(CasosDeUsoInventario):

    def __init__(self, repositorio: RepositorioInventario) -> None:
        self.__repositorio = repositorio

    # Registros básicos
    def registrar_producto(self, codigo: str, nombre: str, precio_venta: int,
                           stock_inicial: int = 0) -> Producto:
        codigo, nombre = _normalizar_codigo(codigo), nombre.strip()
        if not codigo or not nombre:
            raise ErrorInventario("el código y el nombre del producto son obligatorios")
        if self.__repositorio.buscar_producto(codigo) is not None:
            raise ErrorInventario(f"ya existe un producto con el código {codigo}")
        producto = Producto(codigo, nombre, precio_venta, stock_inicial)
        self.__repositorio.guardar_producto(producto)
        return producto

    def registrar_proveedor(self, nit: str, nombre: str, telefono: str) -> Proveedor:
        nit, nombre = nit.strip(), nombre.strip()
        if not nit or not nombre:
            raise ErrorInventario("el NIT y el nombre del proveedor son obligatorios")
        if self.__repositorio.buscar_proveedor(nit) is not None:
            raise ErrorInventario(f"ya existe un proveedor con el NIT {nit}")
        proveedor = Proveedor(nit, nombre, telefono.strip())
        self.__repositorio.guardar_proveedor(proveedor)
        return proveedor

    def registrar_cliente(self, documento: str, nombre: str, telefono: str) -> Cliente:
        documento, nombre = documento.strip(), nombre.strip()
        if not documento or not nombre:
            raise ErrorInventario("el documento y el nombre del cliente son obligatorios")
        if self.__repositorio.buscar_cliente(documento) is not None:
            raise ErrorInventario(f"ya existe un cliente con el documento {documento}")
        cliente = Cliente(documento, nombre, telefono.strip())
        self.__repositorio.guardar_cliente(cliente)
        return cliente

    def actualizar_telefono_cliente(self, documento: str, nuevo_telefono: str) -> Cliente:
        cliente = self.__obtener_cliente(documento)
        # Cliente es un record inmutable: no se modifica, se crea uno NUEVO con el
        # teléfono cambiado y se reemplaza en el arreglo.
        actualizado = replace(cliente, telefono=nuevo_telefono.strip())
        self.__repositorio.reemplazar_cliente(actualizado)
        return actualizado

    # Movimientos de inventario
    def registrar_compra(self, nit_proveedor: str, detalles: list[DetalleCompra]) -> Compra:
        proveedor = self.__obtener_proveedor(nit_proveedor)
        if len(detalles) == 0:
            raise ErrorInventario("la compra debe tener al menos un producto")

        # 1. Validar todo antes de modificar nada.
        productos = [None] * len(detalles)
        lineas = [None] * len(detalles)
        for i in range(len(detalles)):
            detalle = detalles[i]
            if detalle.cantidad <= 0 or detalle.costo_unitario <= 0:
                raise ErrorInventario(
                    f"la cantidad y el costo de {detalle.codigo_producto} deben ser mayores que cero")
            productos[i] = self.__obtener_producto(detalle.codigo_producto)
            if detalle.codigo_producto != productos[i].codigo:
                # El detalle es un record: para normalizar su código se crea uno nuevo.
                detalle = replace(detalle, codigo_producto=productos[i].codigo)
            lineas[i] = detalle

        compra = Compra(self.__repositorio.contar_compras() + 1, proveedor.nit, _hoy())
        for detalle in lineas:
            compra.agregar_detalle(detalle)
        if not proveedor.puede_registrar_compra():
            raise ErrorInventario(f"el proveedor {proveedor.nombre} no admite más compras")

        # 2. Registrar la compra y hacer entrar la mercancía.
        self.__repositorio.guardar_compra(compra)
        proveedor.registrar_compra(compra)
        for i in range(len(lineas)):
            productos[i].aumentar_stock(lineas[i].cantidad)
        return compra

    def registrar_venta(self, documento_cliente: str, items: list[ItemPedido]) -> Venta:
        cliente = self.__obtener_cliente(documento_cliente)
        if len(items) == 0:
            raise ErrorInventario("la venta debe tener al menos un producto")

        # 1. Validar todo antes de modificar nada.
        productos = [None] * len(items)
        for i in range(len(items)):
            if items[i].cantidad <= 0:
                raise ErrorInventario(f"la cantidad de {items[i].codigo_producto} debe ser mayor que cero")
            productos[i] = self.__obtener_producto(items[i].codigo_producto)
        for i in range(len(items)):
            # Si un producto aparece varias veces en el pedido, se suma todo lo pedido.
            pedido_total = 0
            for j in range(len(items)):
                if productos[j] is productos[i]:
                    pedido_total += items[j].cantidad
            if not productos[i].hay_stock(pedido_total):
                raise ErrorInventario(
                    f"stock insuficiente de '{productos[i].nombre}': "
                    f"hay {productos[i].stock} y se piden {pedido_total}")

        venta = Venta(self.__repositorio.contar_ventas() + 1, cliente.documento, _hoy())
        for i in range(len(items)):
            # El precio se copia al detalle (record): la venta conserva el precio de hoy.
            venta.agregar_detalle(
                DetalleVenta(productos[i].codigo, items[i].cantidad, productos[i].precio_venta))

        # 2. Registrar la venta y hacer salir la mercancía.
        self.__repositorio.guardar_venta(venta)
        for i in range(len(items)):
            productos[i].disminuir_stock(items[i].cantidad)
        return venta

    # Consultas
    def buscar_producto(self, codigo: str) -> Optional[Producto]:
        return self.__repositorio.buscar_producto(_normalizar_codigo(codigo))

    def buscar_proveedor(self, nit: str) -> Optional[Proveedor]:
        return self.__repositorio.buscar_proveedor(nit.strip())

    def buscar_cliente(self, documento: str) -> Optional[Cliente]:
        return self.__repositorio.buscar_cliente(documento.strip())

    def listar_productos(self) -> list[Producto]:
        return self.__repositorio.listar_productos()

    def listar_proveedores(self) -> list[Proveedor]:
        return self.__repositorio.listar_proveedores()

    def listar_clientes(self) -> list[Cliente]:
        return self.__repositorio.listar_clientes()

    def listar_ventas(self) -> list[Venta]:
        return self.__repositorio.listar_ventas()

    def reporte_ventas_por_producto(self) -> list[LineaReporte]:
        productos = self.__repositorio.listar_productos()
        lineas = [None] * len(productos)
        for i in range(len(productos)):
            lineas[i] = LineaReporte(productos[i].codigo, productos[i].nombre)

        for venta in self.__repositorio.listar_ventas():
            for detalle in venta.obtener_detalles():
                for linea in lineas:
                    if linea.codigo_producto == detalle.codigo_producto:
                        # LineaReporte es un struct mutable: se acumula en el mismo registro.
                        linea.unidades_vendidas += detalle.cantidad
                        linea.total_vendido += detalle.subtotal
                        break
        return lineas

    # Ayudantes privados
    def __obtener_producto(self, codigo: str) -> Producto:
        producto = self.buscar_producto(codigo)
        if producto is None:
            raise ErrorInventario(f"no existe un producto con el código {_normalizar_codigo(codigo)}")
        return producto

    def __obtener_proveedor(self, nit: str) -> Proveedor:
        proveedor = self.buscar_proveedor(nit)
        if proveedor is None:
            raise ErrorInventario(f"no existe un proveedor con el NIT {nit.strip()}")
        return proveedor

    def __obtener_cliente(self, documento: str) -> Cliente:
        cliente = self.buscar_cliente(documento)
        if cliente is None:
            raise ErrorInventario(f"no existe un cliente con el documento {documento.strip()}")
        return cliente
