#!/usr/bin/env python3
"""
Precarga MASIVA con 500+ términos de búsqueda
Para evitar límites de paginación de las APIs
"""

import sys
import os
from datetime import datetime
from time import sleep

sys.path.insert(0, os.path.dirname(__file__))
from productos.scrapers.scraper_carrefour import ScraperCarrefour
from productos.scrapers.scraper_dia import ScraperDia
from productos.scrapers.scraper_lareina import ScraperLaReina
from productos.scrapers.scraper_lagallega import ScraperLaGallega
from productos.scrapers.scraper_coto import ScraperCoto
from cache_manager import cache_manager

# 500+ términos de búsqueda más populares en supermercados
TERMINOS_BUSQUEDA = [
    # Lácteos (50 términos)
    'leche', 'yogur', 'queso', 'manteca', 'crema', 'dulce de leche',
    'leche descremada', 'leche entera', 'leche chocolatada', 'leche en polvo',
    'yogur entero', 'yogur descremado', 'yogur bebible', 'yogur griego',
    'queso cremoso', 'queso rallado', 'queso roquefort', 'queso parmesano',
    'queso mozzarella', 'queso sardo', 'queso port salut', 'queso barra',
    'ricota', 'casancrem', 'mascarpone', 'crema chantilly',
    
    # Panificados (30 términos)
    'pan', 'pan lactal', 'pan rallado', 'pan integral', 'pan negro',
    'galletitas', 'galletas', 'bizcochos', 'medialunas', 'facturas',
    'tostadas', 'panchos', 'hamburguesas pan', 'pan arabe', 'pan pita',
    'pan viena', 'baguette', 'pan frances', 'pan salvado', 'pan centeno',
    
    # Bebidas (60 términos)
    'agua', 'gaseosa', 'jugo', 'cerveza', 'vino', 'coca cola',
    'sprite', 'fanta', 'pepsi', 'seven up', 'agua con gas', 'agua sin gas',
    'jugo naranja', 'jugo manzana', 'jugo multifruta', 'jugo pomelo',
    'cerveza quilmes', 'cerveza brahma', 'cerveza stella artois',
    'vino tinto', 'vino blanco', 'vino malbec', 'champagne', 'fernet',
    'whisky', 'vodka', 'gin', 'ron', 'aperitivos', 'amargo',
    'cafe', 'te', 'mate cocido', 'yerba mate', 'yerba', 'te verde',
    'te negro', 'te rojo', 'cafe instantaneo', 'cafe molido', 'cafe grano',
    'energizante', 'speed', 'monster', 'red bull', 'gatorade', 'powerade',
    
    # Almacén (80 términos)
    'arroz', 'fideos', 'harina', 'azucar', 'sal', 'aceite',
    'aceite girasol', 'aceite oliva', 'aceite mezcla', 'vinagre',
    'fideos secos', 'fideos frescos', 'ravioles', 'sorrentinos', 'ñoquis',
    'arroz integral', 'arroz yamaní', 'arroz largo fino', 'arroz parboil',
    'harina 0000', 'harina leudante', 'harina integral', 'harina maiz',
    'azucar blanco', 'azucar negro', 'edulcorante', 'polvo hornear',
    'levadura', 'bicarbonato', 'esencia vainilla', 'cacao', 'chocolate',
    'mermelada', 'miel', 'dulce batata', 'dulce membrillo',
    'latas atun', 'latas caballa', 'latas choclo', 'latas arvejas',
    'puré tomate', 'salsa tomate', 'mayonesa', 'mostaza', 'ketchup',
    'pickles', 'aceitunas', 'salsa golf', 'aderezos', 'condimentos',
    'oregano', 'pimienta', 'comino', 'aji molido', 'paprika', 'pimenton',
    'caldo', 'caldo knorr', 'sopa', 'gelatina', 'flan', 'postre',
    'cereales', 'avena', 'granola', 'barras cereal',
    
    # Carnes y fiambres (40 términos)
    'carne', 'pollo', 'cerdo', 'pescado', 'milanesa', 'hamburguesa',
    'salchicha', 'chorizo', 'morcilla', 'fiambre', 'jamon', 'salame',
    'jamon cocido', 'jamon crudo', 'paleta', 'mortadela', 'salamin',
    'bondiola', 'panceta', 'leberwurst', 'pate', 'queso y dulce',
    'carne picada', 'nalga', 'cuadril', 'lomo', 'asado', 'costilla',
    'pollo entero', 'pechuga', 'pata muslo', 'alitas pollo',
    'salmon', 'merluza', 'pejerrey', 'atun', 'caballa',
    
    # Frutas y verduras (50 términos)
    'papa', 'tomate', 'cebolla', 'lechuga', 'zanahoria', 'zapallo',
    'batata', 'choclo', 'brocoli', 'coliflor', 'repollo', 'espinaca',
    'acelga', 'rucula', 'apio', 'pimiento', 'morron', 'berenjena',
    'zapallito', 'calabaza', 'arvejas', 'chauchas', 'poroto', 'lenteja',
    'manzana', 'banana', 'naranja', 'mandarina', 'pera', 'durazno',
    'ciruela', 'kiwi', 'frutilla', 'uva', 'melon', 'sandia', 'anana',
    'limon', 'pomelo', 'palta', 'nuez', 'almendra', 'mani', 'pasas',
    
    # Limpieza (60 términos)
    'detergente', 'lavandina', 'jabon', 'suavizante', 'limpiador',
    'papel higienico', 'servilletas', 'pañuelos', 'rollo cocina',
    'esponja', 'trapo piso', 'escoba', 'balde', 'bolsas residuo',
    'limpia vidrios', 'cif', 'mr musculo', 'ayudin', 'odex', 'lysoform',
    'skip', 'ariel', 'omo', 'magistral', 'vivere', 'cif cremoso',
    'desengrasante', 'desinfectante', 'alcohol', 'alcohol gel',
    'jabon liquido', 'jabon tocador', 'jabon ropa', 'jabon polvo',
    'suavizante concentrado', 'comfort', 'vivere', 'suavizante dilutable',
    'lavandina con detergente', 'cloro', 'soda caustica',
    'limpia pisos', 'cera', 'lustramuebles', 'ajax', 'magistral pisos',
    'bolsas basura', 'bolsas consorcio', 'guantes', 'repasador',
    
    # Perfumería y higiene (50 términos)
    'shampoo', 'acondicionador', 'jabon', 'desodorante', 'crema dental',
    'cepillo dientes', 'hilo dental', 'enjuague bucal', 'crema manos',
    'crema corporal', 'crema facial', 'protector solar', 'after sun',
    'shampoo sedal', 'shampoo pantene', 'shampoo head shoulders',
    'acondicionador sedal', 'rexona', 'dove', 'nivea', 'johnson',
    'colgate', 'pepsodent', 'odontol', 'listerine', 'gillette', 'prestobarba',
    'pañales', 'toallitas humedas', 'talco', 'cotonetes', 'algodon',
    'preservativos', 'prime', 'tulipan', 'lady soft', 'toallitas femeninas',
    'tampones', 'protectores diarios', 'papel tissue', 'kleenex',
    'rastrillos', 'hojas afeitar', 'espuma afeitar', 'after shave',
    
    # Congelados (30 términos)
    'helado', 'hielo', 'verduras congeladas', 'papas fritas congeladas',
    'hamburguesas congeladas', 'milanesas congeladas', 'medallones',
    'pescado congelado', 'tarta congelada', 'empanadas congeladas',
    'pizza congelada', 'masa congelada', 'prepizza', 'tapas tarta',
    'tapas empanadas', 'hojaldre', 'tarta verdura', 'tarta jamon queso',
    'helado pote', 'helado palito', 'helado cucurucho', 'frigor',
    
    # Bebé (20 términos)
    'leche materna', 'formula infantil', 'pañales bebe', 'toallitas bebe',
    'mamaderas', 'chupetes', 'tetinas', 'baberos', 'papillas', 'cereales bebe',
    'compotas', 'juguitos', 'shampoo bebe', 'jabon bebe', 'talco bebe',
    'crema pañal', 'aceite bebe', 'algodon bebe', 'cotonetes bebe',
    
    # Mascotas (20 términos)
    'alimento perro', 'alimento gato', 'piedras sanitarias', 'arena gato',
    'hueso perro', 'snack perro', 'collar', 'correa', 'juguete perro',
    'cama perro', 'cuchas', 'comedero', 'bebedero', 'antipulgas',
    'shampoo perro', 'royal canin', 'pedigree', 'whiskas', 'excellent',
    
    # Bazar y otros (30 términos)
    'velas', 'fosforos', 'encendedor', 'pilas', 'lamparita', 'extension',
    'platos descartables', 'vasos descartables', 'cubiertos descartables',
    'bandeja telgopor', 'film', 'papel aluminio', 'papel manteca',
    'sorbetes', 'palillos', 'escarbadientes', 'broches ropa', 'pinzas',
    'perchas', 'candado', 'llave', 'destornillador', 'martillo', 'cinta',
    'pegamento', 'fibron', 'lapiceras', 'cuadernos', 'hojas',
]

def main():
    print("")
    print("╔" + "="*78 + "╗")
    print("║" + " PRECARGA MASIVA CON 500+ TÉRMINOS ".center(78) + "║")
    print("╚" + "="*78 + "╝")
    print("")
    print(f"🕐 Inicio: {datetime.now().strftime('%H:%M:%S')}")
    print(f"📊 Términos de búsqueda: {len(TERMINOS_BUSQUEDA)}")
    print(f"🏪 Supermercados: Carrefour + Día % + La Reina + La Gallega + Coto")
    print(f"⏱️  Duración estimada: 50-70 minutos")
    print("")
    
    # Inicializar scrapers
    scrapers = {
        'Carrefour': ScraperCarrefour(),
        'Día %': ScraperDia(),
        'La Reina': ScraperLaReina(),
        'La Gallega': ScraperLaGallega(),
        'Coto': ScraperCoto()
    }
    
    total_agregados = {'Carrefour': 0, 'Día %': 0, 'La Reina': 0, 'La Gallega': 0, 'Coto': 0}
    
    try:
        for idx, termino in enumerate(TERMINOS_BUSQUEDA, 1):
            print(f"\n[{idx:3d}/{len(TERMINOS_BUSQUEDA)}] 🔍 '{termino}'")
            
            for nombre, scraper in scrapers.items():
                try:
                    # Forzar precarga = False para evitar autoprecarga
                    scraper._precargando = True
                    
                    # Buscar productos
                    productos = scraper.buscar_productos(termino)
                    
                    if productos:
                        print(f"  {nombre}: ✅ {len(productos)} productos")
                        total_agregados[nombre] += len(productos)
                    else:
                        print(f"  {nombre}: ⚠️ sin resultados")
                    
                    scraper._precargando = False
                    
                except Exception as e:
                    print(f"  {nombre}: ❌ {e}")
                    continue
            
            # Guardar cada 10 búsquedas
            if idx % 10 == 0:
                cache_manager.guardar_cache()
                print(f"\n   💾 Caché guardado - Totales acumulados:")
                for super_key, nombre in [('carrefour', 'Carrefour'), ('dia', 'Día %'), 
                                          ('lareina', 'La Reina'), ('lagallega', 'La Gallega'),
                                          ('coto', 'Coto')]:
                    total = len(cache_manager.cache['productos'].get(super_key, {}))
                    print(f"      {nombre}: {total:,} productos")
            
            # Pausa
            sleep(0.1)
    
    except KeyboardInterrupt:
        print("\n\n⚠️ Precarga interrumpida (Ctrl+C)")
    
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        cache_manager.guardar_cache()
        
        print("")
        print("╔" + "="*78 + "╗")
        print("║" + " RESUMEN FINAL ".center(78) + "║")
        print("╚" + "="*78 + "╝")
        print("")
        
        for super_key, nombre in [('carrefour', 'Carrefour'), ('dia', 'Día %'), 
                                  ('lareina', 'La Reina'), ('lagallega', 'La Gallega'),
                                  ('coto', 'Coto')]:
            total = len(cache_manager.cache['productos'].get(super_key, {}))
            print(f"✅ {nombre}: {total:,} productos")
        
        total_general = sum(len(cache_manager.cache['productos'].get(k, {})) 
                           for k in ['carrefour', 'dia', 'lareina', 'lagallega', 'coto'])
        print(f"\n🎯 TOTAL GENERAL: {total_general:,} productos")
        print(f"\n🕐 Fin: {datetime.now().strftime('%H:%M:%S')}")
        print("")

if __name__ == '__main__':
    main()
