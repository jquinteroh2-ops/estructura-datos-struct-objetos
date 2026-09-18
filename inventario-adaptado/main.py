"""
Inventario adaptado - Estructura de Datos, Unidad 1 (Struct/Record y Objetos).

Punto de entrada: arma la arquitectura hexagonal conectando los adaptadores con
el núcleo, y arranca el adaptador de entrada elegido.

Ejecución (desde la raíz del repositorio):
    python inventario-adaptado/main.py           # menú interactivo con datos de ejemplo
    python inventario-adaptado/main.py --demo    # demostración automática, sin escribir nada
    python inventario-adaptado/main.py --vacio   # menú interactivo sin datos de ejemplo
"""

import sys

from adaptadores.entrada.consola import ConsolaInventario
from adaptadores.entrada.datos_ejemplo import cargar_datos_de_ejemplo
from adaptadores.entrada.demo import DemoInventario
from adaptadores.salida.base_datos import BaseDatos
from adaptadores.salida.repositorio_arreglos import RepositorioArreglos
from aplicacion.servicio_inventario import ServicioInventario


def main() -> None:
    # Adaptador de salida -> puerto de salida -> núcleo -> puerto de entrada -> adaptador de entrada
    base_datos = BaseDatos()                          # struct con las tablas (arreglos)
    repositorio = RepositorioArreglos(base_datos)     # adaptador de salida
    servicio = ServicioInventario(repositorio)        # núcleo: casos de uso

    argumentos = sys.argv[1:]
    if "--demo" in argumentos:
        DemoInventario(servicio).ejecutar()
        return
    if "--vacio" not in argumentos:
        cargar_datos_de_ejemplo(servicio)
    ConsolaInventario(servicio).ejecutar()


if __name__ == "__main__":
    main()
