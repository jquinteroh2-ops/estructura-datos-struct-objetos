"""
Proveedor -> modelado como OBJETO.

Por qué objeto y no struct/record:
  - Además de sus datos, administra su PROPIO ARREGLO de compras, como en la
    versión original en Java: un arreglo de tamaño fijo más un contador de
    posiciones ocupadas.
  - Tiene que controlar que no se exceda la capacidad del arreglo y entregar sus
    compras sin dejar que desde fuera se modifique el arreglo interno. Esas
    responsabilidades son comportamiento, y un struct no lo tiene.
"""

from dominio.compra import Compra
from dominio.errores import ErrorInventario

MAX_COMPRAS_POR_PROVEEDOR = 50


class Proveedor:
    """Proveedor de mercancía con su historial de compras."""

    def __init__(self, nit: str, nombre: str, telefono: str) -> None:
        self.__nit = nit
        self.__nombre = nombre
        self.__telefono = telefono
        # Arreglo de tamaño fijo: todas las posiciones existen desde el inicio (None = vacía).
        self.__compras = [None] * MAX_COMPRAS_POR_PROVEEDOR
        self.__total_compras = 0

    @property
    def nit(self) -> str:
        return self.__nit

    @property
    def nombre(self) -> str:
        return self.__nombre

    @property
    def telefono(self) -> str:
        return self.__telefono

    @property
    def total_compras(self) -> int:
        return self.__total_compras

    def puede_registrar_compra(self) -> bool:
        return self.__total_compras < len(self.__compras)

    def registrar_compra(self, compra: Compra) -> None:
        if not self.puede_registrar_compra():
            raise ErrorInventario(
                f"el proveedor {self.__nombre} alcanzó el máximo de {len(self.__compras)} compras"
            )
        self.__compras[self.__total_compras] = compra
        self.__total_compras += 1

    def obtener_compras(self) -> list[Compra]:
        """Devuelve un arreglo NUEVO con las compras registradas (copia elemento por elemento),
        para que nadie pueda alterar el arreglo interno del proveedor."""
        copia = [None] * self.__total_compras
        for i in range(self.__total_compras):
            copia[i] = self.__compras[i]
        return copia

    def total_comprado(self) -> int:
        total = 0
        for i in range(self.__total_compras):
            total += self.__compras[i].calcular_total()
        return total
