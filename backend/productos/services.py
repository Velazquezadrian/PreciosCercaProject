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
        # Filtrar productos que coincidan mejor con la búsqueda
        query_lower = query.lower().strip()
        palabras_query = query_lower.split()
        productos_relevantes = []
        
        print(f"[Filtro] Query: '{query}' | Palabras a buscar: {palabras_query}")
        print(f"[Filtro] Total productos a filtrar: {len(productos)}")
        
        for producto in productos:
            nombre_original = producto['nombre'].lower()
            
            # Calcular relevancia basada en coincidencias
            relevancia = 0
            palabras_encontradas = 0
            
            # Verificar si TODAS las palabras de la query están en el producto
            for palabra in palabras_query:
                if palabra in nombre_original:
                    palabras_encontradas += 1
                    relevancia += 5
            
            # Bonus si la frase completa está en el nombre
            if query_lower in nombre_original:
                relevancia += 15
            
            # Solo incluir productos que tengan TODAS las palabras de la búsqueda
            if palabras_encontradas == len(palabras_query):
                producto_con_relevancia = producto.copy()
                producto_con_relevancia['relevancia'] = relevancia
                producto_con_relevancia['nombre_normalizado'] = nombre_original
                productos_relevantes.append(producto_con_relevancia)
        
        print(f"[Filtro] Productos después del filtro: {len(productos_relevantes)}")
        
        # Ordenar por relevancia y después por precio
        productos_relevantes.sort(key=lambda x: (-x['relevancia'], x['precio']))
        
        return productos_relevantes


# Función standalone para usar desde simple_server.py
def buscar_productos_similares(query: str, productos: List[Dict]) -> List[Dict]:
    """
    Filtra productos para que solo incluya aquellos que contienen TODAS las palabras de la búsqueda.
    
    Args:
        query: Término de búsqueda (puede ser múltiples palabras)
        productos: Lista de productos a filtrar
    
    Returns:
        Lista filtrada de productos que contienen todas las palabras
    """
    query_lower = query.lower().strip()
    palabras_query = query_lower.split()
    productos_relevantes = []
    
    print(f"[Filtro] Query: '{query}' | Palabras a buscar: {palabras_query}")
    print(f"[Filtro] Total productos a filtrar: {len(productos)}")
    
    for producto in productos:
        nombre_original = producto['nombre'].lower()
        
        # Calcular relevancia basada en coincidencias
        relevancia = 0
        palabras_encontradas = 0
        
        # Verificar si TODAS las palabras de la query están en el producto
        for palabra in palabras_query:
            if palabra in nombre_original:
                palabras_encontradas += 1
                relevancia += 5
        
        # Bonus si la frase completa está en el nombre
        if query_lower in nombre_original:
            relevancia += 15
        
        # Solo incluir productos que tengan TODAS las palabras de la búsqueda
        if palabras_encontradas == len(palabras_query):
            producto_con_relevancia = producto.copy()
            producto_con_relevancia['relevancia'] = relevancia
            productos_relevantes.append(producto_con_relevancia)
    
    print(f"[Filtro] Productos después del filtro: {len(productos_relevantes)}")
    
    # Ordenar por relevancia y después por precio
    productos_relevantes.sort(key=lambda x: (-x['relevancia'], x['precio']))
    
    return productos_relevantes