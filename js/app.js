let juegos = [];

/* =========================
   CARGAR DATOS
========================= */

async function cargarDatos() {

    try {

        const response = await fetch(
            `data/juegos.json?v=${Date.now()}`
        );

        juegos = await response.json();

        cargarPlataformas();
        renderizar();

    } catch (error) {

        console.error("Error cargando juegos:", error);

        document.getElementById("gamesContainer").innerHTML =
            "<p>Error cargando la colección.</p>";
    }
}

/* =========================
   CARGAR PLATAFORMAS
========================= */

function cargarPlataformas() {

    const select =
        document.getElementById("platformFilter");

    select.innerHTML =
        '<option value="">Todas las plataformas</option>';

    const plataformas =
        [...new Set(juegos.map(j => j.plataforma))];

    plataformas.sort();

    plataformas.forEach(plataforma => {

        const option =
            document.createElement("option");

        option.value = plataforma;
        option.textContent = plataforma;

        select.appendChild(option);
    });
}

/* =========================
   FILTRAR Y RENDERIZAR
========================= */

function renderizar() {

    const texto =
        document.getElementById("search")
            .value
            .toLowerCase();

    const plataforma =
        document.getElementById("platformFilter")
            .value;

    const lista = juegos.filter(juego => {

        const coincideTexto =
            juego.titulo
                .toLowerCase()
                .includes(texto);

        const coincidePlataforma =
            plataforma === "" ||
            juego.plataforma === plataforma;

        return coincideTexto &&
               coincidePlataforma;
    });

    const container =
        document.getElementById("gamesContainer");

    container.innerHTML = "";

    lista.forEach(juego => {

        container.innerHTML += `
            <div class="game-card">

                <img
                    src="${juego.portada}"
                    alt="${juego.titulo}"
                    loading="lazy"
                    onerror="this.src='images/no-image.jpg'"
                >

                <div class="game-info">

                    <div class="game-title">
                        ${juego.titulo}
                    </div>

                    <div class="platform">
                        ${juego.plataforma}
                    </div>

                    <div>
                        ${juego.generacion}
                    </div>

                    <div class="region">
                        ${juego.region}
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

document
    .getElementById("search")
    .addEventListener("input", renderizar);

document
    .getElementById("platformFilter")
    .addEventListener("change", renderizar);

/* =========================
   INICIO
========================= */

cargarDatos();
