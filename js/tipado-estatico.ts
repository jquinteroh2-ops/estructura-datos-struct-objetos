/**
 * Ejemplo en un lenguaje de TIPADO ESTÁTICO (TypeScript) - Estructura de Datos, Unidad 1.
 *
 * Complementa la tabla comparativa: el mismo Estudiante como record y como objeto,
 * pero con los tipos declarados y verificados ANTES de ejecutar.
 * TypeScript se usa solo en este ejemplo puntual para ilustrar el tipado estático;
 * el resto de la actividad está en Python y JavaScript.
 *
 * Ejecución (Node.js 22.18 o superior ejecuta .ts directamente, sin instalar nada):
 *   node js/tipado-estatico.ts
 *
 * Node solo borra los tipos y ejecuta el código: la VERIFICACIÓN de tipos la hacen
 * el editor (VS Code la trae incluida) o el compilador `tsc`. Para verla, quite el
 * comentario de las líneas marcadas con "ERROR DE TIPO": VS Code las subraya en rojo
 * sin necesidad de ejecutar el programa.
 */

// Record: un tipo de solo datos. `readonly` impide cambiar los campos (en compilación).
interface EstudianteRecord {
  readonly nombre: string;
  readonly edad: number;
  readonly promedio: number;
}

// Objeto: datos + comportamiento, con el promedio privado y tipado.
class Estudiante {
  static readonly PROMEDIO_MINIMO: number = 0.0;
  static readonly PROMEDIO_MAXIMO: number = 5.0;

  readonly nombre: string;
  readonly edad: number;
  #promedio: number = 0.0;

  constructor(nombre: string, edad: number, promedio: number) {
    this.nombre = nombre;
    this.edad = edad;
    this.setPromedio(promedio);
  }

  getPromedio(): number {
    return this.#promedio;
  }

  // Ya no hace falta comprobar typeof: el compilador garantiza que llega un number.
  setPromedio(nuevoPromedio: number): void {
    if (nuevoPromedio < Estudiante.PROMEDIO_MINIMO || nuevoPromedio > Estudiante.PROMEDIO_MAXIMO) {
      throw new RangeError(`promedio inválido (${nuevoPromedio}): debe estar entre 0.0 y 5.0`);
    }
    this.#promedio = nuevoPromedio;
  }

  mostrarInfo(): void {
    console.log(`  ${this.nombre.padEnd(14)} | edad: ${String(this.edad).padStart(2)} | promedio: ${this.#promedio.toFixed(1)}`);
  }
}

console.log('=== TIPADO ESTÁTICO CON TYPESCRIPT ===');

const registros: EstudianteRecord[] = [
  { nombre: 'Ana Martínez', edad: 19, promedio: 4.2 },
  { nombre: 'Luis Pérez', edad: 21, promedio: 3.6 },
  { nombre: 'Sofía Gómez', edad: 20, promedio: 4.7 },
];

// ERROR DE TIPO: la edad debe ser number.
// const invalido: EstudianteRecord = { nombre: 'Ana Martínez', edad: 'diecinueve', promedio: 4.2 };
//   -> error TS2322: Type 'string' is not assignable to type 'number'.

// ERROR DE TIPO: el record es readonly, no se puede modificar.
// registros[1].promedio = 4.1;
//   -> error TS2540: Cannot assign to 'promedio' because it is a read-only property.

console.log('\nRecords (interface con campos readonly):');
for (const { nombre, edad, promedio } of registros) {
  console.log(`  ${nombre.padEnd(14)} | edad: ${String(edad).padStart(2)} | promedio: ${promedio.toFixed(1)}`);
}

const estudiantes: Estudiante[] = registros.map((r) => new Estudiante(r.nombre, r.edad, r.promedio));
estudiantes[1].setPromedio(4.1);

// ERROR DE TIPO: setPromedio espera un number.
// estudiantes[1].setPromedio('4.1');
//   -> error TS2345: Argument of type 'string' is not assignable to parameter of type 'number'.

console.log('\nObjetos (clase Estudiante), después de setPromedio(4.1) sobre Luis Pérez:');
for (const estudiante of estudiantes) {
  estudiante.mostrarInfo();
}
