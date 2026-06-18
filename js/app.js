const STORAGE_KEY = "coleccion_juegos";

let juegos = [];

async function cargarDatos(){

const localData = localStorage.getItem(STORAGE_KEY);

if(localData){

juegos = JSON.parse(localData);

}else{

const response = await fetch("data/juegos.json");
juegos = await response.json();

guardar();
}

cargarPlataformas();
renderizar();
}

function guardar(){

localStorage.setItem(
STORAGE_KEY,
JSON.stringify(juegos)
);

}

function cargarPlataformas(){

const select =
document.getElementById("platformFilter");

select.innerHTML =
'<option value="">Todas las plataformas</option>';

const plataformas =
[...new Set(juegos.map(j=>j.plataforma))];

plataformas.sort();

plataformas.forEach(p=>{

const option =
document.createElement("option");

option.value = p;
option.textContent = p;

select.appendChild(option);

});

}

function renderizar(){

const texto =
document.getElementById("search")
.value
.toLowerCase();

const plataforma =
document.getElementById("platformFilter")
.value;

const lista = juegos.filter(j=>{

const coincideTexto =
j.titulo.toLowerCase()
.includes(texto);

const coincidePlataforma =
!plataforma ||
j.plataforma === plataforma;

return coincideTexto &&
coincidePlataforma;

});

const container =
document.getElementById("gamesContainer");

container.innerHTML = "";

lista.forEach(j=>{

container.innerHTML += `

<div class="game-card">

<img
src="${j.portada}"
alt="${j.titulo}"
onerror="this.src='images/no-image.jpg'">

<div class="game-info">

<div class="game-title">
${j.titulo}
</div>

<div class="platform">
${j.plataforma}
</div>

<div>
${j.generacion}
</div>

<div class="region">
${j.region}
</div>

<button
class="delete-btn"
onclick="eliminarJuego(${j.id})">

Eliminar

</button>

</div>

</div>

`;

});

document.getElementById("stats")
.textContent =
`Total juegos: ${lista.length}`;

}

function agregarJuego(e){

e.preventDefault();

const juego = {

id: Date.now(),

titulo:
document.getElementById("title").value,

plataforma:
document.getElementById("platform").value,

generacion:
document.getElementById("generation").value,

region:
document.getElementById("region").value,

portada:
document.getElementById("image").value

};

juegos.push(juego);

guardar();

cargarPlataformas();

renderizar();

e.target.reset();

}

function eliminarJuego(id){

if(!confirm("¿Eliminar juego?"))
return;

juegos =
juegos.filter(j=>j.id!==id);

guardar();

cargarPlataformas();

renderizar();

}

document
.getElementById("search")
.addEventListener("input",renderizar);

document
.getElementById("platformFilter")
.addEventListener("change",renderizar);

document
.getElementById("gameForm")
.addEventListener("submit",agregarJuego);

cargarDatos();
