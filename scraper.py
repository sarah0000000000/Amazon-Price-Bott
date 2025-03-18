import aiohttp
import asyncio
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import logging

class AmazonScraper:
    def __init__(self, max_retries=3):
        self.ua = UserAgent()
        self.max_retries = max_retries

    async def get_product_data(self, session, url):
        """Scrape les données produit avec gestion d'erreurs."""
        headers = {
            "User-Agent": self.ua.random,
            "Accept-Language": "fr-FR,fr;q=0.9",
        }
        for attempt in range(self.max_retries):
            try:
                async with session.get(url, headers=headers, timeout=15) as response:
                    if response.status == 200:
                        html = await response.text()
                        return self._parse_response(html, url)
                    else:
                        logging.warning(f"Statut {response.status} sur {url} (tentative {attempt+1}/{self.max_retries})")
            except Exception as e:
                logging.error(f"Erreur sur {url} : {e}")
        return None

    def _parse_response(self, html, url):
        """Extraction des données depuis le HTML."""
        soup = BeautifulSoup(html, 'html.parser')
        
        # Nom du produit
        name = soup.find("span", id="productTitle")
        if not name:
            name = soup.find("h1", class_="a-size-large a-spacing-none")
        if not name:
            name = soup.find("h1", class_="a-size-medium a-spacing-none")
        name = name.text.strip() if name else "Nom inconnu"
        
        # Prix
        price = None
        price_span = soup.find("span", class_="a-price-whole")
        if not price_span:
            price_span = soup.find("span", class_="a-offscreen")
        if not price_span:
            price_span = soup.find("span", class_="a-color-price")

        if price_span:
            price_text = price_span.text.strip().replace("€", "").replace(",", ".")
            if price_text.replace(".", "", 1).isdigit():  # Gère les nombres comme "123.45"
                price = float(price_text)
        
        # Vérification du prix
        if price is not None and price <= 0:  # Si le prix est 0 ou négatif, le considérer comme invalide
            price = None
        
        return {
            "name": name,
            "price": price,
            "url": url,
        }

    async def scrape_all(self, urls):
        """Lance le scraping asynchrone."""
        async with aiohttp.ClientSession() as session:
            tasks = [self.get_product_data(session, url) for url in urls]
            return await asyncio.gather(*tasks)