"""Funciones de presentación en consola, compartidas por el menú y la demostración."""

from dominio.cliente import Cliente
from dominio.compra import Compra
from dominio.producto import Producto
from dominio.proveedor import Proveedor
from dominio.reporte import LineaReporte
from dominio.venta import Venta
from puertos.entrada import CasosDeUsoInventario


def pesos(valor: int) -> str:
    """Formato de moneda colombiana: 12500 -> $12.500"""
    return f"${valor:,}".replace(",", ".")


def titulo(texto: str) -> None:
    print(f"\n{'=' * 70}\n  {texto}\n{'=' * 70}")


def imprimir_tabla(encabezados: list, filas: list, derecha: tuple = ()) -> None:
    """Imprime una tabla con bordes. `derecha` son las columnas alineadas a la derecha."""
    if len(filas) == 0:
        print("  (sin registros)")
        return
    anchos = [len(e) for e in encabezados]
    for fila in filas:
        for i in range(len(fila)):
            anchos[i] = max(anchos[i], len(str(fila[i])))

    def linea(celdas) -> str:
        partes = [str(c).rjust(anchos[i]) if i in derecha else str(c).ljust(anchos[i])
                  for i, c in enumerate(celdas)]
        return "  | " + " | ".join(partes) + " |"

    borde = "  +" + "+".join("-" * (a + 2) for a in anchos) + "+"
    print(borde)
    print(linea(encabezados))
    print(borde)
    for fila in filas:
        print(linea(fila))
    print(borde)


def mostrar_productos(productos: list[Producto]) -> None:
    filas = [(p.codigo, p.nombre, pesos(p.precio_venta), p.stock, pesos(p.valor_en_inventario()))
             for p in productos]
    imprimir_tabla(["Código", "Producto", "Precio", "Stock", "Valor en inventario"], filas, (2, 3, 4))
    total = 0
    for producto in productos:
        total += producto.valor_en_inventario()
    print(f"  Valor total del inventario: {pesos(total)}")


def mostrar_proveedores(proveedores: list[Proveedor]) -> None:
    filas = [(p.nit, p.nombre, p.telefono, p.total_compras, pesos(p.total_comprado()))
             for p in proveedores]
    imprimir_tabla(["NIT", "Proveedor", "Teléfono", "Compras", "Total comprado"], filas, (3, 4))


def mostrar_clientes(clientes: list[Cliente]) -> None:
    filas = [(c.documento, c.nombre, c.telefono) for c in clientes]
    imprimir_tabla(["Documento", "Cliente", "Teléfono"], filas)


def _nombre_producto(casos: CasosDeUsoInventario, codigo: str) -> str:
    producto = casos.buscar_producto(codigo)
    return producto.nombre if producto is not None else "?"


def mostrar_compra(compra: Compra, casos: CasosDeUsoInventario) -> None:
    proveedor = casos.buscar_proveedor(compra.nit_proveedor)
    print(f"  Compra #{compra.numero} | Proveedor: {proveedor.nombre} (NIT {proveedor.nit})"
          f" | Fecha: {compra.fecha}")
    filas = [(d.codigo_producto, _nombre_producto(casos, d.codigo_producto), d.cantidad,
              pesos(d.costo_unitario), pesos(d.subtotal)) for d in compra.obtener_detalles()]
    imprimir_tabla(["Código", "Producto", "Cantidad", "Costo unitario", "Subtotal"], filas, (2, 3, 4))
    print(f"  Total de la compra: {pesos(compra.calcular_total())}")


def mostrar_venta(venta: Venta, casos: CasosDeUsoInventario) -> None:
    cliente = casos.buscar_cliente(venta.documento_cliente)
    print(f"  Venta #{venta.numero} | Cliente: {cliente.nombre} (doc. {cliente.documento})"
          f" | Fecha: {venta.fecha}")
    filas = [(d.codigo_producto, _nombre_producto(casos, d.codigo_producto), d.cantidad,
              pesos(d.precio_unitario), pesos(d.subtotal)) for d in venta.obtener_detalles()]
    imprimir_tabla(["Código", "Producto", "Cantidad", "Precio unitario", "Subtotal"], filas, (2, 3, 4))
    print(f"  Total de la venta: {pesos(venta.calcular_total())}")


def mostrar_reporte(lineas: list[LineaReporte]) -> None:
    filas = [(l.codigo_producto, l.nombre_producto, l.unidades_vendidas, pesos(l.total_vendido))
             for l in lineas]
    imprimir_tabla(["Código", "Producto", "Unidades vendidas", "Total vendido"], filas, (2, 3))
    total = 0
    for linea in lineas:
        total += linea.total_vendido
    print(f"  Total vendido: {pesos(total)}")
