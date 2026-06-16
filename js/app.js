let juegos = [];

const STORAGE_KEY = "mi_coleccion_juegos";

async function init() {

    const stored = localStorage.getItem(STORAGE_KEY);

    if (stored) {
        juegos = JSON.parse(stored);
    } else {
        const res = await fetch("data/juegos.json");
        juegos = await res.json();
        save();
    }

    cargarPlataformas();
    render();
}

function save() {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(juegos));
}

/* =========================
   PORTADAS AUTOMÁTICAS
========================= */

function generarPortada(titulo, plataforma) {

    // Esto genera una "carátula temporal" que SI se ve
    return `https://via.placeholder.com/300x420?text=${encodeURIComponent(titulo)}`;
}

/* =========================
   AÑADIR JUEGO
========================= */

function addGame(e) {
    e.preventDefault();

    const titulo = document.getElementById("title").value;
    const plataforma = document.getElementById("platform").value;
    const generacion = document.getElementById("generation").value;
    const region = document.getElementById("region").value;

    const juego = {
        id: Date.now(),
        titulo,
        plataforma,
        generacion,
        region,
        portada: generarPortada(titulo, plataforma)
    };

    juegos.push(juego);

    save();
    render();
    e.target.reset();
}

/* =========================
   ELIMINAR
========================= */

function deleteGame(id) {
    juegos = juegos.filter(j => j.id !== id);
    save();
    render();
}

/* =========================
   FILTROS
========================= */

function filterGames() {

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
    const lista = filterGames();

    container.innerHTML = "";

    lista.forEach(j => {

        container.innerHTML += `
        <div class="game-card">
            <img src="${j.portada}" alt="${j.titulo}">

            <div class="game-info">
                <div class="game-title">${j.titulo}</div>
                <div>${j.plataforma}</div>
                <div>${j.generacion}</div>
                <div>${j.region}</div>

                <button onclick="deleteGame(${j.id})">
                    ❌ Eliminar
                </button>
            </div>
        </div>
        `;
    });

    document.getElementById("stats").textContent =
        `Total: ${lista.length} juegos`;
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
