from django.shortcuts import render
from django.http import JsonResponse
# Importar todos los scrapers y servicios
from .scrapers.scraper_lareina import ScraperLaReina
from .scrapers.scraper_carrefour import ScraperCarrefour
from .scrapers.scraper_lagallega import ScraperLaGallega
from .services import NormalizadorProductos
from .models import Supermercado, Producto, Precio
from django.utils import timezone
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

def buscar_productos(request):
    query = request.GET.get('query', '')

    if not query:
        return JsonResponse({
            'error': 'faltan parametros query'
        }, status=400)
    
    # Usar múltiples scrapers en paralelo
    scrapers = [
        ScraperLaReina(),
        ScraperCarrefour(),
        ScraperLaGallega()
    ]
    
    # Ejecutar scrapers en paralelo para mayor velocidad
    todos_productos = []
    with ThreadPoolExecutor(max_workers=3) as executor:
        # Enviar tareas a los scrapers
        futures = {executor.submit(scraper.buscar_productos, query): scraper for scraper in scrapers}
        
        # Recopilar resultados
        for future in as_completed(futures, timeout=30):
            try:
                productos_scrapeados = future.result()
                todos_productos.extend(productos_scrapeados)
            except Exception as e:
                scraper_name = futures[future].supermercado_nombre
                print(f"Error en scraper {scraper_name}: {e}")
    
    # Normalizar y consolidar resultados
    normalizador = NormalizadorProductos()
    productos_relevantes = normalizador.buscar_productos_similares(todos_productos, query)
    
    # Guardar en base de datos y preparar respuesta
    resultados = []
    for producto_data in productos_relevantes:
        # Crear o buscar supermercado
        supermercado, _ = Supermercado.objects.get_or_create(
            nombre=producto_data['supermercado'],
            defaults={
                'url_sitio': producto_data['url'],
                'activo': True
            }
        )
        
        # Crear o buscar producto
        producto, _ = Producto.objects.get_or_create(
            nombre=producto_data['nombre'],
            defaults={'categoria': 'General'}
        )
        
        # Crear precio actual
        precio = Precio.objects.create(
            supermercado=supermercado,
            producto=producto,
            precio=producto_data['precio'],
            url_producto=producto_data['url']
        )
        
        # Agregar a resultados con información extra
        resultados.append({
            'nombre': producto.nombre,
            'precio': float(precio.precio),
            'supermercado': supermercado.nombre,
            'fecha': precio.fecha.isoformat(),
            'relevancia': producto_data.get('relevancia', 0)
        })
    
    # Estadísticas por supermercado
    supermercados_stats = {}
    for resultado in resultados:
        super_name = resultado['supermercado']
        if super_name not in supermercados_stats:
            supermercados_stats[super_name] = 0
        supermercados_stats[super_name] += 1
    
    return JsonResponse({
        'query': query,
        'total_encontrados': len(resultados),
        'supermercados_consultados': list(supermercados_stats.keys()),
        'productos_por_supermercado': supermercados_stats,
        'resultados': resultados
    })
  