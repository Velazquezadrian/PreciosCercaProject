#!/usr/bin/env python3
"""
Datos de ubicaciones de sucursales de supermercados en Argentina
Incluye coordenadas GPS para calcular distancias
"""

# Diccionario de sucursales por supermercado
# Sucursales reales de La Gallega en Rosario obtenidas de Tiendeo
SUCURSALES = {
    'La Gallega': [
        {
            'nombre': 'La Gallega - Dorrego',
            'direccion': 'Dorrego 965, Rosario',
            'lat': -32.9476,
            'lng': -60.6395,
            'ciudad': 'Rosario'
        },
        {
            'nombre': 'La Gallega - Pellegrini 1966',
            'direccion': 'Av. Pellegrini 1966, Rosario',
            'lat': -32.9542,
            'lng': -60.6405,
            'ciudad': 'Rosario'
        },
        {
            'nombre': 'La Gallega - Pellegrini 1194',
            'direccion': 'Av. Pellegrini 1194, Rosario',
            'lat': -32.9485,
            'lng': -60.6358,
            'ciudad': 'Rosario'
        },
        {
            'nombre': 'La Gallega - Catamarca',
            'direccion': 'Catamarca 1498, Rosario',
            'lat': -32.9622,
            'lng': -60.6462,
            'ciudad': 'Rosario'
        },
        {
            'nombre': 'La Gallega - Urquiza',
            'direccion': 'Urquiza 1145, Rosario',
            'lat': -32.9615,
            'lng': -60.6520,
            'ciudad': 'Rosario'
        },
        {
            'nombre': 'La Gallega - Balcarce',
            'direccion': 'Balcarce 248, Rosario',
            'lat': -32.9605,
            'lng': -60.6295,
            'ciudad': 'Rosario'
        },
        {
            'nombre': 'La Gallega - 9 de Julio',
            'direccion': '9 de Julio 734, Rosario',
            'lat': -32.9650,
            'lng': -60.6380,
            'ciudad': 'Rosario'
        },
        {
            'nombre': 'La Gallega - Entre Ríos',
            'direccion': 'Entre Ríos 2361, Rosario',
            'lat': -32.9720,
            'lng': -60.6450,
            'ciudad': 'Rosario'
        },
        {
            'nombre': 'La Gallega - Mendoza',
            'direccion': 'Avenida Mendoza 255, Rosario',
            'lat': -32.9325,
            'lng': -60.6510,
            'ciudad': 'Rosario'
        },
        {
            'nombre': 'La Gallega - Alberdi',
            'direccion': 'Av. Alberdi 465 Bis, Rosario',
            'lat': -32.9288,
            'lng': -60.6710,
            'ciudad': 'Rosario'
        },
        {
            'nombre': 'La Gallega - Córdoba 7605',
            'direccion': 'Córdoba 7605, Rosario',
            'lat': -32.9880,
            'lng': -60.7020,
            'ciudad': 'Rosario'
        },
        {
            'nombre': 'La Gallega - Mendoza 7875',
            'direccion': 'Mendoza 7875, Rosario',
            'lat': -32.9920,
            'lng': -60.7050,
            'ciudad': 'Rosario'
        }
    ]
}

def obtener_sucursales(supermercado_nombre):
    """
    Obtiene la lista de sucursales para un supermercado específico
    """
    return SUCURSALES.get(supermercado_nombre, [])

def calcular_distancia_haversine(lat1, lng1, lat2, lng2):
    """
    Calcula la distancia entre dos coordenadas GPS usando la fórmula de Haversine
    Retorna la distancia en kilómetros
    """
    from math import radians, sin, cos, sqrt, atan2
    
    # Radio de la Tierra en kilómetros
    R = 6371.0
    
    # Convertir grados a radianes
    lat1_rad = radians(lat1)
    lng1_rad = radians(lng1)
    lat2_rad = radians(lat2)
    lng2_rad = radians(lng2)
    
    # Diferencias
    dlat = lat2_rad - lat1_rad
    dlng = lng2_rad - lng1_rad
    
    # Fórmula de Haversine
    a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlng / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    distancia = R * c
    return distancia

def encontrar_sucursal_mas_cercana(supermercado_nombre, lat_usuario, lng_usuario):
    """
    Encuentra la sucursal más cercana a la ubicación del usuario
    Para búsquedas simples, retorna búsqueda de Google Maps
    
    Args:
        supermercado_nombre: Nombre del supermercado
        lat_usuario: Latitud del usuario
        lng_usuario: Longitud del usuario
        
    Returns:
        Dict con información de la sucursal más cercana y distancia
    """
    sucursales = obtener_sucursales(supermercado_nombre)
    
    if not sucursales:
        return None
    
    sucursal_cercana = None
    distancia_minima = float('inf')
    
    for sucursal in sucursales:
        distancia = calcular_distancia_haversine(
            lat_usuario, lng_usuario,
            sucursal['lat'], sucursal['lng']
        )
        
        if distancia < distancia_minima:
            distancia_minima = distancia
            sucursal_cercana = sucursal.copy()
            sucursal_cercana['distancia_km'] = round(distancia, 2)
    
    # Si tiene búsqueda de maps personalizada, crear URL de búsqueda
    if 'busqueda_maps' in sucursal_cercana:
        busqueda = sucursal_cercana['busqueda_maps']
        sucursal_cercana['google_maps_url'] = f"https://www.google.com/maps/search/?api=1&query={busqueda.replace(' ', '+')}"
    
    return sucursal_cercana

def obtener_supermercados_cercanos(lat_usuario, lng_usuario, radio_km=10):
    """
    Obtiene lista de supermercados que tienen sucursales dentro del radio especificado
    
    Args:
        lat_usuario: Latitud del usuario
        lng_usuario: Longitud del usuario
        radio_km: Radio de búsqueda en kilómetros (default: 10km)
        
    Returns:
        Lista de nombres de supermercados con sucursales cercanas
    """
    supermercados_cercanos = []
    
    for supermercado_nombre in SUCURSALES.keys():
        sucursales = obtener_sucursales(supermercado_nombre)
        
        # Verificar si alguna sucursal está dentro del radio
        for sucursal in sucursales:
            distancia = calcular_distancia_haversine(
                lat_usuario, lng_usuario,
                sucursal['lat'], sucursal['lng']
            )
            
            if distancia <= radio_km:
                supermercados_cercanos.append(supermercado_nombre)
                break  # Ya encontramos una sucursal cercana, no seguir buscando
    
    return supermercados_cercanos

def filtrar_sucursales_por_radio(lat_usuario, lng_usuario, radio_km=10):
    """
    Filtra todas las sucursales dentro del radio especificado
    
    Args:
        lat_usuario: Latitud del usuario
        lng_usuario: Longitud del usuario
        radio_km: Radio de búsqueda en kilómetros (default: 10km)
        
    Returns:
        Dict con supermercados como keys y lista de sucursales cercanas como values
    """
    resultado = {}
    
    for supermercado_nombre, sucursales in SUCURSALES.items():
        sucursales_cercanas = []
        
        for sucursal in sucursales:
            distancia = calcular_distancia_haversine(
                lat_usuario, lng_usuario,
                sucursal['lat'], sucursal['lng']
            )
            
            if distancia <= radio_km:
                sucursal_con_distancia = sucursal.copy()
                sucursal_con_distancia['distancia_km'] = round(distancia, 2)
                sucursales_cercanas.append(sucursal_con_distancia)
        
        if sucursales_cercanas:
            # Ordenar por distancia
            sucursales_cercanas.sort(key=lambda x: x['distancia_km'])
            resultado[supermercado_nombre] = sucursales_cercanas
    
    return resultado

def detectar_ciudad_usuario(lat_usuario, lng_usuario):
    """
    Detecta la ciudad más cercana al usuario basándose en coordenadas GPS
    
    Args:
        lat_usuario: Latitud del usuario
        lng_usuario: Longitud del usuario
        
    Returns:
        String con el nombre de la ciudad más cercana
    """
    # Coordenadas centrales de ciudades principales
    CIUDADES = {
        'Buenos Aires': {'lat': -34.6037, 'lng': -58.3816},
        'Córdoba': {'lat': -31.4201, 'lng': -64.1888},
        'Rosario': {'lat': -32.9442, 'lng': -60.6505},
        'Mendoza': {'lat': -32.8895, 'lng': -68.8458},
        'La Plata': {'lat': -34.9205, 'lng': -57.9536},
        'Mar del Plata': {'lat': -38.0055, 'lng': -57.5426},
        'Tucumán': {'lat': -26.8083, 'lng': -65.2176},
        'Salta': {'lat': -24.7859, 'lng': -65.4117}
    }
    
    ciudad_mas_cercana = None
    distancia_minima = float('inf')
    
    for ciudad, coords in CIUDADES.items():
        distancia = calcular_distancia_haversine(
            lat_usuario, lng_usuario,
            coords['lat'], coords['lng']
        )
        
        if distancia < distancia_minima:
            distancia_minima = distancia
            ciudad_mas_cercana = ciudad
    
    return {
        'ciudad': ciudad_mas_cercana,
        'distancia_km': round(distancia_minima, 2)
    }

def obtener_supermercados_por_ciudad(ciudad):
    """
    Obtiene lista de supermercados que tienen sucursales en una ciudad específica
    
    Args:
        ciudad: Nombre de la ciudad
        
    Returns:
        Lista de nombres de supermercados con presencia en esa ciudad
    """
    supermercados_en_ciudad = []
    
    for supermercado_nombre, sucursales in SUCURSALES.items():
        # Verificar si hay alguna sucursal en esta ciudad
        tiene_sucursal_en_ciudad = any(
            sucursal['ciudad'] == ciudad 
            for sucursal in sucursales
        )
        
        if tiene_sucursal_en_ciudad:
            supermercados_en_ciudad.append(supermercado_nombre)
    
    return supermercados_en_ciudad
