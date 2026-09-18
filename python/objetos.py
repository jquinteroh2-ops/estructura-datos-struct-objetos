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


def main() -> None:
    print("=== OBJETOS (CLASES E INSTANCIAS) EN PYTHON ===")
    declaracion()


if __name__ == "__main__":
    main()
