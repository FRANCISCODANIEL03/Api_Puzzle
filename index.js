function crearFormulario() {
    const cantidad = parseInt(document.getElementById("nodos").value);
    const aristasContainer = document.getElementById("aristasContainer");
    const form = document.getElementById("grafoForm");
  
    aristasContainer.innerHTML = "";
    form.classList.add("hidden");
  
    if (isNaN(cantidad) || cantidad < 2) {
      alert("Debe ingresar un número de nodos mayor o igual a 2.");
      return;
    }

    if(cantidad > 10) {
      alert("El número máximo de nodos es 10.");
      return;
    }

    form.classList.remove("hidden");
  
    for (let i = 1; i <= cantidad; i++) {
      for (let j = i + 1; j <= cantidad; j++) {
        const div = document.createElement("div");
        div.innerHTML = `
          <label>Peso entre nodo ${i} y ${j}:</label>
          <input type="number" min="0" id="peso-${i}-${j}" />
        `;
        aristasContainer.appendChild(div);
      }
    }
  }

function limpiarTodo() {
    // Limpiar campos
    document.getElementById("nodos").value = "";
    document.getElementById("inicio").value = "";
    document.getElementById("fin").value = "";
  
    // Ocultar formulario de aristas
    document.getElementById("grafoForm").classList.add("hidden");
  
    // Limpiar inputs de aristas
    document.getElementById("aristasContainer").innerHTML = "";
  
    // Limpiar resultados
    document.getElementById("resultado").innerHTML = "";
}
  
  
document.getElementById("grafoForm").addEventListener("submit", function (e) {
    e.preventDefault();
  
    const cantidad = parseInt(document.getElementById("nodos").value);
    const grafo = {};
    const resultadoDiv = document.getElementById("resultado");
    resultadoDiv.innerHTML = "";
  
    if (isNaN(cantidad) || cantidad < 2) {
      alert("Número de nodos inválido.");
      return;
    }
  
    for (let i = 1; i <= cantidad; i++) {
      grafo[i] = {};
    }
  
    for (let i = 1; i <= cantidad; i++) {
      for (let j = i + 1; j <= cantidad; j++) {
        const pesoInput = document.getElementById(`peso-${i}-${j}`);
        const valor = pesoInput.value.trim();
  
        if (valor === "") continue;
  
        const peso = parseInt(valor);
        if (isNaN(peso) || peso <= 0) {
          alert(`El peso entre nodo ${i} y ${j} debe ser un número positivo.`);
          return;
        }
  
        grafo[i][j] = peso;
        grafo[j][i] = peso;
      }
    }
  
    const nodoInicial = document.getElementById("inicio").value.trim();
    const nodoFinal = document.getElementById("fin").value.trim();
  
    if (nodoInicial === "" || nodoFinal === "") {
      alert("Debe especificar los nodos de inicio y fin.");
      return;
    }
  
    if (!grafo[nodoInicial] || !grafo[nodoFinal]) {
      alert("El nodo de inicio o fin no existe en el grafo.");
      return;
    }
  
    if (nodoInicial === nodoFinal) {
      alert("El nodo de inicio y el nodo final no pueden ser el mismo.");
      return;
    }
  
    resultadoDiv.innerHTML = "Procesando...";
  
    fetch("https://api-puzzle-1.onrender.com/grafo", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        grafo: grafo,
        nodoInicial: nodoInicial,
        nodoFinal: nodoFinal,
      }),
    })
      .then(response => {
        if (!response.ok) throw new Error("Error al procesar el grafo.");
        return response.json();
      })
      .then(([distancia, camino]) => {
        const timestamp = new Date().getTime();
        const imagenURL = `https://api-puzzle-1.onrender.com/imagen?t=${timestamp}`;

        resultadoDiv.innerHTML = `
            <p><strong>Distancia más corta:</strong> ${distancia}</p>
            <p><strong>Camino:</strong> ${camino.join(" ➝ ")}</p>
            <p><strong>Imagen del grafo:</strong></p>
            <img src="${imagenURL}" alt="Imagen del grafo" />
        `;
      })
      .catch(error => {
        resultadoDiv.innerHTML = `<p style="color:red;">Error al obtener recursos</p>`;
        console.log(error);
        
      });
}); 