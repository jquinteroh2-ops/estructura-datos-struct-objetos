"""
LineaReporte -> modelada como STRUCT (dataclass MUTABLE, sin frozen).

Por qué struct (y no record ni objeto):
  - Solo agrupa datos, sin reglas propias: por eso no es un objeto.
  - A diferencia de un record, SÍ necesita cambiar: mientras se recorren las
    ventas se van acumulando en la misma línea las unidades vendidas y el total
    de cada producto. Es un contenedor temporal que se arma para mostrar el
    reporte y luego se descarta.
"""

from dataclasses import dataclass


@dataclass
class LineaReporte:
    codigo_producto: str
    nombre_producto: str
    unidades_vendidas: int = 0
    total_vendido: int = 0
