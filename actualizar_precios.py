import json
import time
import re
import statistics
import urllib.parse
import requests
from bs4 import BeautifulSoup

RUTA_JSON = 'data/juegos.json'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept-Language': 'es-ES,es;q=0.9'
}

def obtener_precio_ebay(titulo, plataforma):
    query = urllib.parse.quote(f"{titulo} {plataforma}")
    url = f"https://ebay.es{query}&LH_Sold=1&LH_Complete=1"
    
    try:
        res = requests.get(url, headers=HEADERS, timeout=15)
        if res.status_code != 200:
            print(f"  [Aviso] Código HTTP: {res.status_code}")
            return None
        
        if "Pardon Our Interruption" in res.text or "captcha" in res.text.lower():
            print("  [Bloqueo] eBay bloqueó la petición (CAPTCHA / Anti-bot)")
            return None

        soup = BeautifulSoup(res.text, 'html.parser')
        precios = []
        
        # Busca tanto el selector clásico como el nuevo diseño de eBay
        items = soup.select('.s-item__price, .s-card__price')
        for item in items[:12]:
            texto = item.get_text().strip()
            if ' a ' in texto or ' to ' in texto:
                continue
            match = re.search(r'(\d+(?:\.\d{3})*,\d{2})', texto)
            if match:
                valor = float(match.group(1).replace('.', '').replace(',', '.'))
                if 1.0 < valor < 2000.0:
                    precios.append(valor)
        
        if precios:
            return round(statistics.median(precios), 2)
        else:
            print(f"  [Aviso] HTML recibido ({len(res.text)} bytes), pero 0 precios encontrados.")
    except Exception as e:
        print(f"  [Error] {e}")
    
    return None


def main():
    with open(RUTA_JSON, 'r', encoding='utf-8') as f:
        juegos = json.load(f)

    for juego in juegos:
        titulo = juego.get('titulo', '')
        plataforma = juego.get('plataforma', '')
        print(f"Buscando precio: {titulo} ({plataforma})...")
        
        precio = obtener_precio_ebay(titulo, plataforma)
        if precio is not None:
            juego['precio'] = precio
            print(f"  -> {precio} €")
        else:
            # Mantiene el precio anterior si falla una consulta puntual
            juego.setdefault('precio', 0.0)
            print("  -> Sin cambios")
        
        # Pausa obligatoria para evitar bloqueos en +200 peticiones
        time.sleep(2.5)

    with open(RUTA_JSON, 'w', encoding='utf-8') as f:
        json.dump(juegos, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()

