const ubicaciones = {
    'EDO.MEX': [19.293704, -99.653710],
    'QRO': [20.593507, -100.390072],
    'CDMX': [19.432915, -99.133364],
    'SPL': [22.150933, -100.974140],
    'MTY': [25.675058, -100.287582],
    'PUE': [19.063633, -98.306990],
    'GDL': [20.677204, -103.346994],
    'MICH': [19.702594, -101.192382],
    'SON': [29.075226, -110.959624]
};

let restriccionCount = 0;

document.getElementById('agregarRestriccion').addEventListener('click', () => {
    if (restriccionCount >= 10) {
        Swal.fire("¡Límite alcanzado!", "Solo puedes agregar hasta 10 restricciones.", "warning");
        return;
    }

    const contenedor = document.getElementById('restriccionesContainer');
    const div = document.createElement('div');
    div.className = 'restriccion';
    div.innerHTML = `
      <input placeholder="Origen (ej: QRO)" class="origen" required />
      <input placeholder="Destino (ej: PUE)" class="destino" required />
      <button type="button" class="borrarRestriccion">X</button>
    `;
    contenedor.appendChild(div);
    restriccionCount++;

    div.querySelector('.borrarRestriccion').addEventListener('click', () => {
        div.remove();
        restriccionCount--;
    });
});

document.getElementById('vrpForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    const almacenKey = document.getElementById('almacen').value;
    const max_carga = document.getElementById('max_carga').value;
    const max_clientes = document.getElementById('max_clientes').value;
    const contenedor = document.getElementById('resultados');

    // Validación de campos vacíos
    if (!almacenKey || !max_carga || !max_clientes) {
        Swal.fire("Campos vacíos", "Por favor llena todos los campos antes de continuar.", "warning");
        return;
    }

    const almacenCoords = ubicaciones[almacenKey];
    const restricciones = [];
    let error = false;

    document.querySelectorAll('.restriccion').forEach(div => {
        const origen = div.querySelector('.origen').value.trim().toUpperCase();
        const destino = div.querySelector('.destino').value.trim().toUpperCase();

        if (!origen || !destino) {
            Swal.fire("Campos vacíos", "Todas las restricciones deben tener origen y destino.", "warning");
            error = true;
            return;
        }

        if (!(origen in ubicaciones) || !(destino in ubicaciones)) {
            Swal.fire("Ubicación inválida", `Revisa los valores: "${origen}" o "${destino}"`, "error");
            error = true;
        } else {
            restricciones.push([origen, destino]);
        }
    });

    if (error) return;

    const datos = {
        almacen: almacenCoords,
        max_carga: parseInt(max_carga),
        max_clientes: parseInt(max_clientes),
        restricciones_trafico: restricciones
    };

    contenedor.innerHTML = "Procesando...";
    try {
        const res = await fetch('https://vrp-voraz.onrender.com/vrp', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(datos)
        });

        const resultado = await res.json();
        mostrarResultados(resultado.rutas);
    } catch (err) {
        Swal.fire("Error de conexión", err.message, "error");
    }
});


function mostrarResultados(rutas) {
    const contenedor = document.getElementById('resultados');
    contenedor.innerHTML = `<h2>Rutas Generadas ${rutas.length}</h2>`;
    if (!rutas.length) {
        contenedor.innerHTML += '<p>No se generaron rutas.</p>';
        return;
    }

    rutas.forEach((ruta, i) => {
        contenedor.innerHTML += `
        <div class="ruta">
          <h3>Ruta ${i + 1}</h3>
          <p><strong>Clientes:</strong> ${ruta.ruta.join(' → ')}</p>
          <p><strong>Peso total:</strong> ${ruta.peso_total}</p>
          <p><strong>Clientes en ruta:</strong> ${ruta.clientes}</p>
        </div>
      `;
    });
}
