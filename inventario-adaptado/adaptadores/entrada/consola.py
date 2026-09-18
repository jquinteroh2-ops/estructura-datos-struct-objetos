"""
ConsolaInventario -> adaptador de ENTRADA por consola (menú interactivo).

Traduce lo que escribe el usuario en llamadas al puerto de entrada
(CasosDeUsoInventario) y muestra los resultados. No contiene reglas de negocio.
"""

from adaptadores.entrada import vistas
from dominio.compra import MAX_DETALLES_POR_COMPRA, DetalleCompra
from dominio.errores import ErrorInventario
from dominio.venta import MAX_DETALLES_POR_VENTA
from puertos.entrada import CasosDeUsoInventario, ItemPedido

MENU = """
  1. Registrar producto
  2. Registrar proveedor
  3. Registrar cliente
  4. Registrar compra a proveedor (entrada de mercancía)
  5. Registrar venta a cliente (salida de mercancía)
  6. Ver inventario de productos
  7. Ver proveedores
  8. Ver clientes
  9. Ver ventas
 10. Reporte de ventas por producto
 11. Actualizar teléfono de un cliente
  0. Salir"""


class ConsolaInventario:

    def __init__(self, casos: CasosDeUsoInventario) -> None:
        self.__casos = casos
        self.__opciones = {
            1: self.__registrar_producto,
            2: self.__registrar_proveedor,
            3: self.__registrar_cliente,
            4: self.__registrar_compra,
            5: self.__registrar_venta,
            6: lambda: vistas.mostrar_productos(self.__casos.listar_productos()),
            7: lambda: vistas.mostrar_proveedores(self.__casos.listar_proveedores()),
            8: lambda: vistas.mostrar_clientes(self.__casos.listar_clientes()),
            9: self.__ver_ventas,
            10: lambda: vistas.mostrar_reporte(self.__casos.reporte_ventas_por_producto()),
            11: self.__actualizar_telefono,
        }

    def ejecutar(self) -> None:
        try:
            while True:
                vistas.titulo("INVENTARIO - Struct/Record y Objetos")
                print(MENU)
                opcion = self.__leer_entero("\n  Opción: ", 0)
                if opcion == 0:
                    print("  Hasta luego.")
                    return
                accion = self.__opciones.get(opcion)
                if accion is None:
                    print("  Opción no válida.")
                    continue
                try:
                    accion()
                except ErrorInventario as error:
                    print(f"\n  ERROR: {error}")
                input("\n  Presione Enter para continuar...")
        except (EOFError, KeyboardInterrupt):
            print("\n  Programa terminado.")

    # Opciones del menú
    def __registrar_producto(self) -> None:
        codigo = self.__leer_texto("  Código: ")
        nombre = self.__leer_texto("  Nombre: ")
        precio = self.__leer_pesos("  Precio de venta: ")
        stock = self.__leer_entero("  Stock inicial: ", 0)
        producto = self.__casos.registrar_producto(codigo, nombre, precio, stock)
        print(f"\n  Producto {producto.codigo} registrado.")

    def __registrar_proveedor(self) -> None:
        nit = self.__leer_texto("  NIT: ")
        nombre = self.__leer_texto("  Nombre: ")
        telefono = self.__leer_texto("  Teléfono: ")
        proveedor = self.__casos.registrar_proveedor(nit, nombre, telefono)
        print(f"\n  Proveedor {proveedor.nombre} registrado.")

    def __registrar_cliente(self) -> None:
        documento = self.__leer_texto("  Documento: ")
        nombre = self.__leer_texto("  Nombre: ")
        telefono = self.__leer_texto("  Teléfono: ")
        cliente = self.__casos.registrar_cliente(documento, nombre, telefono)
        print(f"\n  Cliente registrado: {cliente}")

    def __registrar_compra(self) -> None:
        vistas.mostrar_proveedores(self.__casos.listar_proveedores())
        nit = self.__leer_texto("  NIT del proveedor: ")
        if self.__casos.buscar_proveedor(nit) is None:
            raise ErrorInventario(f"no existe un proveedor con el NIT {nit}")
        n = self.__leer_entero("  ¿Cuántos productos distintos trae la compra? ", 1, MAX_DETALLES_POR_COMPRA)
        detalles = [None] * n
        for i in range(n):
            print(f"  Producto {i + 1} de {n}")
            codigo = self.__leer_texto("    Código: ").upper()
            cantidad = self.__leer_entero("    Cantidad: ", 1)
            costo = self.__leer_pesos("    Costo unitario: ")
            detalles[i] = DetalleCompra(codigo, cantidad, costo)
        compra = self.__casos.registrar_compra(nit, detalles)
        print()
        vistas.mostrar_compra(compra, self.__casos)

    def __registrar_venta(self) -> None:
        vistas.mostrar_clientes(self.__casos.listar_clientes())
        documento = self.__leer_texto("  Documento del cliente: ")
        if self.__casos.buscar_cliente(documento) is None:
            raise ErrorInventario(f"no existe un cliente con el documento {documento}")
        vistas.mostrar_productos(self.__casos.listar_productos())
        n = self.__leer_entero("  ¿Cuántos productos distintos lleva? ", 1, MAX_DETALLES_POR_VENTA)
        items = [None] * n
        for i in range(n):
            print(f"  Producto {i + 1} de {n}")
            codigo = self.__leer_texto("    Código: ").upper()
            cantidad = self.__leer_entero("    Cantidad: ", 1)
            items[i] = ItemPedido(codigo, cantidad)
        venta = self.__casos.registrar_venta(documento, items)
        print()
        vistas.mostrar_venta(venta, self.__casos)

    def __ver_ventas(self) -> None:
        ventas = self.__casos.listar_ventas()
        if len(ventas) == 0:
            print("  (sin ventas registradas)")
        for venta in ventas:
            print()
            vistas.mostrar_venta(venta, self.__casos)

    def __actualizar_telefono(self) -> None:
        vistas.mostrar_clientes(self.__casos.listar_clientes())
        documento = self.__leer_texto("  Documento del cliente: ")
        telefono = self.__leer_texto("  Nuevo teléfono: ")
        cliente = self.__casos.actualizar_telefono_cliente(documento, telefono)
        print(f"\n  Cliente actualizado (record nuevo): {cliente}")

    # Lectura de datos con validación
    @staticmethod
    def __leer_texto(mensaje: str) -> str:
        while True:
            texto = input(mensaje).strip()
            if texto:
                return texto
            print("    Este dato es obligatorio.")

    @staticmethod
    def __leer_entero(mensaje: str, minimo: int, maximo: int = None) -> int:
        while True:
            texto = input(mensaje).strip()
            try:
                valor = int(texto)
            except ValueError:
                print("    Escriba un número entero.")
                continue
            if valor < minimo or (maximo is not None and valor > maximo):
                limite = f"entre {minimo} y {maximo}" if maximo is not None else f"mayor o igual a {minimo}"
                print(f"    El valor debe ser {limite}.")
                continue
            return valor

    @staticmethod
    def __leer_pesos(mensaje: str) -> int:
        """Acepta valores como 12500, 12.500 o $12.500."""
        while True:
            texto = input(mensaje).strip().replace("$", "").replace(".", "")
            try:
                valor = int(texto)
            except ValueError:
                print("    Escriba el valor en pesos, sin decimales (por ejemplo 12500).")
                continue
            if valor <= 0:
                print("    El valor debe ser mayor que cero.")
                continue
            return valor
