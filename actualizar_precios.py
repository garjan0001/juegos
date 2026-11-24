import json
import time
import re
import requests
from bs4 import BeautifulSoup

RUTA_JSON = 'data/juegos.json'

SESSION = requests.Session()
SESSION.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9'
})

TASA_USD_A_EUR = 0.92

MAPA_CONSOLAS = {
    'playstation': 'Playstation',
    'playstation 1': 'Playstation',
    'ps1': 'Playstation',
    'playstation 2': 'Playstation 2',
    'ps2': 'Playstation 2',
    'playstation 3': 'Playstation 3',
    'ps3': 'Playstation 3',
    'playstation 4': 'Playstation 4',
    'ps4': 'Playstation 4',
    'psp': 'PSP',
    'ps vita': 'Playstation Vita',
    'nintendo switch': 'Nintendo Switch',
    'wii': 'Wii',
    'wii u': 'Wii U',
    'nintendo ds': 'Nintendo DS',
    'nintendo 3ds': 'Nintendo 3DS',
    'game boy': 'GameBoy',
    'game boy color': 'GameBoy Color',
    'game boy advance': 'GameBoy Advance',
    'super nintendo': 'Super Nintendo',
    'nes': 'NES',
    'nintendo 64': 'Nintendo 64',
    'gamecube': 'GameCube',
    'megadrive': 'Sega Genesis',
    'mega drive': 'Sega Genesis',
    'dreamcast': 'Sega Dreamcast',
    'xbox': 'Xbox',
    'xbox 360': 'Xbox 360',
    'xbox one': 'Xbox One'
}

def consultar_url(query, debug=False):
    url = "https://pricecharting.com"
    res = SESSION.get(url, params={'q': query, 'type': 'prices'}, timeout=15)
    if res.status_code != 200:
        return None, res.status_code

    soup = BeautifulSoup(res.text, 'html.parser')
    if debug:
        titulo_pag = soup.title.string.strip() if soup.title else "Sin título"
        print(f"  [Debug] URL: {res.url} | Título: {titulo_pag}", flush=True)

    # 1. Si redirige directo a la ficha del juego
    for selector in ['#complete_price .price', '#used_price .price']:
        el = soup.select_one(selector)
        if el:
            m = re.search(r'\$(\d+(?:,\d{3})*\.\d{2})', el.get_text())
            if m:
                return round(float(m.group(1).replace(',', '')) * TASA_USD_A_EUR, 2), 200

    # 2. Si muestra la tabla de resultados
    for fila in soup.select('table#games_table tbody tr, table tbody tr'):
        celdas = fila.select('td.price')
        if celdas:
            # Índice 1 = CIB (completo con caja), Índice 0 = Loose (suelto)
            orden = [celdas[1], celdas[0]] if len(celdas) >= 2 else [celdas[0]]
            for celda in orden:
                m = re.search(r'\$(\d+(?:,\d{3})*\.\d{2})', celda.get_text())
                if m:
                    return round(float(m.group(1).replace(',', '')) * TASA_USD_A_EUR, 2), 200

    return None, 200

def obtener_precio_pricecharting(titulo, plataforma, region="", debug=False):
    consola = MAPA_CONSOLAS.get(plataforma.lower().strip(), plataforma)
    es_pal = 'pal' in region.lower()

    if es_pal:
        precio, status = consultar_url(f"PAL {titulo} {consola}", debug=debug)
        if precio is not None:
            return precio
        time.sleep(0.8)

    precio, status = consultar_url(f"{titulo} {consola}", debug=debug)
    if precio is not None:
        return precio

    if status != 200:
        print(f"  [Aviso] Código HTTP: {status}", flush=True)
    else:
        print("  [Aviso] Sin coincidencias en PriceCharting", flush=True)
    return None

def main():
    with open(RUTA_JSON, 'r', encoding='utf-8') as f:
        juegos = json.load(f)

    for i, juego in enumerate(juegos):
        titulo = juego.get('titulo', '')
        plataforma = juego.get('plataforma', '')
        region = juego.get('region', '')
        print(f"Buscando precio: {titulo} ({plataforma})...", flush=True)
        
        precio = obtener_precio_pricecharting(titulo, plataforma, region, debug=(i == 0))
        if precio is not None:
            juego['precio'] = precio
            print(f"  -> {precio} €", flush=True)
        else:
            juego.setdefault('precio', 0.0)
            print("  -> Sin cambios", flush=True)
        
        time.sleep(1.2)

    with open(RUTA_JSON, 'w', encoding='utf-8') as f:
        json.dump(juegos, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()
