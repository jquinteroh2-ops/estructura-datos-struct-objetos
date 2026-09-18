/**
 * Comparativa Struct/Record vs Objeto en JavaScript - Estructura de Datos, Unidad 1.
 *
 * Se resuelve EL MISMO PROBLEMA con el mismo Estudiante modelado de tres formas,
 * en un solo archivo, para señalar las diferencias directamente en el código.
 *
 *   Problema: registrar 3 estudiantes, mostrarlos, cambiar el promedio de uno,
 *   intentar asignarle un promedio inválido (7.5) y copiar un estudiante.
 *
 *   A) Struct -> objeto literal plano (mutable). Las operaciones son funciones EXTERNAS.
 *   B) Record -> objeto plano congelado con Object.freeze (inmutable).
 *   C) Objeto -> clase con el campo privado #promedio y métodos que validan el dato.
 *
 * Ejecución:
 *   node js/comparativa.js
 */

'use strict';

const NOMBRE_A_MODIFICAR = 'Luis Pérez';
const NUEVO_PROMEDIO = 4.1;
const PROMEDIO_INVALIDO = 7.5;

// A) Struct: solo datos, mutable.
function crearEstudianteStruct(nombre, edad, promedio) {
  return { nombre, edad, promedio };
}

// B) Record: solo datos, inmutable.
function crearEstudianteRecord(nombre, edad, promedio) {
  return Object.freeze({ nombre, edad, promedio });
}

// C) Objeto: datos + comportamiento, con el promedio encapsulado.
class Estudiante {
  static PROMEDIO_MINIMO = 0.0;
  static PROMEDIO_MAXIMO = 5.0;
  #promedio = 0.0;

  constructor(nombre, edad, promedio) {
    this.nombre = nombre;
    this.edad = edad;
    this.setPromedio(promedio);
  }

  getPromedio() {
    return this.#promedio;
  }

  setPromedio(nuevoPromedio) {
    if (typeof nuevoPromedio !== 'number') {
      throw new TypeError(`el promedio debe ser un número, se recibió un ${typeof nuevoPromedio}`);
    }
    if (nuevoPromedio < Estudiante.PROMEDIO_MINIMO || nuevoPromedio > Estudiante.PROMEDIO_MAXIMO) {
      throw new RangeError(`promedio inválido (${nuevoPromedio}): debe estar entre 0.0 y 5.0`);
    }
    this.#promedio = nuevoPromedio;
  }

  mostrarInfo() {
    console.log(formatear(this.nombre, this.edad, this.#promedio));
  }
}

// Con el struct y el record, "mostrar" y "cambiar" son funciones EXTERNAS que
// reciben los datos como parámetro: el struct no sabe hacer nada por sí mismo.
function formatear(nombre, edad, promedio) {
  return `       ${nombre.padEnd(14)} | edad: ${String(edad).padStart(2)} | promedio: ${promedio.toFixed(1)}`;
}

function mostrarInfo(estudiante) {
  console.log(formatear(estudiante.nombre, estudiante.edad, estudiante.promedio));
}

/** Búsqueda lineal por nombre: devuelve la posición o -1 (sirve para los tres modelos). */
function buscarPosicion(arreglo, nombre) {
  for (let i = 0; i < arreglo.length; i++) {
    if (arreglo[i].nombre === nombre) {
      return i;
    }
  }
  return -1;
}

function declaracion() {
  console.log('\n1. Declaración: el mismo Estudiante tres veces');
  console.log('  A) Struct -> objeto literal { ... }      : nombre, edad, promedio | sin métodos propios');
  console.log('  B) Record -> Object.freeze({ ... })      : nombre, edad, promedio | sin métodos, inmutable');
  console.log('  C) Objeto -> class Estudiante            : nombre, edad, #promedio (privado)'
    + ' | getPromedio, setPromedio, mostrarInfo');
}

function crearYMostrar() {
  const datos = [['Ana Martínez', 19, 4.2], ['Luis Pérez', 21, 3.6], ['Sofía Gómez', 20, 4.7]];
  const structs = datos.map((d) => crearEstudianteStruct(...d));
  const records = datos.map((d) => crearEstudianteRecord(...d));
  const objetos = datos.map((d) => new Estudiante(...d));

  console.log('\n2. Crear los 3 estudiantes, guardarlos en un arreglo y mostrarlos');
  console.log('  A) Struct -> función externa: mostrarInfo(estudiante)');
  structs.forEach(mostrarInfo);
  console.log('  B) Record -> la misma función externa: mostrarInfo(estudiante)');
  records.forEach(mostrarInfo);
  console.log('  C) Objeto -> método propio: estudiante.mostrarInfo()');
  objetos.forEach((estudiante) => estudiante.mostrarInfo());
  return { structs, records, objetos };
}

function modificar({ structs, records, objetos }) {
  console.log(`\n3. Cambiar el promedio de ${NOMBRE_A_MODIFICAR} a ${NUEVO_PROMEDIO}`);

  const luisStruct = structs[buscarPosicion(structs, NOMBRE_A_MODIFICAR)];
  luisStruct.promedio = NUEVO_PROMEDIO;
  console.log(`  A) Struct: luis.promedio = ${NUEVO_PROMEDIO} -> promedio = ${luisStruct.promedio}`
    + ' (cualquier parte del programa puede cambiarlo)');

  const posicion = buscarPosicion(records, NOMBRE_A_MODIFICAR);
  const luisRecord = records[posicion];
  try {
    luisRecord.promedio = NUEVO_PROMEDIO;
  } catch (error) {
    console.log(`  B) Record: luis.promedio = ${NUEVO_PROMEDIO} -> ${error.name}: ${error.message}`);
  }
  records[posicion] = Object.freeze({ ...luisRecord, promedio: NUEVO_PROMEDIO });
  console.log(`             Object.freeze({ ...luis, promedio: ${NUEVO_PROMEDIO} }) -> record NUEVO con promedio =`
    + ` ${records[posicion].promedio} (¿es otro objeto? ${records[posicion] !== luisRecord})`);

  const luisObjeto = objetos[buscarPosicion(objetos, NOMBRE_A_MODIFICAR)];
  luisObjeto.setPromedio(NUEVO_PROMEDIO);
  console.log(`  C) Objeto: luis.setPromedio(${NUEVO_PROMEDIO}) -> getPromedio() = ${luisObjeto.getPromedio()}`);
}

function datoInvalido({ structs, records, objetos }) {
  console.log(`\n4. Intentar asignar un promedio inválido (${PROMEDIO_INVALIDO}, la escala es de 0.0 a 5.0)`);

  const luisStruct = structs[buscarPosicion(structs, NOMBRE_A_MODIFICAR)];
  luisStruct.promedio = PROMEDIO_INVALIDO;
  console.log(`  A) Struct: se acepta sin avisar -> promedio = ${luisStruct.promedio}`
    + ' (el dato queda inconsistente)');

  const luisRecord = Object.freeze({
    ...records[buscarPosicion(records, NOMBRE_A_MODIFICAR)],
    promedio: PROMEDIO_INVALIDO,
  });
  console.log(`  B) Record: la copia con spread también lo acepta -> promedio = ${luisRecord.promedio}`
    + ' (habría que validar en la factory function)');

  const luisObjeto = objetos[buscarPosicion(objetos, NOMBRE_A_MODIFICAR)];
  try {
    luisObjeto.setPromedio(PROMEDIO_INVALIDO);
  } catch (error) {
    console.log(`  C) Objeto: ${error.name}: ${error.message}`);
  }
  console.log(`             el promedio sigue siendo ${luisObjeto.getPromedio()} (el objeto protege su estado)`);
}

function igualdad() {
  console.log('\n5. Igualdad: dos instancias con los MISMOS datos, ¿son iguales (===)?');
  const s1 = crearEstudianteStruct('Ana Martínez', 19, 4.2);
  const s2 = crearEstudianteStruct('Ana Martínez', 19, 4.2);
  console.log(`  A) Struct: ${s1 === s2} -> === compara referencias, no los campos`);
  console.log(`             comparando campo por campo: ${s1.nombre === s2.nombre && s1.edad === s2.edad && s1.promedio === s2.promedio}`);
  const r1 = crearEstudianteRecord('Ana Martínez', 19, 4.2);
  const r2 = crearEstudianteRecord('Ana Martínez', 19, 4.2);
  console.log(`  B) Record: ${r1 === r2} -> congelar el objeto no cambia cómo se compara`);
  const o1 = new Estudiante('Ana Martínez', 19, 4.2);
  const o2 = new Estudiante('Ana Martínez', 19, 4.2);
  console.log(`  C) Objeto: ${o1 === o2} -> identidad: son dos objetos distintos en memoria`);
}

function tipado() {
  console.log('\n6. Tipado: JavaScript es dinámico; no hay tipos declarados que se verifiquen');
  const struct = crearEstudianteStruct('Ana Martínez', 'diecinueve', 4.2);
  console.log(`  A) Struct: crearEstudianteStruct('Ana Martínez', 'diecinueve', 4.2) se crea sin error`
    + ` -> edad = '${struct.edad}' (${typeof struct.edad})`);
  try {
    new Estudiante('Ana Martínez', 19, '4.2');
  } catch (error) {
    console.log(`  C) Objeto: new Estudiante('Ana Martínez', 19, '4.2') -> ${error.name}: ${error.message}`);
  }
  console.log("             (sin la comprobación typeof, JS habría convertido '4.2' a número al comparar)");
}

function memoria() {
  console.log('\n7. Memoria: en JavaScript las variables de tipo objeto guardan REFERENCIAS al heap');
  const original = crearEstudianteStruct('Sofía Gómez', 20, 4.7);
  const alias = original; // no copia: las dos variables apuntan al mismo objeto
  alias.promedio = 0.0;
  console.log(`  alias = original; alias.promedio = 0.0 -> original.promedio = ${original.promedio.toFixed(1)}`
    + ` (¿mismo objeto? ${alias === original})`);
  const copia = { ...original, promedio: 4.7 }; // copia superficial: un objeto nuevo
  console.log(`  copia = { ...original, promedio: 4.7 } -> original.promedio = ${original.promedio.toFixed(1)},`
    + ` copia.promedio = ${copia.promedio.toFixed(1)} (¿mismo objeto? ${copia === original})`);
  console.log('  En C#, C o Go un struct es un VALOR: asignarlo copia todos sus campos (normalmente en el');
  console.log('  stack). En Python y JavaScript structs y objetos viven en el heap y se comparten por referencia.');
}

function resumen() {
  console.log('\n8. Resumen');
  const filas = [
    ['', 'Struct', 'Record', 'Objeto'],
    ['Mutabilidad', 'mutable', 'inmutable', 'mutable controlada'],
    ['Valida datos', 'no', 'solo si se agrega', 'sí (setPromedio)'],
    ['Comportamiento', 'funciones externas', 'funciones externas', 'métodos propios'],
    ['Igualdad (===)', 'por referencia', 'por referencia', 'por referencia'],
    ['Encapsulamiento', 'no', 'no', 'sí (#promedio)'],
  ];
  for (const [criterio, struct, record, objeto] of filas) {
    console.log(`  ${criterio.padEnd(16)}| ${struct.padEnd(19)}| ${record.padEnd(19)}| ${objeto}`);
  }
}

function main() {
  console.log('=== COMPARATIVA STRUCT / RECORD vs OBJETO EN JAVASCRIPT ===');
  console.log('Problema: registrar 3 estudiantes, mostrarlos, cambiar un promedio,');
  console.log('intentar un promedio inválido y copiar un estudiante.');
  declaracion();
  const arreglos = crearYMostrar();
  modificar(arreglos);
  datoInvalido(arreglos);
  igualdad();
  tipado();
  memoria();
  resumen();
}

main();
