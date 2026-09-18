/**
 * Objetos (clases e instancias) en JavaScript - Estructura de Datos, Unidad 1.
 *
 * Desde ES2015 JavaScript tiene la palabra reservada `class`, que define el
 * molde de los objetos: sus datos (campos) y su comportamiento (métodos).
 * Desde ES2022 los campos que empiezan por # son PRIVADOS de verdad: el lenguaje
 * no permite leerlos ni escribirlos desde fuera de la clase.
 *
 * Ejecución:
 *   node js/objetos.js
 */

'use strict';

// 1. Declaración
class Estudiante {
  static PROMEDIO_MINIMO = 0.0;
  static PROMEDIO_MAXIMO = 5.0;

  /** Campo privado: solo se lee con getPromedio() y solo se cambia con setPromedio(). */
  #promedio = 0.0;

  constructor(nombre, edad, promedio) {
    this.nombre = nombre;
    this.edad = edad;
    this.setPromedio(promedio); // el constructor reutiliza la misma validación
  }

  getPromedio() {
    return this.#promedio;
  }

  // 4. Modificación
  setPromedio(nuevoPromedio) {
    // typeof evita que JS convierta textos como '4.5' a número al comparar.
    if (typeof nuevoPromedio !== 'number'
        || nuevoPromedio < Estudiante.PROMEDIO_MINIMO
        || nuevoPromedio > Estudiante.PROMEDIO_MAXIMO) {
      throw new RangeError(
        `promedio inválido (${nuevoPromedio}): debe estar entre `
        + `${Estudiante.PROMEDIO_MINIMO.toFixed(1)} y ${Estudiante.PROMEDIO_MAXIMO.toFixed(1)}`,
      );
    }
    this.#promedio = nuevoPromedio;
  }

  mostrarInfo() {
    console.log(`    ${this.nombre.padEnd(14)} | edad: ${String(this.edad).padStart(2)} | promedio: ${this.#promedio.toFixed(1)}`);
  }
}

function declaracion() {
  console.log('\n1. Declaración');
  const metodos = Object.getOwnPropertyNames(Estudiante.prototype)
    .filter((nombre) => nombre !== 'constructor');
  console.log('  Clase Estudiante');
  console.log('    Campos: nombre, edad, #promedio (privado)');
  console.log(`    Métodos públicos: ${metodos.join(', ')}`);
}

// 2. Inicialización
/** Crea 3 instancias de Estudiante con `new` y las guarda en un arreglo. */
function inicializacion() {
  console.log('\n2. Inicialización (3 instancias guardadas en un arreglo)');
  const estudiantes = [
    new Estudiante('Ana Martínez', 19, 4.2),
    new Estudiante('Luis Pérez', 21, 3.6),
    new Estudiante('Sofía Gómez', 20, 4.7),
  ];
  console.log(`  Se crearon ${estudiantes.length} objetos de tipo ${estudiantes[0].constructor.name}`);
  console.log(`  ¿estudiantes[0] instanceof Estudiante? ${estudiantes[0] instanceof Estudiante}`);
  // Al serializar el objeto solo aparecen los campos públicos: #promedio queda oculto.
  console.log(`  JSON.stringify(estudiantes[0]) -> ${JSON.stringify(estudiantes[0])}`);
  return estudiantes;
}

// 3. Recorrido
function recorrido(estudiantes, titulo = '3. Recorrido: mostrarInfo() de cada objeto') {
  console.log(`\n${titulo}`);
  // Cada objeto sabe mostrarse a sí mismo: el recorrido solo le envía el mensaje.
  for (const estudiante of estudiantes) {
    estudiante.mostrarInfo();
  }
}

// 4. Modificación
/** Búsqueda lineal: devuelve la posición del estudiante o -1 si no está. */
function buscarPorNombre(estudiantes, nombre) {
  for (let i = 0; i < estudiantes.length; i++) {
    if (estudiantes[i].nombre === nombre) {
      return i;
    }
  }
  return -1;
}

function modificacion(estudiantes) {
  const nombre = 'Luis Pérez';
  const nuevoPromedio = 4.1;
  console.log(`\n4. Modificación con setPromedio() (promedio de ${nombre} a ${nuevoPromedio})`);
  const luis = estudiantes[buscarPorNombre(estudiantes, nombre)];
  console.log(`  Antes:   getPromedio() = ${luis.getPromedio()}`);
  luis.setPromedio(nuevoPromedio);
  console.log(`  Después: getPromedio() = ${luis.getPromedio()}`);

  console.log('  a) El método valida el dato: setPromedio(7.5) se rechaza');
  try {
    luis.setPromedio(7.5);
  } catch (error) {
    console.log(`    ${error.name}: ${error.message}`);
  }
  console.log(`    El promedio sigue siendo ${luis.getPromedio()}`);

  console.log('  b) El campo es privado: desde fuera no existe como propiedad');
  // Escribir luis.#promedio fuera de la clase ni siquiera compila (SyntaxError).
  console.log(`    luis.promedio -> ${luis.promedio} | Object.keys(luis) -> [${Object.keys(luis).join(', ')}]`);
}

function main() {
  console.log('=== OBJETOS (CLASES E INSTANCIAS) EN JAVASCRIPT ===');
  declaracion();
  const estudiantes = inicializacion();
  recorrido(estudiantes);
  modificacion(estudiantes);
  recorrido(estudiantes, 'Arreglo después de la modificación');
}

main();
