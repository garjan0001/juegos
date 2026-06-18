let juegos = [];

/* =========================
   CARGA DE DATOS
========================= */

async function cargarDatos() {

    const response = await fetch(
        "data/juegos.json?v=" + Date.now()
    );

    juegos = await response.json();

    cargarPlataformas();
    renderizar();
}

/* =========================
   PLATAFORMAS
========================= */

function cargarPlataformas() {

    const select = document.getElementById("platformFilter");

    select.innerHTML = '<option value="">Todas las plataformas</option>';

    const plataformas = [...new Set(juegos.map(j => j.plataforma))];

    plataformas.sort().forEach(p => {

        const option = document.createElement("option");

        option.value = p;
        option.textContent = p;

        select.appendChild(option);
    });
}

/* =========================
   FILTRO + RENDER
========================= */

function renderizar() {

    const texto = document.getElementById("search").value.toLowerCase();
    const plataforma = document.getElementById("platformFilter").value;

    const lista = juegos.filter(j => {

        const matchText = j.titulo.toLowerCase().includes(texto);
        const matchPlatform = !plataforma || j.plataforma === plataforma;

        return matchText && matchPlatform;
    });

    const container = document.getElementById("gamesContainer");

    container.innerHTML = "";

    lista.forEach(j => {

        container.innerHTML += `
        <div class="game-card">

            <img src="${j.portada}" alt="${j.titulo}"
                 onerror="this.src='images/no-image.jpg'">

            <div class="game-info">

                <div class="game-title">${j.titulo}</div>
                <div class="platform">${j.plataforma}</div>
                <div>${j.region}</div>

                <div class="prestamo">
                    ${
                        j.prestadoA
                        ? `<span class="loaned">🔴 Prestado a ${j.prestadoA}</span>`
                        : `<span class="available">🟢 Disponible</span>`
                    }
                </div>

            </div>
        </div>
        `;
    });

    document.getElementById("stats").textContent =
        `Total juegos: ${lista.length}`;
}

/* =========================
   EVENTOS
========================= */

document.getElementById("search").addEventListener("input", renderizar);
document.getElementById("platformFilter").addEventListener("change", renderizar);

cargarDatos();
