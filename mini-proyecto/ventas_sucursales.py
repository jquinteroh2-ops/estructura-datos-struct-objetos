"""
Mini-proyecto integrador - Estructura de Datos, Unidad 1.

Arreglo de OBJETOS en el que cada objeto tiene un campo que es a su vez una
MATRIZ: cada Producto guarda las unidades vendidas en una matriz ventas[mes][sucursal].
La misma solución está en mini-proyecto/ventas_sucursales.js para comparar la
sintaxis y el paradigma de Python y JavaScript (la salida es la misma).

Ejecución:
    python mini-proyecto/ventas_sucursales.py
"""

MESES = ["Enero", "Febrero", "Marzo", "Abril"]
SUCURSALES = ["Centro", "Bocagrande", "Manga"]

# Datos ficticios: (código, nombre, precio, unidades vendidas [mes][sucursal]).
DATOS = [
    ("P001", "Arroz 500 g", 3200, [[120, 95, 80], [110, 100, 85], [130, 90, 95], [115, 100, 88]]),
    ("P002", "Aceite 1 L", 12500, [[40, 55, 30], [35, 60, 28], [45, 50, 33], [38, 65, 31]]),
    ("P004", "Café molido 250 g", 9800, [[60, 80, 45], [58, 85, 50], [62, 78, 47], [70, 90, 52]]),
]


def pesos(valor: int) -> str:
    return f"${valor:,}".replace(",", ".")


class Producto:
    """Objeto cuyo campo `ventas` es una matriz de MESES x SUCURSALES."""

    def __init__(self, codigo: str, nombre: str, precio: int) -> None:
        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio
        # Una fila NUEVA por mes. Ojo: [[0] * 3] * 4 repetiría la MISMA fila 4 veces.
        self.ventas = [[0] * len(SUCURSALES) for _ in range(len(MESES))]

    def registrar_venta(self, mes: int, sucursal: int, unidades: int) -> None:
        if not (0 <= mes < len(MESES) and 0 <= sucursal < len(SUCURSALES)):
            raise IndexError(f"posición inválida ventas[{mes}][{sucursal}]")
        if unidades <= 0:
            raise ValueError("las unidades deben ser mayores que cero")
        self.ventas[mes][sucursal] += unidades

    def total_por_mes(self, mes: int) -> int:
        """Suma de una FILA de la matriz."""
        return sum(self.ventas[mes])

    def total_por_sucursal(self, sucursal: int) -> int:
        """Suma de una COLUMNA de la matriz."""
        total = 0
        for mes in range(len(MESES)):
            total += self.ventas[mes][sucursal]
        return total

    def total_unidades(self) -> int:
        total = 0
        for fila in self.ventas:
            for unidades in fila:
                total += unidades
        return total

    def mejor_mes(self) -> int:
        mejor = 0
        for mes in range(1, len(MESES)):
            if self.total_por_mes(mes) > self.total_por_mes(mejor):
                mejor = mes
        return mejor

    def ingresos(self) -> int:
        return self.total_unidades() * self.precio


def imprimir_matriz(matriz: list[list[int]]) -> None:
    """Imprime la matriz como tabla, con el total de cada fila y de cada columna."""
    print("    " + "".ljust(9) + "".join(s.rjust(12) for s in SUCURSALES) + "Total".rjust(9))
    totales_columna = [0] * len(SUCURSALES)
    for mes in range(len(MESES)):
        fila = matriz[mes]
        for sucursal in range(len(SUCURSALES)):
            totales_columna[sucursal] += fila[sucursal]
        celdas = "".join(str(unidades).rjust(12) for unidades in fila)
        print(f"    {MESES[mes]:<9}{celdas}{str(sum(fila)).rjust(9)}")
    celdas = "".join(str(total).rjust(12) for total in totales_columna)
    print(f"    {'Total':<9}{celdas}{str(sum(totales_columna)).rjust(9)}")


def crear_productos() -> list[Producto]:
    print("\n1. Arreglo de objetos: cada Producto tiene una matriz ventas[mes][sucursal]")
    productos = [None] * len(DATOS)
    for i in range(len(DATOS)):
        codigo, nombre, precio, unidades = DATOS[i]
        producto = Producto(codigo, nombre, precio)
        for mes in range(len(MESES)):
            for sucursal in range(len(SUCURSALES)):
                producto.registrar_venta(mes, sucursal, unidades[mes][sucursal])
        productos[i] = producto
    print(f"  {len(productos)} productos, cada uno con una matriz de {len(MESES)} meses x {len(SUCURSALES)} sucursales")
    return productos


def recorrer(productos: list[Producto]) -> None:
    print("\n2. Recorrido: la matriz de cada objeto del arreglo")
    for producto in productos:
        print(f"\n  {producto.codigo} - {producto.nombre} ({pesos(producto.precio)} c/u)")
        imprimir_matriz(producto.ventas)


def totales(productos: list[Producto]) -> None:
    print("\n3. Totales por producto")
    mas_vendido = productos[0]
    for producto in productos:
        print(f"  {producto.nombre:<18} unidades: {producto.total_unidades():>5} | ingresos: "
              f"{pesos(producto.ingresos()):>11} | mejor mes: {MESES[producto.mejor_mes()]}")
        if producto.total_unidades() > mas_vendido.total_unidades():
            mas_vendido = producto
    print(f"  Producto más vendido: {mas_vendido.nombre} ({mas_vendido.total_unidades()} unidades)")


def consolidado(productos: list[Producto]) -> None:
    print("\n4. Matriz consolidada (suma de las matrices de todos los productos)")
    matriz = [[0] * len(SUCURSALES) for _ in range(len(MESES))]
    for producto in productos:
        for mes in range(len(MESES)):
            for sucursal in range(len(SUCURSALES)):
                matriz[mes][sucursal] += producto.ventas[mes][sucursal]
    imprimir_matriz(matriz)

    mejor = 0
    for sucursal in range(1, len(SUCURSALES)):
        if sum(fila[sucursal] for fila in matriz) > sum(fila[mejor] for fila in matriz):
            mejor = sucursal
    print(f"  Sucursal con más unidades vendidas: {SUCURSALES[mejor]}")


def modificar(productos: list[Producto]) -> None:
    mes, sucursal, unidades = 3, 2, 20
    producto = productos[1]
    print(f"\n5. Modificación: registrar {unidades} unidades más de {producto.nombre}"
          f" en {MESES[mes]} / {SUCURSALES[sucursal]}")
    print(f"  Antes:   ventas[{mes}][{sucursal}] = {producto.ventas[mes][sucursal]}"
          f" | total del producto = {producto.total_unidades()}")
    producto.registrar_venta(mes, sucursal, unidades)
    print(f"  Después: ventas[{mes}][{sucursal}] = {producto.ventas[mes][sucursal]}"
          f" | total del producto = {producto.total_unidades()}")
    try:
        producto.registrar_venta(4, 0, 10)
    except IndexError as error:
        print(f"  registrar_venta(4, 0, 10) -> IndexError: {error}")


def main() -> None:
    print("=== MINI-PROYECTO: VENTAS POR MES Y SUCURSAL (PYTHON) ===")
    productos = crear_productos()
    recorrer(productos)
    totales(productos)
    consolidado(productos)
    modificar(productos)


if __name__ == "__main__":
    main()
