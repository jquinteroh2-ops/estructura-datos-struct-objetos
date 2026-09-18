"""
Objetos (clases e instancias) en Python - Estructura de Datos, Unidad 1.

Una CLASE es el molde que define los datos (atributos) y el comportamiento
(métodos) de sus objetos; cada OBJETO (instancia) tiene sus propios valores.

Los nombres mostrarInfo y setPromedio se escriben en camelCase porque así los
pide el enunciado de la actividad (en Python la convención PEP 8 sería
snake_case: mostrar_info, set_promedio).

Ejecución:
    python python/objetos.py
"""


# 1. Declaración
class Estudiante:
    """Estudiante con nombre, edad y promedio, y los métodos que operan sobre ellos.

    El promedio es un atributo privado (__promedio): desde fuera de la clase solo
    se lee con getPromedio().
    """

    def __init__(self, nombre: str, edad: int, promedio: float) -> None:
        self.nombre = nombre
        self.edad = edad
        self.__promedio = promedio

    def getPromedio(self) -> float:
        return self.__promedio

    def mostrarInfo(self) -> None:
        print(f"    {self.nombre:<14} | edad: {self.edad:>2} | promedio: {self.__promedio:.1f}")


def declaracion() -> None:
    print("\n1. Declaración")
    metodos = [nombre for nombre, valor in vars(Estudiante).items()
               if callable(valor) and not nombre.startswith("_")]
    print("  Clase Estudiante")
    print("    Atributos: nombre, edad, __promedio (privado)")
    print(f"    Métodos públicos: {', '.join(metodos)}")


# 2. Inicialización
def inicializacion() -> list[Estudiante]:
    """Crea 3 instancias de Estudiante y las guarda en un arreglo (lista)."""
    print("\n2. Inicialización (3 instancias guardadas en un arreglo)")
    estudiantes = [
        Estudiante("Ana Martínez", 19, 4.2),
        Estudiante("Luis Pérez", 21, 3.6),
        Estudiante("Sofía Gómez", 20, 4.7),
    ]
    print(f"  Se crearon {len(estudiantes)} objetos de tipo {type(estudiantes[0]).__name__}")
    # Una clase normal no genera __repr__ como @dataclass: al imprimir el objeto
    # se ve su tipo y su dirección en memoria, no sus datos.
    print(f"  print(estudiantes[0]) -> {estudiantes[0]}")
    print(f"  ¿Cada instancia es un objeto distinto? {estudiantes[0] is not estudiantes[1]}")
    return estudiantes


def main() -> None:
    print("=== OBJETOS (CLASES E INSTANCIAS) EN PYTHON ===")
    declaracion()
    inicializacion()


if __name__ == "__main__":
    main()
