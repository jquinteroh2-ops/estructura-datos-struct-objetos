"""
DemoInventario -> adaptador de ENTRADA automático.

Recorre un escenario completo usando el mismo puerto de entrada que el menú, sin
que el usuario tenga que escribir nada. Que existan dos adaptadores de entrada
distintos (menú y demo) para el mismo núcleo es una de las ventajas de la
arquitectura hexagonal.
"""

from dataclasses import FrozenInstanceError

from adaptadores.entrada import vistas
from adaptadores.entrada.datos_ejemplo import cargar_datos_de_ejemplo
from dominio.compra import DetalleCompra
from dominio.errores import ErrorInventario
from puertos.entrada import CasosDeUsoInventario, ItemPedido


class DemoInventario:

    def __init__(self, casos: CasosDeUsoInventario) -> None:
        self.__casos = casos

    def ejecutar(self) -> None:
        casos = self.__casos
        cargar_datos_de_ejemplo(casos)

        vistas.titulo("1. Datos iniciales guardados en los arreglos de BaseDatos")
        print("  Productos (OBJETOS: protegen su precio y su stock):")
        vistas.mostrar_productos(casos.listar_productos())
        print("\n  Proveedores (OBJETOS: cada uno tiene su propio arreglo de compras):")
        vistas.mostrar_proveedores(casos.listar_proveedores())
        print("\n  Clientes (RECORDS inmutables: solo datos):")
        vistas.mostrar_clientes(casos.listar_clientes())

        vistas.titulo("2. Compra a un proveedor (Compra = OBJETO, DetalleCompra = RECORD)")
        compra = casos.registrar_compra("900123456-1", [
            DetalleCompra("P001", 20, 2400),
            DetalleCompra("P002", 10, 9800),
        ])
        vistas.mostrar_compra(compra, casos)
        proveedor = casos.buscar_proveedor("900123456-1")
        print(f"  El proveedor {proveedor.nombre} ya tiene {proveedor.total_compras} compra(s)"
              " en su propio arreglo.")
        print(f"  Stock después de la compra: P001 = {casos.buscar_producto('P001').stock},"
              f" P002 = {casos.buscar_producto('P002').stock}")

        vistas.titulo("3. Ventas a clientes (Venta = OBJETO, DetalleVenta = RECORD)")
        venta = casos.registrar_venta("1047000001", [
            ItemPedido("P001", 5), ItemPedido("P004", 2), ItemPedido("P005", 1),
        ])
        vistas.mostrar_venta(venta, casos)
        print()
        venta = casos.registrar_venta("1047000002", [ItemPedido("P002", 3), ItemPedido("P001", 10)])
        vistas.mostrar_venta(venta, casos)

        vistas.titulo("4. Venta con stock insuficiente (el objeto Producto protege su stock)")
        stock_antes = casos.buscar_producto("P003").stock
        try:
            casos.registrar_venta("1047000003", [ItemPedido("P003", 2), ItemPedido("P005", 50)])
        except ErrorInventario as error:
            print(f"  Venta rechazada: {error}")
        print(f"  El stock de P003 sigue en {casos.buscar_producto('P003').stock}"
              f" (antes: {stock_antes}): la venta se validó completa antes de modificar nada.")

        vistas.titulo("5. Un RECORD no se puede modificar")
        detalle = compra.obtener_detalles()[0]
        print(f"  {detalle}")
        try:
            detalle.cantidad = 999
        except FrozenInstanceError as error:
            print(f"  detalle.cantidad = 999 -> FrozenInstanceError: {error}")

        vistas.titulo("6. Actualizar el teléfono de un cliente (RECORD: se crea uno nuevo)")
        antes = casos.buscar_cliente("1047000003")
        despues = casos.actualizar_telefono_cliente("1047000003", "3005550000")
        print(f"  Antes:   {antes}")
        print(f"  Después: {despues}")
        print(f"  ¿Es el mismo objeto en memoria? {antes is despues}"
              " -> el arreglo de clientes guarda ahora el record nuevo")

        vistas.titulo("7. Reporte de ventas por producto (LineaReporte = STRUCT mutable)")
        vistas.mostrar_reporte(casos.reporte_ventas_por_producto())

        vistas.titulo("8. Inventario final")
        vistas.mostrar_productos(casos.listar_productos())
        print()
        vistas.mostrar_proveedores(casos.listar_proveedores())
