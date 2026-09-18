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

function main() {
  console.log('=== OBJETOS (CLASES E INSTANCIAS) EN JAVASCRIPT ===');
  declaracion();
}

main();
