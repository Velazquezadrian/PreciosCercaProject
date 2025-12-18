#!/usr/bin/env python3
from backend.productos.scrapers.scraper_coto import ScraperCoto
import json

scraper = ScraperCoto()

# Hacer request manualmente para ver la respuesta completa
params = {
    '_Ntt': 'leche',
    '_Nrpp': 50,
    'format': 'json'
}

response = scraper.session.get(scraper.search_url, params=params, timeout=15)
print(f"Status: {response.status_code}")
print(f"URL: {response.url}")

data = response.json()

# Guardar para analizar
with open('coto_debug.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("\nKeys principales:")
print(list(data.keys()))

if 'contents' in data and len(data['contents']) > 0:
    print(f"\nTotal contents: {len(data['contents'])}")
    content = data['contents'][0]
    print(f"\nContent[0] keys: {list(content.keys())}")
    
    if 'MainContent' in content:
        main_content_list = content['MainContent']
        print(f"\nMainContent items: {len(main_content_list)}")
        
        for idx, mc in enumerate(main_content_list):
            print(f"\n--- MainContent[{idx}] ---")
            print(f"Keys: {list(mc.keys())[:10]}")
            print(f"@type: {mc.get('@type')}")
            
            if 'records' in mc:
                records = mc['records']
                print(f"✅ RECORDS ENCONTRADOS: {len(records) if records else 0}")
                
                if records and len(records) > 0:
                    print("\nPRIMER RECORD:")
                    print(json.dumps(records[0], indent=2, ensure_ascii=False)[:1500])
