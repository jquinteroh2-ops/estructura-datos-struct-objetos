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
  const ejemplo = crearEstudiante('ejemplo', 0, 0.0);
  console.log(`  crearEstudiante()       (objeto plano, mutable)    -> ${describirCampos(ejemplo)}`);
  console.log(`  crearEstudianteRecord() (Object.freeze, inmutable) -> ${describirCampos(ejemplo)}`);
  console.log(`  ¿Es un objeto plano? ${Object.getPrototypeOf(ejemplo) === Object.prototype}`);
}

function main() {
  console.log('=== STRUCT / RECORD EN JAVASCRIPT ===');
  declaracion();
}

main();
