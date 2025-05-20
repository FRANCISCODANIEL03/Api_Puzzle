document.getElementById('btn-generar').addEventListener('click', async () => {

  const datos = {
    "max_iter":10,
	"max_poblacion":50,
	"num_vars":10,
	"prob_mutacion": 0.1
  };

  try {
    const respuesta = await fetch('http://172.168.3.215:5001/genes', { // cambia la URL
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(datos)
    });

    if (!respuesta.ok) {
      throw new Error(`Error HTTP: ${respuesta.status}`);
    }

    const resultado = await respuesta.json();

    // Parsear si vienen como strings
    const mejorGen = JSON.parse(resultado.mejor_gen_encontrado);
    const solucion = JSON.parse(resultado.solucion);

    // Mostrar resultados
    const contenedor = document.getElementById('resultado');
    contenedor.innerHTML = `
      <div class="datos">
        <p><strong>Función de adaptación:</strong> ${resultado.funcion_de_adaptacion}</p>
        <p><strong>Mejor gen encontrado:</strong> ${mejorGen.join(', ')}</p>
        <p><strong>Solución:</strong> ${solucion.join(', ')}</p>
      </div>
      <div class="tarjetas">
        ${solucion.map((gen, i) => `<div class="tarjeta">Gen ${i + 1}: ${gen}</div>`).join('')}
      </div>
    `;
  } catch (error) {
    console.error('Error al hacer la solicitud:', error);
    document.getElementById('resultado').innerHTML = `
      <p style="color: red;"><strong>Error:</strong> No se pudo obtener la solución.</p>
    `;
  }
});
