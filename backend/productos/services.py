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
        query_normalizada = self.normalizar_nombre(query)
        productos_relevantes = []
        
        for producto in productos:
            nombre_norm = producto.get('nombre_normalizado', '')
            
            # Calcular relevancia basada en coincidencias
            relevancia = 0
            
            # Coincidencia exacta en query
            if query_normalizada in nombre_norm:
                relevancia += 10
            
            # Coincidencias por palabras
            palabras_query = query_normalizada.split()
            for palabra in palabras_query:
                if palabra in nombre_norm:
                    relevancia += 5
            
            # Solo incluir productos con relevancia mínima
            if relevancia >= 5:
                producto_con_relevancia = producto.copy()
                producto_con_relevancia['relevancia'] = relevancia
                productos_relevantes.append(producto_con_relevancia)
        
        # Ordenar por relevancia y después por precio
        productos_relevantes.sort(key=lambda x: (-x['relevancia'], x['precio']))
        
        return productos_relevantes