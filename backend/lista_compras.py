"""
Módulo para gestionar la lista de compras del usuario
"""
from typing import List, Dict, Any
from datetime import datetime

class ItemListaCompras:
    """Representa un item en la lista de compras"""
    def __init__(self, nombre: str, cantidad: int = 1, precio: float = 0.0, 
                 supermercado: str = "", imagen: str = ""):
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio
        self.supermercado = supermercado
        self.imagen = imagen
        self.agregado_en = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'nombre': self.nombre,
            'cantidad': self.cantidad,
            'precio': self.precio,
            'supermercado': self.supermercado,
            'imagen': self.imagen,
            'agregado_en': self.agregado_en
        }


class ListaCompras:
    """Gestiona la lista de compras del usuario (en memoria por ahora)"""
    
    def __init__(self):
        self.items: List[ItemListaCompras] = []
    
    def agregar_producto(self, nombre: str, cantidad: int = 1, precio: float = 0.0,
                        supermercado: str = "", imagen: str = "") -> Dict[str, Any]:
        """Agrega un producto a la lista o incrementa su cantidad si ya existe"""
        # Buscar si el producto ya está en la lista
        for item in self.items:
            if item.nombre.lower() == nombre.lower():
                item.cantidad += cantidad
                return {
                    'status': 'actualizado',
                    'producto': nombre,
                    'cantidad': item.cantidad
                }
        
        # Si no existe, agregarlo
        nuevo_item = ItemListaCompras(nombre, cantidad, precio, supermercado, imagen)
        self.items.append(nuevo_item)
        return {
            'status': 'agregado',
            'producto': nombre,
            'cantidad': cantidad
        }
    
    def eliminar_producto(self, nombre: str) -> Dict[str, Any]:
        """Elimina un producto de la lista"""
        for i, item in enumerate(self.items):
            if item.nombre.lower() == nombre.lower():
                self.items.pop(i)
                return {
                    'status': 'eliminado',
                    'producto': nombre
                }
        
        return {
            'status': 'error',
            'mensaje': 'Producto no encontrado en la lista'
        }
    
    def obtener_items(self) -> List[Dict[str, Any]]:
        """Devuelve todos los items de la lista ordenados alfabéticamente"""
        # Ordenar items alfabéticamente por nombre
        items_ordenados = sorted(self.items, key=lambda x: x.nombre.lower())
        return [item.to_dict() for item in items_ordenados]
    
    def limpiar(self):
        """Limpia toda la lista de compras"""
        self.items.clear()
    
    def cantidad_items(self) -> int:
        """Retorna la cantidad total de items en la lista"""
        return len(self.items)


# Instancia global de la lista de compras (en producción esto debería ser por usuario)
lista_compras_global = ListaCompras()


def comparar_precios_lista(lista_items: List[str], productos_disponibles: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Compara precios de una lista de productos entre diferentes supermercados
    
    Args:
        lista_items: Lista de nombres de productos buscados
        productos_disponibles: Lista de productos obtenidos de scrapers
    
    Returns:
        Dict con comparación de totales por supermercado
    """
    # Agrupar productos por supermercado
    supermercados: Dict[str, Dict[str, Any]] = {}
    
    # Para cada producto en la lista
    for item_nombre in lista_items:
        # Buscar el producto más barato en cada supermercado
        productos_item = [
            p for p in productos_disponibles 
            if item_nombre.lower() in p.get('nombre', '').lower()
        ]
        
        if not productos_item:
            continue
        
        # Agrupar por supermercado y tomar el más barato de cada uno
        for producto in productos_item:
            super_nombre = producto.get('supermercado', 'Desconocido')
            
            if super_nombre not in supermercados:
                supermercados[super_nombre] = {
                    'nombre': super_nombre,
                    'productos': [],
                    'total': 0.0,
                    'productos_encontrados': 0
                }
            
            # Verificar si ya tenemos este producto para este supermercado
            producto_existente = next(
                (p for p in supermercados[super_nombre]['productos'] 
                 if p['nombre_buscado'] == item_nombre),
                None
            )
            
            if not producto_existente:
                supermercados[super_nombre]['productos'].append({
                    'nombre_buscado': item_nombre,
                    'nombre_encontrado': producto.get('nombre'),
                    'precio': producto.get('precio', 0.0)
                })
                supermercados[super_nombre]['total'] += producto.get('precio', 0.0)
                supermercados[super_nombre]['productos_encontrados'] += 1
            else:
                # Si ya existe, quedarse con el más barato
                if producto.get('precio', 0.0) < producto_existente['precio']:
                    supermercados[super_nombre]['total'] -= producto_existente['precio']
                    supermercados[super_nombre]['total'] += producto.get('precio', 0.0)
                    producto_existente['nombre_encontrado'] = producto.get('nombre')
                    producto_existente['precio'] = producto.get('precio', 0.0)
    
    # Ordenar supermercados por total (más barato primero)
    supermercados_ordenados = sorted(
        supermercados.values(),
        key=lambda x: x['total']
    )
    
    return {
        'total_productos_buscados': len(lista_items),
        'supermercados': supermercados_ordenados,
        'mas_barato': supermercados_ordenados[0] if supermercados_ordenados else None
    }
