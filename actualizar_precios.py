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
    # Misma URL de artículos vendidos que usas en tu web
    url = f"https://ebay.es{query}&LH_Sold=1&LH_Complete=1"
    
    try:
        res = requests.get(url, headers=HEADERS, timeout=15)
        if res.status_code != 200:
            return None
        
        soup = BeautifulSoup(res.text, 'html.parser')
        precios = []
        
        # Extraer los primeros 10 resultados vendidos
        for item in soup.select('.s-item__price')[:10]:
            texto = item.get_text()
            # Ignorar rangos de precios (ej. "10,00 EUR a 20,00 EUR")
            if ' a ' in texto:
                continue
            match = re.search(r'(\d+[.,]\d+)', texto)
            if match:
                valor = float(match.group(1).replace('.', '').replace(',', '.'))
                if 1.0 < valor < 2000.0: # Filtro básico contra errores
                    precios.append(valor)
        
        # Usar la mediana evita que precios absurdos alteren el valor real
        if precios:
            return round(statistics.median(precios), 2)
    except Exception as e:
        print(f"Error buscando {titulo}: {e}")
    
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

