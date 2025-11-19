# Servicio para normalizar y consolidar resultados de múltiples scrapers
from typing import List, Dict
import re

class NormalizadorProductos:
    def __init__(self):
        # Palabras comunes para normalizar nombres
        self.palabras_comunes = {
            'leche': ['leche', 'milk'],
            'arroz': ['arroz', 'rice'],
            'cafe': ['cafe', 'café', 'coffee'],
            'agua': ['agua', 'water'],
            'te': ['te', 'té', 'tea'],
            'pan': ['pan', 'bread'],
            'aceite': ['aceite', 'oil'],
            'azucar': ['azucar', 'azúcar', 'sugar']
        }
    
    def normalizar_nombre(self, nombre: str) -> str:
        # Limpiar el nombre del producto
        nombre_limpio = nombre.lower().strip()
        
        # Remover texto extra común
        nombre_limpio = re.sub(r'\b(x\d+|pack|paquete|unidades?|kg|gr?|ml|lt?)\b', '', nombre_limpio)
        nombre_limpio = re.sub(r'\d+\s*(kg|gr?|ml|lt?|un|unidades?)', '', nombre_limpio)
        nombre_limpio = re.sub(r'\s+', ' ', nombre_limpio).strip()
        
        return nombre_limpio
    
    def consolidar_productos(self, productos_por_supermercado: List[List[Dict]]) -> List[Dict]:
        # Consolidar productos de múltiples supermercados
        todos_productos = []
        
        for productos_super in productos_por_supermercado:
            for producto in productos_super:
                # Normalizar nombre para mejor comparación
                producto_normalizado = producto.copy()
                producto_normalizado['nombre_normalizado'] = self.normalizar_nombre(producto['nombre'])
                todos_productos.append(producto_normalizado)
        
        # Ordenar por precio (más barato primero)
        todos_productos.sort(key=lambda x: x['precio'])
        
        return todos_productos
    
    def buscar_productos_similares(self, productos: List[Dict], query: str) -> List[Dict]:
        """
        Filtrar y ordenar productos según búsqueda del usuario.
        Prioriza productos con más coincidencias, luego ordena alfabéticamente.
        """
        query_lower = query.lower().strip()
        palabras_query = query_lower.split()
        productos_con_coincidencia = []
        
        print(f"[Filtro] Query: '{query}' | Palabras a buscar: {palabras_query}")
        print(f"[Filtro] Total productos a filtrar: {len(productos)}")
        
        for producto in productos:
            nombre_original = producto['nombre'].lower()
            
            # Contar palabras encontradas
            palabras_encontradas = sum(1 for palabra in palabras_query if palabra in nombre_original)
            
            # Solo incluir si tiene al menos una palabra
            if palabras_encontradas > 0:
                producto_con_meta = producto.copy()
                producto_con_meta['coincidencias'] = palabras_encontradas
                producto_con_meta['nombre_normalizado'] = nombre_original
                productos_con_coincidencia.append(producto_con_meta)
        
        print(f"[Filtro] Productos con coincidencias: {len(productos_con_coincidencia)}")
        
        # Ordenar: primero por coincidencias (más=mejor), luego alfabéticamente
        productos_con_coincidencia.sort(
            key=lambda x: (-x['coincidencias'], x['nombre'].lower())
        )
        
        return productos_con_coincidencia


# Función standalone para usar desde simple_server.py
def buscar_productos_similares(query: str, productos: List[Dict]) -> List[Dict]:
    """
    Filtra y ordena productos según coincidencia con búsqueda del usuario.
    
    LÓGICA DE PRIORIZACIÓN:
    1. Productos con TODAS las palabras buscadas → orden alfabético
    2. Productos con ALGUNAS palabras → orden alfabético (pero después del grupo 1)
    
    Ejemplo: "pan rayado"
    - 1º: "Pan rayado Carrefour" (tiene "pan" + "rayado")
    - 2º: "Pan rallado Don Satur" (tiene "pan" + "rayado/rallado")
    - 3º: "Pan francés" (solo tiene "pan")
    - 4º: "Pan lactal" (solo tiene "pan")
    
    Args:
        query: Término de búsqueda del usuario
        productos: Lista de productos a filtrar
    
    Returns:
        Lista filtrada y ordenada: primero por coincidencia completa, luego alfabético
    """
    query_lower = query.lower().strip()
    palabras_query = query_lower.split()
    productos_con_coincidencia = []
    
    print(f"[Filtro] Query: '{query}' | Palabras a buscar: {palabras_query}")
    print(f"[Filtro] Total productos a filtrar: {len(productos)}")
    
    for producto in productos:
        nombre_original = producto['nombre'].lower()
        
        # Contar cuántas palabras de la búsqueda están en el producto
        palabras_encontradas = 0
        for palabra in palabras_query:
            if palabra in nombre_original:
                palabras_encontradas += 1
        
        # Solo incluir si tiene AL MENOS UNA palabra de la búsqueda
        if palabras_encontradas > 0:
            producto_con_meta = producto.copy()
            # Guardar cuántas palabras coinciden (para ordenar después)
            producto_con_meta['coincidencias'] = palabras_encontradas
            producto_con_meta['tiene_todas'] = (palabras_encontradas == len(palabras_query))
            productos_con_coincidencia.append(producto_con_meta)
    
    print(f"[Filtro] Productos con coincidencias: {len(productos_con_coincidencia)}")
    
    # ORDENAR:
    # 1º por número de coincidencias (más coincidencias = más arriba)
    # 2º alfabéticamente por nombre
    productos_con_coincidencia.sort(
        key=lambda x: (-x['coincidencias'], x['nombre'].lower())
    )
    
    if productos_con_coincidencia:
        print(f"[Filtro] Top 5 productos más relevantes:")
        for i, p in enumerate(productos_con_coincidencia[:5], 1):
            match_info = f"({p['coincidencias']}/{len(palabras_query)} palabras)"
            print(f"  {i}. {p['nombre'][:50]} {match_info}")
    
    return productos_con_coincidencia