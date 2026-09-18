/**
 * Mini-proyecto integrador - Estructura de Datos, Unidad 1.
 *
 * Arreglo de OBJETOS en el que cada objeto tiene un campo que es a su vez una
 * MATRIZ: cada Producto guarda las unidades vendidas en una matriz ventas[mes][sucursal].
 * La misma solución está en mini-proyecto/ventas_sucursales.py para comparar la
 * sintaxis y el paradigma de Python y JavaScript (la salida es idéntica).
 *
 * Ejecución:
 *   node mini-proyecto/ventas_sucursales.js
 */

'use strict';

const MESES = ['Enero', 'Febrero', 'Marzo', 'Abril'];
const SUCURSALES = ['Centro', 'Bocagrande', 'Manga'];

// Datos ficticios: [código, nombre, precio, unidades vendidas [mes][sucursal]].
const DATOS = [
  ['P001', 'Arroz 500 g', 3200, [[120, 95, 80], [110, 100, 85], [130, 90, 95], [115, 100, 88]]],
  ['P002', 'Aceite 1 L', 12500, [[40, 55, 30], [35, 60, 28], [45, 50, 33], [38, 65, 31]]],
  ['P004', 'Café molido 250 g', 9800, [[60, 80, 45], [58, 85, 50], [62, 78, 47], [70, 90, 52]]],
];

function pesos(valor) {
  return `$${valor.toLocaleString('es-CO')}`;
}

/** Crea una matriz de MESES x SUCURSALES con ceros (una fila NUEVA por mes). */
function crearMatriz() {
  // Ojo: new Array(4).fill(new Array(3).fill(0)) repetiría la MISMA fila 4 veces.
  return Array.from({ length: MESES.length }, () => new Array(SUCURSALES.length).fill(0));
}

/** Objeto cuyo campo `ventas` es una matriz de MESES x SUCURSALES. */
class Producto {
  constructor(codigo, nombre, precio) {
    this.codigo = codigo;
    this.nombre = nombre;
    this.precio = precio;
    this.ventas = crearMatriz();
  }

  registrarVenta(mes, sucursal, unidades) {
    if (!(mes >= 0 && mes < MESES.length && sucursal >= 0 && sucursal < SUCURSALES.length)) {
      throw new RangeError(`posición inválida ventas[${mes}][${sucursal}]`);
    }
    if (unidades <= 0) {
      throw new RangeError('las unidades deben ser mayores que cero');
    }
    this.ventas[mes][sucursal] += unidades;
  }

  /** Suma de una FILA de la matriz. */
  totalPorMes(mes) {
    return this.ventas[mes].reduce((suma, unidades) => suma + unidades, 0);
  }

  /** Suma de una COLUMNA de la matriz. */
  totalPorSucursal(sucursal) {
    let total = 0;
    for (let mes = 0; mes < MESES.length; mes++) {
      total += this.ventas[mes][sucursal];
    }
    return total;
  }

  totalUnidades() {
    let total = 0;
    for (const fila of this.ventas) {
      for (const unidades of fila) {
        total += unidades;
      }
    }
    return total;
  }

  mejorMes() {
    let mejor = 0;
    for (let mes = 1; mes < MESES.length; mes++) {
      if (this.totalPorMes(mes) > this.totalPorMes(mejor)) {
        mejor = mes;
      }
    }
    return mejor;
  }

  ingresos() {
    return this.totalUnidades() * this.precio;
  }
}

const sumar = (valores) => valores.reduce((suma, valor) => suma + valor, 0);

/** Imprime la matriz como tabla, con el total de cada fila y de cada columna. */
function imprimirMatriz(matriz) {
  console.log(`    ${''.padEnd(9)}${SUCURSALES.map((s) => s.padStart(12)).join('')}${'Total'.padStart(9)}`);
  const totalesColumna = new Array(SUCURSALES.length).fill(0);
  for (let mes = 0; mes < MESES.length; mes++) {
    const fila = matriz[mes];
    for (let sucursal = 0; sucursal < SUCURSALES.length; sucursal++) {
      totalesColumna[sucursal] += fila[sucursal];
    }
    const celdas = fila.map((unidades) => String(unidades).padStart(12)).join('');
    console.log(`    ${MESES[mes].padEnd(9)}${celdas}${String(sumar(fila)).padStart(9)}`);
  }
  const celdas = totalesColumna.map((total) => String(total).padStart(12)).join('');
  console.log(`    ${'Total'.padEnd(9)}${celdas}${String(sumar(totalesColumna)).padStart(9)}`);
}

function crearProductos() {
  console.log('\n1. Arreglo de objetos: cada Producto tiene una matriz ventas[mes][sucursal]');
  const productos = new Array(DATOS.length).fill(null);
  for (let i = 0; i < DATOS.length; i++) {
    const [codigo, nombre, precio, unidades] = DATOS[i];
    const producto = new Producto(codigo, nombre, precio);
    for (let mes = 0; mes < MESES.length; mes++) {
      for (let sucursal = 0; sucursal < SUCURSALES.length; sucursal++) {
        producto.registrarVenta(mes, sucursal, unidades[mes][sucursal]);
      }
    }
    productos[i] = producto;
  }
  console.log(`  ${productos.length} productos, cada uno con una matriz de ${MESES.length} meses x ${SUCURSALES.length} sucursales`);
  return productos;
}

function recorrer(productos) {
  console.log('\n2. Recorrido: la matriz de cada objeto del arreglo');
  for (const producto of productos) {
    console.log(`\n  ${producto.codigo} - ${producto.nombre} (${pesos(producto.precio)} c/u)`);
    imprimirMatriz(producto.ventas);
  }
}

function totales(productos) {
  console.log('\n3. Totales por producto');
  let masVendido = productos[0];
  for (const producto of productos) {
    console.log(`  ${producto.nombre.padEnd(18)} unidades: ${String(producto.totalUnidades()).padStart(5)} | ingresos: `
      + `${pesos(producto.ingresos()).padStart(11)} | mejor mes: ${MESES[producto.mejorMes()]}`);
    if (producto.totalUnidades() > masVendido.totalUnidades()) {
      masVendido = producto;
    }
  }
  console.log(`  Producto más vendido: ${masVendido.nombre} (${masVendido.totalUnidades()} unidades)`);
}

function consolidado(productos) {
  console.log('\n4. Matriz consolidada (suma de las matrices de todos los productos)');
  const matriz = crearMatriz();
  for (const producto of productos) {
    for (let mes = 0; mes < MESES.length; mes++) {
      for (let sucursal = 0; sucursal < SUCURSALES.length; sucursal++) {
        matriz[mes][sucursal] += producto.ventas[mes][sucursal];
      }
    }
  }
  imprimirMatriz(matriz);

  const totalColumna = (sucursal) => sumar(matriz.map((fila) => fila[sucursal]));
  let mejor = 0;
  for (let sucursal = 1; sucursal < SUCURSALES.length; sucursal++) {
    if (totalColumna(sucursal) > totalColumna(mejor)) {
      mejor = sucursal;
    }
  }
  console.log(`  Sucursal con más unidades vendidas: ${SUCURSALES[mejor]}`);
}

function modificar(productos) {
  const [mes, sucursal, unidades] = [3, 2, 20];
  const producto = productos[1];
  console.log(`\n5. Modificación: registrar ${unidades} unidades más de ${producto.nombre}`
    + ` en ${MESES[mes]} / ${SUCURSALES[sucursal]}`);
  console.log(`  Antes:   ventas[${mes}][${sucursal}] = ${producto.ventas[mes][sucursal]}`
    + ` | total del producto = ${producto.totalUnidades()}`);
  producto.registrarVenta(mes, sucursal, unidades);
  console.log(`  Después: ventas[${mes}][${sucursal}] = ${producto.ventas[mes][sucursal]}`
    + ` | total del producto = ${producto.totalUnidades()}`);
  try {
    producto.registrarVenta(4, 0, 10);
  } catch (error) {
    console.log(`  registrarVenta(4, 0, 10) -> ${error.name}: ${error.message}`);
  }
}

function main() {
  console.log('=== MINI-PROYECTO: VENTAS POR MES Y SUCURSAL (JAVASCRIPT) ===');
  const productos = crearProductos();
  recorrer(productos);
  totales(productos);
  consolidado(productos);
  modificar(productos);
}

main();
