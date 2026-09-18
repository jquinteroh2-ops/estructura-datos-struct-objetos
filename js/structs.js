/**
 * Struct / Record en JavaScript - Estructura de Datos, Unidad 1.
 *
 * JavaScript NO tiene struct nativo. Lo más cercano es un OBJETO LITERAL PLANO
 * ({ nombre, edad, promedio }):
 *   - agrupa datos relacionados en campos con nombre, igual que un struct;
 *   - no tiene clase ni métodos propios: solo datos;
 *   - no necesita declararse antes: su "forma" existe en el momento de crearlo.
 * Para no repetir el literal en cada instancia se usa una FACTORY FUNCTION: una
 * función normal que recibe los valores y devuelve el objeto plano.
 *
 * Para imitar un RECORD (inmutable) se congela el objeto con Object.freeze().
 *
 * Ejecución:
 *   node js/structs.js
 */

'use strict';

// 1. Declaración
/** "Struct" (mutable): objeto literal plano con los tres campos. */
function crearEstudiante(nombre, edad, promedio) {
  return { nombre, edad, promedio };
}

/** "Record" (inmutable): el mismo objeto plano, pero congelado. */
function crearEstudianteRecord(nombre, edad, promedio) {
  return Object.freeze({ nombre, edad, promedio });
}

/** Devuelve los campos del objeto y el tipo de cada valor, p. ej. 'nombre: string'. */
function describirCampos(objeto) {
  return Object.entries(objeto)
    .map(([campo, valor]) => `${campo}: ${typeof valor}`)
    .join(', ');
}

function declaracion() {
  console.log('\n1. Declaración');
  // En JS no hay declaración de tipo: los campos solo se conocen al crear un objeto.
  const struct = crearEstudiante('ejemplo', 0, 0.0);
  const record = crearEstudianteRecord('ejemplo', 0, 0.0);
  console.log(`  crearEstudiante()       (objeto plano, mutable)    -> ${describirCampos(struct)}`);
  console.log(`  crearEstudianteRecord() (Object.freeze, inmutable) -> ${describirCampos(record)}`);
  console.log(`  ¿Es un objeto plano? ${Object.getPrototypeOf(struct) === Object.prototype}`
    + ` | ¿El record está congelado? ${Object.isFrozen(record)}`);
}

// 2. Inicialización
/** Crea 3 instancias de cada tipo con datos ficticios y las guarda en arreglos. */
function inicializacion() {
  console.log('\n2. Inicialización (3 instancias con datos ficticios)');
  const ana = crearEstudiante('Ana Martínez', 19, 4.2);
  const luis = crearEstudiante('Luis Pérez', 21, 3.6);
  // También se puede escribir el objeto literal directamente, sin la factory function.
  const sofia = { nombre: 'Sofía Gómez', edad: 20, promedio: 4.7 };
  const estudiantes = [ana, luis, sofia];

  const registros = [
    crearEstudianteRecord('Ana Martínez', 19, 4.2),
    crearEstudianteRecord('Luis Pérez', 21, 3.6),
    crearEstudianteRecord('Sofía Gómez', 20, 4.7),
  ];

  // JSON.stringify muestra el objeto con sus datos (equivalente al __repr__ de Python).
  console.log('  a) Structs (objetos planos):');
  for (const estudiante of estudiantes) {
    console.log(`    ${JSON.stringify(estudiante)}`);
  }
  console.log('  b) Records (objetos congelados):');
  for (const registro of registros) {
    console.log(`    ${JSON.stringify(registro)}`);
  }
  return { estudiantes, registros };
}

function main() {
  console.log('=== STRUCT / RECORD EN JAVASCRIPT ===');
  declaracion();
  inicializacion();
}

main();
