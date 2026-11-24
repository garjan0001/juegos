import json
import time
import re
import unicodedata
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

MAPA_SLUGS = {
    'playstation': 'playstation',
    'playstation 1': 'playstation',
    'ps1': 'playstation',
    'playstation 2': 'playstation-2',
    'ps2': 'playstation-2',
    'playstation 3': 'playstation-3',
    'ps3': 'playstation-3',
    'playstation 4': 'playstation-4',
    'ps4': 'playstation-4',
    'psp': 'psp',
    'ps vita': 'playstation-vita',
    'nintendo switch': 'nintendo-switch',
    'wii': 'wii',
    'wii u': 'wii-u',
    'nintendo ds': 'nintendo-ds',
    'nintendo 3ds': 'nintendo-3ds',
    'game boy': 'gameboy',
    'game boy color': 'gameboy-color',
    'game boy advance': 'gameboy-advance',
    'super nintendo': 'super-nintendo',
    'nes': 'nes',
    'nintendo 64': 'nintendo-64',
    'gamecube': 'gamecube',
    'megadrive': 'sega-genesis',
    'mega drive': 'sega-genesis',
    'dreamcast': 'sega-dreamcast',
    'xbox': 'xbox',
    'xbox 360': 'xbox-360',
    'xbox one': 'xbox-one'
}

def a_slug(texto):
    texto = unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode('ascii')
    texto = texto.lower().replace('&', 'and')
    texto = re.sub(r'[^a-z0-9]+', '-', texto).strip('-')
    return texto

def leer_ficha_directa(consola_slug, juego_slug):
    url = f"https://pricecharting.com{consola_slug}/{juego_slug}"
    res = SESSION.get(url, timeout=15)
    if res.status_code != 200:
        return None

    soup = BeautifulSoup(res.text, 'html.parser')
    # #complete_price = Completo con caja y manual (CIB), #used_price = Suelto
    for selector in ['#complete_price .price', '#used_price .price']:
        el = soup.select_one(selector)
        if el:
            m = re.search(r'\$(\d+(?:,\d{3})*\.\d{2})', el.get_text())
            if m:
                return round(float(m.group(1).replace(',', '')) * TASA_USD_A_EUR, 2)
    return None

def obtener_precio_pricecharting(titulo, plataforma, region=""):
    base_consola = MAPA_SLUGS.get(plataforma.lower().strip(), a_slug(plataforma))
    juego_slug = a_slug(titulo)
    es_pal = 'pal' in region.lower()

    candidatas = []
    if es_pal:
        candidatas.append(f"pal-{base_consola}")
    candidatas.append(base_consola)

    for consola_slug in candidatas:
        precio = leer_ficha_directa(consola_slug, juego_slug)
        if precio is not None:
            return precio
        time.sleep(0.5)

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
            print("  -> No encontrado (slug distinto)", flush=True)
        
        time.sleep(0.8)

    with open(RUTA_JSON, 'w', encoding='utf-8') as f:
        json.dump(juegos, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()
