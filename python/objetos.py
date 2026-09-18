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
    se lee con getPromedio() y solo se cambia con setPromedio(), que valida que
    la nota esté en la escala de 0.0 a 5.0.
    """

    PROMEDIO_MINIMO = 0.0
    PROMEDIO_MAXIMO = 5.0

    def __init__(self, nombre: str, edad: int, promedio: float) -> None:
        self.nombre = nombre
        self.edad = edad
        self.__promedio = 0.0
        self.setPromedio(promedio)  # el constructor reutiliza la misma validación

    def getPromedio(self) -> float:
        return self.__promedio

    # 4. Modificación
    def setPromedio(self, nuevo_promedio: float) -> None:
        if not Estudiante.PROMEDIO_MINIMO <= nuevo_promedio <= Estudiante.PROMEDIO_MAXIMO:
            raise ValueError(
                f"promedio inválido ({nuevo_promedio}): debe estar entre "
                f"{Estudiante.PROMEDIO_MINIMO} y {Estudiante.PROMEDIO_MAXIMO}"
            )
        self.__promedio = nuevo_promedio

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


# 3. Recorrido
def recorrido(estudiantes: list[Estudiante], titulo: str = "3. Recorrido: mostrarInfo() de cada objeto") -> None:
    print(f"\n{titulo}")
    # Cada objeto sabe mostrarse a sí mismo: el recorrido solo le envía el mensaje.
    for estudiante in estudiantes:
        estudiante.mostrarInfo()


# 4. Modificación
def buscar_por_nombre(estudiantes: list[Estudiante], nombre: str) -> int:
    """Búsqueda lineal: devuelve la posición del estudiante o -1 si no está."""
    for i in range(len(estudiantes)):
        if estudiantes[i].nombre == nombre:
            return i
    return -1


def modificacion(estudiantes: list[Estudiante]) -> None:
    nombre, nuevo_promedio = "Luis Pérez", 4.1
    print(f"\n4. Modificación con setPromedio() (promedio de {nombre} a {nuevo_promedio})")
    luis = estudiantes[buscar_por_nombre(estudiantes, nombre)]
    print(f"  Antes:   getPromedio() = {luis.getPromedio()}")
    luis.setPromedio(nuevo_promedio)
    print(f"  Después: getPromedio() = {luis.getPromedio()}")

    print("  a) El método valida el dato: setPromedio(7.5) se rechaza")
    try:
        luis.setPromedio(7.5)
    except ValueError as error:
        print(f"    ValueError: {error}")
    print(f"    El promedio sigue siendo {luis.getPromedio()}")

    print("  b) El atributo es privado: leer luis.__promedio desde fuera falla")
    try:
        print(luis.__promedio)
    except AttributeError as error:
        print(f"    AttributeError: {error}")


def main() -> None:
    print("=== OBJETOS (CLASES E INSTANCIAS) EN PYTHON ===")
    declaracion()
    estudiantes = inicializacion()
    recorrido(estudiantes)
    modificacion(estudiantes)
    recorrido(estudiantes, "Arreglo después de la modificación")


if __name__ == "__main__":
    main()
