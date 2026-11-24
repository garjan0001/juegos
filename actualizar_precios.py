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

def consultar_url(query):
    url = "https://pricecharting.com"
    res = SESSION.get(url, params={'q': query}, timeout=15)
    if res.status_code != 200:
        return None, res.status_code

    soup = BeautifulSoup(res.text, 'html.parser')

    # 1. Si entra directo en la ficha del juego
    for selector in ['#complete_price .price', '#used_price .price']:
        el = soup.select_one(selector)
        if el:
            m = re.search(r'(\d+(?:,\d{3})*\.\d{2})', el.get_text())
            if m:
                return round(float(m.group(1).replace(',', '')) * TASA_USD_A_EUR, 2), 200

    # 2. Si devuelve tabla de resultados (busca cualquier celda con precio $)
    for fila in soup.select('table tr'):
        celdas = fila.select('td.price, td.cib_price, td.used_price')
        # Normalmente la 2ª columna de precio es CIB (completo) y la 1ª es Loose (suelto)
        candidatas = [celdas[1], celdas[0]] if len(celdas) >= 2 else celdas
        for c in candidatas:
            m = re.search(r'\$(\d+(?:,\d{3})*\.\d{2})', c.get_text())
            if m:
                return round(float(m.group(1).replace(',', '')) * TASA_USD_A_EUR, 2), 200

    return None, 200

def obtener_precio_pricecharting(titulo, plataforma, region=""):
    consola = MAPA_CONSOLAS.get(plataforma.lower().strip(), plataforma)
    es_pal = 'pal' in region.lower()

    # Intento 1: con PAL si corresponde
    if es_pal:
        precio, status = consultar_url(f"PAL {titulo} {consola}")
        if precio is not None:
            return precio
        time.sleep(0.8)

    # Intento 2: búsqueda estándar sin región
    precio, status = consultar_url(f"{titulo} {consola}")
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

    for juego in juegos:
        titulo = juego.get('titulo', '')
        plataforma = juego.get('plataforma', '')
        region = juego.get('region', '')
        print(f"Buscando precio: {titulo} ({plataforma})...", flush=True)
        
        precio = obtener_precio_pricecharting(titulo, plataforma, region)
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
