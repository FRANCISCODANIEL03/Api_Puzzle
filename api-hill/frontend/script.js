coord = {
    'Jiloyork' :(19.916012, -99.580580),
    'Toluca':(19.289165, -99.655697),
    'Atlacomulco':(19.799520, -99.873844),
    'Guadalajara':(20.677754472859146, -103.34625354877137),
    'Monterrey':(25.69161110159454, -100.321838480256),
    'QuintanaRoo':(21.163111924844458, -86.80231502121464),
    'Michohacan':(19.701400113725654, -101.20829680213464),
    'Aguascalientes':(21.87641043660486, -102.26438663286967),
    'CDMX':(19.432713075976878, -99.13318344772986),
    'QRO':(20.59719437542255, -100.38667040246602)
}

const btn = document.getElementById('btn1');

btn.addEventListener('click', async (e) => {
    console.log("Enviando formulario");
    
    e.preventDefault();
    const contenedor = document.getElementById('resultados');
    contenedor.innerHTML = "Procesando...";
    try {
        const res = await fetch('http://localhost:5001/hill');
        console.log(res);
        const resultado = await res.json();
        mostrarResultados(resultado.ruta, resultado.distancia_total);
    } catch (err) {
        console.log(err);
    }
});


function mostrarResultados(ruta, distancia) {
    const contenedor = document.getElementById('resultados');
    if (!ruta.length) {
        contenedor.innerHTML = '<p>No se generaron rutas.</p>';
        return;
    }
    contenedor.innerHTML = `
        <h2>Resultados</h2>
        <p><strong>Distancia total:</strong> ${distancia} km</p>
        <h3>Ruta generada:</h3>
        <p><strong>Lugares:</strong> ${ruta.join(' -> ')}</p>
    `;
}

