# Inventario adaptado — Struct/Record y Objetos

Adaptación del ejercicio de inventario del **Protocolo Individual de la Unidad 1** (originalmente
en Java puro, sin librerías ni `ArrayList`) a **Python**, aplicando explícitamente los conceptos de
**struct**, **record** y **objeto** como elementos guardados en los arreglos.

Se conserva la idea original:

- Clases `Producto`, `Proveedor` (con su propio arreglo de compras), `Cliente`,
  `Compra`/`DetalleCompra` y `Venta`/`DetalleVenta`.
- Una `BaseDatos` con **arreglos de tamaño fijo como si fueran tablas**, cada uno con un contador
  de posiciones ocupadas. No se usan `append`, `remove` ni diccionarios para guardar los datos:
  se escribe en la posición del contador y se busca con búsqueda lineal, como en Java.
- **Arquitectura hexagonal** (puertos y adaptadores de entrada y salida).
- Sin dependencias externas: solo la librería estándar (`dataclasses`, `abc`, `datetime`).

## Cómo ejecutar

Desde la raíz del repositorio (Python 3.9 o superior):

```bash
python inventario-adaptado/main.py --demo    # demostración automática, sin escribir nada
python inventario-adaptado/main.py           # menú interactivo con datos de ejemplo
python inventario-adaptado/main.py --vacio   # menú interactivo sin datos de ejemplo
```

La demostración recorre: datos iniciales → compra a un proveedor → ventas a clientes → venta
rechazada por stock insuficiente → intento de modificar un record → actualización del teléfono de
un cliente (record nuevo) → reporte de ventas por producto → inventario final.

## ¿Struct, record u objeto? Decisión por clase

| Clase | Modelo | Declaración en Python | Por qué |
|---|---|---|---|
| `Producto` | **Objeto** | `class` con atributos privados y propiedades de solo lectura | Tiene reglas que proteger (precio > 0, stock nunca negativo) y su estado cambia con compras y ventas; esos cambios solo ocurren por sus métodos `aumentar_stock()` y `disminuir_stock()`, que validan. |
| `Proveedor` | **Objeto** | `class` | Administra su **propio arreglo de compras** (tamaño fijo + contador): controla la capacidad, registra compras y las entrega como copia para que nadie altere el arreglo interno. Eso es comportamiento. |
| `Cliente` | **Record** | `@dataclass(frozen=True)` | Solo datos de identificación y contacto, sin reglas propias. Inmutable para que nadie cambie por accidente el documento; si cambia el teléfono se crea un record nuevo con `replace()` y se reemplaza en el arreglo. |
| `Compra` | **Objeto** | `class` | Guarda sus detalles en un arreglo de tamaño fijo, controla que no se llene y calcula su total recorriéndolo. |
| `DetalleCompra` | **Record** | `@dataclass(frozen=True)` | Una línea de la compra: un hecho histórico que no debe cambiar. Su `subtotal` es un dato derivado de sus campos (propiedad de solo lectura), no un comportamiento que cambie estado. |
| `Venta` | **Objeto** | `class` | Igual que `Compra`: arreglo propio de detalles, control de capacidad y cálculo del total. |
| `DetalleVenta` | **Record** | `@dataclass(frozen=True)` | Guarda el precio del **momento de la venta**; si luego cambia el precio del producto, la venta ya hecha no debe cambiar. La inmutabilidad lo garantiza. |
| `LineaReporte` | **Struct** | `@dataclass` (mutable) | Solo datos, pero **sí debe cambiar**: al recorrer las ventas se acumulan en la misma línea las unidades y el total de cada producto. Es un contenedor temporal para el reporte. |
| `ItemPedido` | **Record** | `@dataclass(frozen=True)` | Dato de entrada de una venta (producto y cantidad) que viaja del adaptador al núcleo; al ser inmutable nadie lo altera en el camino. |
| `BaseDatos` | **Struct** | `@dataclass` (mutable) | Solo agrupa las tablas (arreglos) y sus contadores; no decide ni valida nada. Quien inserta, busca y recorre es el adaptador `RepositorioArreglos`. |
| `RepositorioArreglos` | **Objeto** | `class` que implementa el puerto de salida | Tiene el comportamiento de almacenamiento: insertar en la posición del contador, búsqueda lineal y copia de arreglos. |
| `ServicioInventario` | **Objeto** | `class` que implementa el puerto de entrada | Contiene los casos de uso: valida cada compra o venta **completa** antes de modificar el inventario. |

**Regla usada para decidir:** si el dato tiene **reglas o acciones propias** → objeto. Si solo son
datos que **no deben cambiar** → record. Si solo son datos que **sí cambian** y no tienen reglas →
struct.

## Arquitectura hexagonal

```
                 ADAPTADORES DE ENTRADA                          ADAPTADOR DE SALIDA
          ┌──────────────────────────────┐              ┌──────────────────────────────┐
          │ ConsolaInventario (menú)     │              │ RepositorioArreglos          │
          │ DemoInventario (automático)  │              │   └─ BaseDatos (arreglos)    │
          └──────────────┬───────────────┘              └──────────────▲───────────────┘
                         │ usa                                         │ implementa
          ┌──────────────▼───────────────┐              ┌──────────────┴───────────────┐
          │ Puerto de entrada            │              │ Puerto de salida             │
          │ CasosDeUsoInventario (ABC)   │              │ RepositorioInventario (ABC)  │
          └──────────────┬───────────────┘              └──────────────▲───────────────┘
                         │ implementa                                  │ usa
                         └──────────► ServicioInventario ──────────────┘
                                             │ usa
                                        ┌────▼────┐
                                        │ DOMINIO │  Producto, Proveedor, Cliente, Compra,
                                        └─────────┘  DetalleCompra, Venta, DetalleVenta, LineaReporte
```

- Los **puertos** son clases abstractas (`abc.ABC` + `@abstractmethod`), el equivalente en Python
  a las `interface` de Java.
- El núcleo (`ServicioInventario` y el dominio) **no sabe** que los datos están en arreglos ni que
  hay una consola: solo conoce los puertos. Se podría cambiar `RepositorioArreglos` por uno que
  guarde en archivos sin tocar el núcleo.
- Hay **dos adaptadores de entrada** para el mismo núcleo (menú y demo), lo que muestra la ventaja
  de separar la entrada de la lógica.

## Estructura

```
inventario-adaptado/
  main.py                              -> arma la arquitectura y arranca el adaptador de entrada
  dominio/
    errores.py                         -> ErrorInventario
    producto.py                        -> Producto (objeto)
    proveedor.py                       -> Proveedor (objeto con arreglo propio de compras)
    cliente.py                         -> Cliente (record)
    compra.py                          -> DetalleCompra (record) y Compra (objeto)
    venta.py                           -> DetalleVenta (record) y Venta (objeto)
    reporte.py                         -> LineaReporte (struct)
  puertos/
    entrada.py                         -> ItemPedido (record) y CasosDeUsoInventario (interfaz)
    salida.py                          -> RepositorioInventario (interfaz)
  aplicacion/
    servicio_inventario.py             -> ServicioInventario (casos de uso)
  adaptadores/
    entrada/consola.py                 -> menú interactivo
    entrada/demo.py                    -> demostración automática
    entrada/vistas.py                  -> tablas y formatos de consola
    entrada/datos_ejemplo.py           -> datos ficticios de ejemplo
    salida/base_datos.py               -> BaseDatos (struct con los arreglos-tabla)
    salida/repositorio_arreglos.py     -> RepositorioArreglos (implementa el puerto de salida)
```

## ¿Por qué Python y no JavaScript?

Los dos lenguajes permiten simular arreglos de tamaño fijo (`[None] * n` en Python,
`new Array(n).fill(null)` en JavaScript). Se eligió Python porque conserva mejor los conceptos del
original en Java sin usar librerías externas:

- Tiene **records y structs reales** en la librería estándar: `@dataclass(frozen=True)` verifica la
  inmutabilidad al ejecutar (lanza `FrozenInstanceError`), y `@dataclass` da el struct mutable. En
  JavaScript el struct es solo una convención (un objeto plano).
- Tiene **clases abstractas** (`abc`) para declarar los puertos como las `interface` de Java.
