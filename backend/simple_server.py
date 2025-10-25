#!/usr/bin/env python3
"""
PreciosCerca - Servidor Principal
================================

Servidor Flask que proporciona una API REST para buscar productos y precios
en supermercados argentinos usando web scraping.

Actualmente soporta:
- Carrefour (API VTEX) ✅

Autor: PreciosCerca Team
Fecha: Octubre 2025
"""

from flask import Flask, jsonify, request
import sys
import os

# Agregar el directorio backend al path de Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

print("🚀 Inicializando PreciosCerca Server...")

try:
    from productos.scrapers.scraper_carrefour import ScraperCarrefour
    print("✅ Carrefour scraper cargado correctamente")
except Exception as e:
    print(f"❌ Error cargando scrapers: {e}")
    sys.exit(1)

app = Flask(__name__)

# Inicializar scrapers disponibles
scrapers = {
    'carrefour': ScraperCarrefour()
}

print(f"✅ {len(scrapers)} scraper(s) inicializado(s)")

@app.route('/products', methods=['GET'])
def buscar_productos():
    """
    Endpoint principal para buscar productos.
    
    Parámetros:
    - query: término de búsqueda (ej: "leche", "pan", "jabón")
    
    Retorna JSON con estructura compatible con app Android:
    {
        "query": "leche",
        "total_encontrados": 50,
        "supermercados_consultados": ["Carrefour"],
        "productos_por_supermercado": {"Carrefour": 50},
        "resultados": [...]
    }
    """
    query = request.args.get('query', request.args.get('q', 'leche'))
    
    print(f"🔍 Búsqueda: '{query}'")
    
    try:
        todos_los_productos = []
        supermercados_consultados = []
        productos_por_supermercado = {}
        
        # Buscar en Carrefour (único scraper funcionando actualmente)
        carrefour_productos = scrapers['carrefour'].buscar_productos(query)
        todos_los_productos.extend(carrefour_productos)
        supermercados_consultados.append('Carrefour')
        productos_por_supermercado['Carrefour'] = len(carrefour_productos)
        
        # Ordenar por precio (más barato primero)
        todos_los_productos.sort(key=lambda x: x['precio'])
        
        # Convertir al formato que espera la app Android
        resultados = []
        for producto in todos_los_productos:
            resultados.append({
                'nombre': producto['nombre'],
                'precio': producto['precio'],
                'supermercado': producto['supermercado'],
                'fecha': '2025-10-24',
                'relevancia': 1.0
            })
        
        print(f"✅ {len(resultados)} productos encontrados")
        
        # Respuesta en formato Android
        response = {
            'query': query,
            'total_encontrados': len(resultados),
            'supermercados_consultados': supermercados_consultados,
            'productos_por_supermercado': productos_por_supermercado,
            'resultados': resultados
        }
        
        return jsonify(response)
        
    except Exception as e:
        print(f"❌ Error en búsqueda: {e}")
        return jsonify({
            'error': str(e),
            'query': query,
            'total_encontrados': 0,
            'supermercados_consultados': [],
            'productos_por_supermercado': {},
            'resultados': []
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de salud para verificar que el servidor funciona."""
    return jsonify({
        'status': 'OK', 
        'message': 'PreciosCerca Server funcionando',
        'scrapers_disponibles': list(scrapers.keys()),
        'version': '1.0.0'
    })

@app.route('/', methods=['GET'])
def info():
    """Información básica del servidor."""
    return jsonify({
        'app': 'PreciosCerca API',
        'descripcion': 'API para comparar precios en supermercados argentinos',
        'supermercados_soportados': list(scrapers.keys()),
        'endpoints': {
            '/products?query=TERMINO': 'Buscar productos',
            '/health': 'Estado del servidor'
        }
    })

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🏪 PRECIOSCERCA SERVER - DATOS REALES")
    print("="*60)
    print("📍 URL: http://localhost:8000")
    print("� Supermercados disponibles:", ", ".join(scrapers.keys()))
    print("📱 Compatible con app Android PreciosCerca")
    print("🔍 Endpoint: /products?query=PRODUCTO")
    print("="*60)
    
    app.run(host='0.0.0.0', port=8000, debug=False)