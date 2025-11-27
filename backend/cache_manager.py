#!/usr/bin/env python3
"""
Sistema de caché inteligente para productos
============================================

Guarda productos en JSON con estructura:
{
  "supermercado": {
    "producto_nombre": {
      "categoria": "02000000",
      "precio": 1500.50,
      "imagen_url": "https://www.lagallega.com.ar/imagenes/producto.jpg",
      "url": "https://..."
    }
  }
}

NOTA: Solo guarda URLs de imágenes, NO las descarga.
Android + Glide manejan la descarga y caché eficientemente.
"""

import json
import os
from datetime import datetime
import re

class CacheManager:
    def __init__(self, cache_file='productos_cache.json'):
        self.cache_file = cache_file
        self.cache = self._cargar_cache()
    
    def _cargar_cache(self):
        """Carga el caché desde archivo JSON"""
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️ Error cargando caché: {e}")
                return self._cache_vacio()
        return self._cache_vacio()
    
    def _cache_vacio(self):
        """Estructura de caché vacío"""
        return {
            'last_update': None,
            'productos': {
                'lagallega': {},
                'lareina': {},
                'carrefour': {},
                'dia': {}
            }
        }
    
    def guardar_cache(self):
        """Guarda el caché en archivo JSON"""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, ensure_ascii=False, indent=2)
            print(f"💾 Caché guardado: {len(self.cache['productos'])} supermercados")
        except Exception as e:
            print(f"❌ Error guardando caché: {e}")
    

    
    def agregar_producto(self, supermercado, nombre, categoria, precio, url, imagen_url=None):
        """
        Agrega o actualiza producto en el caché
        
        Args:
            supermercado: 'lagallega', 'lareina', 'carrefour', 'dia'
            nombre: Nombre del producto
            categoria: Código de categoría (ej: "02000000")
            precio: Precio actual
            url: URL del producto
            imagen_url: URL de la imagen (SOLO URL, no se descarga)
        """
        if supermercado not in self.cache['productos']:
            self.cache['productos'][supermercado] = {}
        
        # SOLO guardar la URL de la imagen, NO descargar
        # Android + Glide se encargan de descargar y cachear eficientemente
        
        # Guardar en caché
        self.cache['productos'][supermercado][nombre] = {
            'categoria': categoria,
            'precio': precio,
            'imagen_url': imagen_url,  # Solo URL, no descarga
            'url': url,
            'last_update': datetime.now().isoformat()
        }
    
    def buscar_producto(self, supermercado, query):
        """
        Busca productos en el caché que coincidan con el query
        Retorna lista de productos con su categoría
        
        BÚSQUEDA FLEXIBLE: Busca si CUALQUIER palabra del query está en el nombre
        """
        if supermercado not in self.cache['productos']:
            return []
        
        query_lower = query.lower()
        palabras_query = query_lower.split()
        
        # Remover stopwords
        stopwords = {'de', 'del', 'la', 'el', 'los', 'las', 'un', 'una', 'y', 'con', 'sin'}
        palabras_query = [p for p in palabras_query if p not in stopwords]
        
        if not palabras_query:
            palabras_query = query_lower.split()
        
        resultados = []
        for nombre, datos in self.cache['productos'][supermercado].items():
            # Agregar espacios al inicio y fin para búsqueda de palabras completas
            nombre_lower = ' ' + nombre.lower() + ' '
            
            # Verificar que TODAS las palabras del query estén presentes
            # "pan" → acepta "pan lactal", "bizcochos de pan"
            # "dulce de leche" → acepta "dulce de leche", "dulce leche condensada"
            # NO encuentra: "emPANada", "camPANa"
            tiene_todas = True
            for palabra in palabras_query:
                # Buscar palabra con espacio antes (word boundary)
                if ' ' + palabra not in nombre_lower:
                    tiene_todas = False
                    break
            
            if tiene_todas:
                resultados.append({
                    'nombre': nombre,
                    'categoria': datos['categoria'],
                    'precio': datos['precio'],
                    'imagen_url': datos.get('imagen_url'),  # Solo URL
                    'url': datos['url']
                })
        
        return resultados
    
    def actualizar_desde_scraper(self, supermercado, productos_scrapeados):
        """
        Actualiza caché masivamente desde resultado de scraper
        
        Args:
            supermercado: nombre del supermercado
            productos_scrapeados: lista de productos del scraper con estructura:
                [{'nombre': '...', 'precio': ..., 'categoria': '...', 'imagen': '...', 'url': '...'}]
        """
        print(f"🔄 Actualizando caché de {supermercado}: {len(productos_scrapeados)} productos...")
        
        for prod in productos_scrapeados:
            self.agregar_producto(
                supermercado=supermercado,
                nombre=prod.get('nombre', ''),
                categoria=prod.get('categoria', ''),
                precio=prod.get('precio', 0),
                url=prod.get('url', ''),
                imagen_url=prod.get('imagen')
            )
        
        self.cache['last_update'] = datetime.now().isoformat()
        self.guardar_cache()
        print(f"✅ Caché actualizado para {supermercado}")
    
    def obtener_estadisticas(self):
        """Retorna estadísticas del caché"""
        stats = {}
        for super_nombre, productos in self.cache['productos'].items():
            stats[super_nombre] = {
                'total_productos': len(productos),
                'con_imagen': sum(1 for p in productos.values() if p.get('imagen_url'))
            }
        return stats


# Instancia global del cache manager
cache_manager = CacheManager()
