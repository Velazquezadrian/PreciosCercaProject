#!/usr/bin/env python3
from backend.productos.scrapers.scraper_coto import ScraperCoto
import json

scraper = ScraperCoto()

params = {
    '_Ntt': 'leche',
    '_Nrpp': 50,
    'format': 'json'
}

response = scraper.session.get(scraper.search_url, params=params, timeout=15)
data = response.json()

# Navegar estructura más profundo
main_content_slot = data['contents'][0]['MainContent'][1]  # ContentSlot-Main

print(f"ContentSlot-Main keys: {list(main_content_slot.keys())}")
print(f"\nTotal contents within ContentSlot: {len(main_content_slot.get('contents', []))}")

for idx, content_item in enumerate(main_content_slot.get('contents', [])):
    print(f"\n--- Content item [{idx}] ---")
    print(f"Keys: {list(content_item.keys())[:15]}")
    print(f"@type: {content_item.get('@type')}")
    print(f"name: {content_item.get('name')}")
    
    if 'records' in content_item:
        records = content_item['records']
        print(f"✅ RECORDS: {len(records) if records else 0}")
        
        if records and len(records) > 0:
            print("\nPRIMER RECORD (truncado):")
            record_str = json.dumps(records[0], indent=2, ensure_ascii=False)
            print(record_str[:2000])
            break
