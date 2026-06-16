let juegos = [];

const STORAGE_KEY = "coleccion_juegos";

/* =========================
   INIT
========================= */
async function init() {

    const saved = localStorage.getItem(STORAGE_KEY);

    if (saved) {
        juegos = JSON.parse(saved);
    } else {
        const res = await fetch("data/juegos.json");
        juegos = await res.json();
        save();
    }

    cargarPlataformas();
    render();

    document.getElementById("gameForm")
        .addEventListener("submit", addGame);
}

/* =========================
   GUARDAR
========================= */
function save() {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(juegos));
}

/* =========================
   PORTADAS (FUNCIONALES)
   -> EVITA ERRORES
========================= */
function generarPortada(titulo) {

    return `https://placehold.co/300x420/111/ffffff?text=${encodeURIComponent(titulo)}`;
}

/* =========================
   AÑADIR JUEGO
========================= */
function addGame(e) {
    e.preventDefault();

    const juego = {
        id: Date.now(),
        titulo: document.getElementById("title").value,
        plataforma: document.getElementById("platform").value,
        generacion: document.getElementById("generation").value,
        region: document.getElementById("region").value,
        portada: generarPortada(
            document.getElementById("title").value,
            document.getElementById("platform").value
        )
    };

    juegos.push(juego);
    save();
    render();

    e.target.reset();
}

/* =========================
   BORRAR
========================= */
function deleteGame(id) {
    juegos = juegos.filter(j => j.id !== id);
    save();
    render();
}

/* =========================
   FILTRO
========================= */
function getFiltered() {

    const text = document.getElementById("search").value.toLowerCase();
    const platform = document.getElementById("platformFilter").value;

    return juegos.filter(j => {

        const matchText = j.titulo.toLowerCase().includes(text);
        const matchPlatform = !platform || j.plataforma === platform;

        return matchText && matchPlatform;
    });
}

/* =========================
   RENDER
========================= */
function render() {

    const container = document.getElementById("gamesContainer");
    const list = getFiltered();

    container.innerHTML = "";

    list.forEach(j => {

        container.innerHTML += `
        <div class="card">
            <img src="${j.portada}" alt="${j.titulo}">
            <div class="card-info">
                <h3>${j.titulo}</h3>
                <p>${j.plataforma}</p>
                <p>${j.generacion}</p>
                <p>${j.region}</p>

                <button class="delete" onclick="deleteGame(${j.id})">
                    Eliminar
                </button>
            </div>
        </div>
        `;
    });

    document.getElementById("stats").textContent =
        `Total juegos: ${list.length}`;
}

/* =========================
   PLATAFORMAS
========================= */
function cargarPlataformas() {

    const select = document.getElementById("platformFilter");

    const plataformas = [...new Set(juegos.map(j => j.plataforma))];

    plataformas.forEach(p => {
        const opt = document.createElement("option");
        opt.value = p;
        opt.textContent = p;
        select.appendChild(opt);
    });
}

/* =========================
   EVENTOS
========================= */
document.getElementById("search").addEventListener("input", render);
document.getElementById("platformFilter").addEventListener("change", render);

init();
