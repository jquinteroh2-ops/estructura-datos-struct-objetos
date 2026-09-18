"""Errores de negocio del inventario."""


class ErrorInventario(Exception):
    """Se lanza cuando una operación viola una regla del inventario
    (stock insuficiente, código repetido, arreglo lleno, etc.)."""
