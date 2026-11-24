import json
import time
import re
import requests
from bs4 import BeautifulSoup

RUTA_JSON = 'data/juegos.json'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8'
}

# Conversión aproximada USD -> EUR (PriceCharting da precios base en USD)
TASA_USD_A_EUR = 0.92

# Mapeo de nombres de plataforma de tu JSON al formato de PriceCharting
MAPA_CONSOLAS = {
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

def obtener_precio_pricecharting(titulo, plataforma, region=""):
    consola_slug = MAPA_CONSOLAS.get(plataforma.lower().strip(), plataforma)
    # Si el juego es PAL, añadir 'PAL' ayuda a encontrar la edición europea
    es_pal = 'pal' in region.lower()
    query = f"{titulo} {consola_slug}" + (" PAL" if es_pal else "")
    
    url = "https://pricecharting.com"
    params = {'q': query, 'type': 'prices'}
    
    try:
        res = requests.get(url, params=params, headers=HEADERS, timeout=15)
        if res.status_code != 200:
            print(f"  [Aviso] Código HTTP: {res.status_code}")
            return None

        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Caso 1: Redirige directamente a la ficha del juego
        cib_price = soup.select_one('#complete_price .price, #used_price .price')
        if cib_price:
            texto = cib_price.get_text().strip()
            match = re.search(r'(\d+(?:,\d{3})*\.\d{2})', texto)
            if match:
                usd = float(match.group(1).replace(',', ''))
                return round(usd * TASA_USD_A_EUR, 2)

        # Caso 2: Muestra tabla de resultados de búsqueda (tomamos el primer resultado)
        fila = soup.select_one('table#games_table tbody tr')
        if fila:
            # Columna cib_price (completo con caja) o used_price (suelto)
            celda = fila.select_one('td.cib_price, td.used_price')
            if celda:
                texto = celda.get_text().strip()
                match = re.search(r'(\d+(?:,\d{3})*\.\d{2})', texto)
                if match:
                    usd = float(match.group(1).replace(',', ''))
                    return round(usd * TASA_USD_A_EUR, 2)

        print("  [Aviso] Juego no encontrado en catálogo")
    except Exception as e:
        print(f"  [Error] {e}")
    
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
        
        time.sleep(1.5)

    with open(RUTA_JSON, 'w', encoding='utf-8') as f:
        json.dump(juegos, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()
