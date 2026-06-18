/* =========================
   VARIABLES GLOBALES
========================= */

let juegos = [];

/* =========================
   CARGAR DATOS
========================= */

async function cargarDatos() {

    try {

        const response = await fetch(
            `data/juegos.json?v=${Date.now()}`
        );

        if (!response.ok) {
            throw new Error(
                `Error HTTP ${response.status}`
            );
        }

        juegos = await response.json();

        cargarPlataformas();
        renderizar();

    } catch (error) {

        console.error(
            "Error cargando juegos:",
            error
        );

        document.getElementById(
            "gamesContainer"
        ).innerHTML = `
            <div style="padding:20px;">
                Error cargando la colección.
            </div>
        `;
    }
}

/* =========================
   CARGAR PLATAFORMAS
========================= */

function cargarPlataformas() {

    const select =
        document.getElementById(
            "platformFilter"
        );

    select.innerHTML =
        '<option value="">Todas las plataformas</option>';

    const plataformas =
        [...new Set(
            juegos.map(
                j => j.plataforma
            )
        )];

    plataformas
        .sort((a, b) =>
            a.localeCompare(b, 'es')
        )
        .forEach(plataforma => {

            const option =
                document.createElement(
                    "option"
                );

            option.value =
                plataforma;

            option.textContent =
                plataforma;

            select.appendChild(
                option
            );
        });
}

/* =========================
   OBTENER LISTA FILTRADA
========================= */

function obtenerListaFiltrada() {

    const texto =
        document
            .getElementById("search")
            .value
            .toLowerCase()
            .trim();

    const plataforma =
        document
            .getElementById(
                "platformFilter"
            )
            .value;

    const orden =
        document
            .getElementById(
                "sortFilter"
            )
            .value;

    let lista =
        juegos.filter(juego => {

            const coincideTexto =
                juego.titulo
                    .toLowerCase()
                    .includes(texto);

            const coincidePlataforma =
                !plataforma ||
                juego.plataforma ===
                    plataforma;

            return (
                coincideTexto &&
                coincidePlataforma
            );
        });

    /* =====================
       DISPONIBLES
    ===================== */

    if (orden === "available") {

        lista = lista.filter(
            j => !j.prestadoA
        );
    }

    /* =====================
       PRESTADOS
    ===================== */

    if (orden === "loaned") {

        lista = lista.filter(
            j => j.prestadoA
        );
    }

    /* =====================
       ORDEN A-Z
    ===================== */

    if (orden === "az") {

        lista.sort((a, b) =>
            a.titulo.localeCompare(
                b.titulo,
                "es",
                {
                    sensitivity:
                        "base"
                }
            )
        );
    }

    /* =====================
       ORDEN Z-A
    ===================== */

    if (orden === "za") {

        lista.sort((a, b) =>
            b.titulo.localeCompare(
                a.titulo,
                "es",
                {
                    sensitivity:
                        "base"
                }
            )
        );
    }

    return lista;
}

/* =========================
   RENDERIZAR
========================= */

function renderizar() {

    const lista =
        obtenerListaFiltrada();

    const container =
        document.getElementById(
            "gamesContainer"
        );

    container.innerHTML = "";

    lista.forEach(juego => {

        const estadoPrestamo =
            juego.prestadoA
                ? `
                <span class="loaned">
                    🔴 Prestado a ${juego.prestadoA}
                </span>
                `
                : `
                <span class="available">
                    🟢 Disponible
                </span>
                `;

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

                    <div class="region">
                        ${juego.region}
                    </div>

                    <div class="prestamo">
                        ${estadoPrestamo}
                    </div>

                </div>

            </div>
        `;
    });

    document.getElementById(
        "stats"
    ).textContent =
        `Total juegos: ${lista.length}`;
}

/* =========================
   EVENTOS
========================= */

document
    .getElementById("search")
    .addEventListener(
        "input",
        renderizar
    );

document
    .getElementById(
        "platformFilter"
    )
    .addEventListener(
        "change",
        renderizar
    );

document
    .getElementById(
        "sortFilter"
    )
    .addEventListener(
        "change",
        renderizar
    );

/* =========================
   INICIO
========================= */

cargarDatos();
