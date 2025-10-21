# Clase base abstracta para todos los scrapers de supermercados
from abc import ABC, abstractmethod
from typing import List, Dict
import requests
from bs4 import BeautifulSoup

class BaseScraper(ABC):
    def __init__(self, base_url: str, supermercado_nombre: str):
        # Configuración básica del scraper
        self.base_url = base_url
        self.supermercado_nombre = supermercado_nombre
        self.session = requests.Session()  # Mantener cookies/sesión

    @abstractmethod
    def buscar_productos(self, query: str) -> List[Dict]:
        # Método que debe implementar cada scraper específico
        pass

    def hacer_request(self, url: str) -> BeautifulSoup:
        # Realizar petición HTTP y parsear HTML
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()  # Lanzar excepción si status != 200
            return BeautifulSoup(response.content, 'html.parser')  # Usar parser por defecto
        except Exception as e:
            print(f"Error al hacer request a {url}: {e}")
            return None