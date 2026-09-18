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
  /** Campo privado: solo se lee con getPromedio(). */
  #promedio;

  constructor(nombre, edad, promedio) {
    this.nombre = nombre;
    this.edad = edad;
    this.#promedio = promedio;
  }

  getPromedio() {
    return this.#promedio;
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

function main() {
  console.log('=== OBJETOS (CLASES E INSTANCIAS) EN JAVASCRIPT ===');
  declaracion();
  const estudiantes = inicializacion();
  recorrido(estudiantes);
}

main();
