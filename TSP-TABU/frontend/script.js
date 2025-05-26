const API_BASE = "https://busqueda-tabu.onrender.com";
const boton = document.getElementById("btn-generar");
const resultadoDiv = document.getElementById("resultado");

boton.addEventListener("click", () => {
  resultadoDiv.innerHTML = "<p>Cargando rutas...</p>";

  fetch(`${API_BASE}/ruta`)
    .then(response => {
      if (!response.ok) throw new Error("Error al procesar la ruta.");
      return response.json();
    })
    .then(data => {
      const tarjetasInicial = data.ruta_inicial.map(ciudad => `<div class="tarjeta">${ciudad}</div>`).join('');
      const tarjetasOptima = data.mejor_ruta.map(ciudad => `<div class="tarjeta">${ciudad}</div>`).join('');

      resultadoDiv.innerHTML = `
        <div class="datos">
          <p><strong>Distancia inicial:</strong> ${data.distancia_inicial.toFixed(4)}</p>
          <p><strong>Distancia optimizada:</strong> ${data.distancia_optimizada.toFixed(4)}</p>
        </div>
        <p><strong>Ruta inicial:</strong></p>
        <div class="tarjetas">${tarjetasInicial}</div>
        <p><strong>Ruta optimizada:</strong></p>
        <div class="tarjetas">${tarjetasOptima}</div>
      `;
    })
    .catch(error => {
      resultadoDiv.innerHTML = `<p style="color:red;">Error al obtener la ruta.</p>`;
      console.error(error);
    });
})