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

  }
});
