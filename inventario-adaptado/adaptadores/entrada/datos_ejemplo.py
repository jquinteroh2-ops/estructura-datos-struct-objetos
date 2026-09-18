"""Datos ficticios de ejemplo, cargados a través del puerto de entrada."""

from puertos.entrada import CasosDeUsoInventario


def cargar_datos_de_ejemplo(casos: CasosDeUsoInventario) -> None:
    casos.registrar_producto("P001", "Arroz 500 g", 3200, 40)
    casos.registrar_producto("P002", "Aceite 1 L", 12500, 15)
    casos.registrar_producto("P003", "Panela 500 g", 3000, 25)
    casos.registrar_producto("P004", "Café molido 250 g", 9800, 10)
    casos.registrar_producto("P005", "Huevos AA x30", 18000, 8)

    casos.registrar_proveedor("900123456-1", "Distribuidora La Costa", "3001234567")
    casos.registrar_proveedor("800987654-3", "Granos del Caribe", "3109876543")

    casos.registrar_cliente("1047000001", "María Fernanda Ríos", "3151112233")
    casos.registrar_cliente("1047000002", "Carlos Andrés Mejía", "3204445566")
    casos.registrar_cliente("1047000003", "Valentina Torres", "3017778899")
