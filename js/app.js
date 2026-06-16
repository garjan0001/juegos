let juegos = [];

async function cargarDatos() {

    const response = await fetch("data/juegos.json");
    juegos = await response.json();

    cargarPlataformas();
    renderizar(juegos);
}

function cargarPlataformas() {

    const plataformas = [
        ...new Set(
            juegos.map(j => j.plataforma)
        )
    ];

    const select =
        document.getElementById("platformFilter");

    plataformas.sort().forEach(plataforma => {

        const option =
            document.createElement("option");

        option.value = plataforma;
        option.textContent = plataforma;

        select.appendChild(option);
    });
}

function renderizar(lista) {

    const container =
        document.getElementById("gamesContainer");

    container.innerHTML = "";

    lista.forEach(juego => {

        container.innerHTML += `
            <div class="game-card">
                <img src="${juego.portada}" alt="${juego.titulo}">

                <div class="game-info">
                    <div class="game-title">
                        ${juego.titulo}
                    </div>

                    <div class="platform">
                        ${juego.plataforma}
                    </div>

                    <div class="generation">
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
        `${lista.length} juegos encontrados`;
}

function filtrar() {

    const texto =
        document.getElementById("search")
        .value
        .toLowerCase();

    const plataforma =
        document.getElementById("platformFilter")
        .value;

    const resultado = juegos.filter(juego => {

        const coincideTitulo =
            juego.titulo
            .toLowerCase()
            .includes(texto);

        const coincidePlataforma =
            plataforma === "" ||
            juego.plataforma === plataforma;

        return coincideTitulo &&
               coincidePlataforma;
    });

    renderizar(resultado);
}

document
.getElementById("search")
.addEventListener("input", filtrar);

document
.getElementById("platformFilter")
.addEventListener("change", filtrar);

cargarDatos();
