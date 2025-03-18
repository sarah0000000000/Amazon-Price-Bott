import requests
from bs4 import BeautifulSoup
import logging

def get_all_categories():
    """Retourne une liste de toutes les catégories Amazon."""
    base_url = "https://www.amazon.fr"
    categories = []

    # Catégories spécifiques
    specific_categories = [
        "/gp/bestsellers/electronics",  # Multimédia
        "/gp/bestsellers/computers",    # Informatique
        "/gp/bestsellers/videogames",   # Jeux vidéo
        "/gp/bestsellers/console-gaming",  # Consoles de jeu
        "/gp/bestsellers/tv-hifi",      # TV/Hifi
        "/gp/bestsellers/pc",           # PC
        "/gp/bestsellers/pc-gaming",    # PC Gamer
        "/gp/bestsellers/laptops",      # PC Portable
        "/gp/bestsellers/phones",       # Téléphones
        "/s?k=iphone",                  # iPhone
        "/s?k=samsung",                 # Samsung
    ]

    for category in specific_categories:
        categories.append(f"{base_url}{category}")

    # Supprimer les doublons
    categories = list(set(categories))
    logging.info(f"{len(categories)} catégories trouvées.")
    return categories

def scrape_category_asins(category_url):
    """Scrape les ASINs d'une catégorie Amazon."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(category_url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        asins = []
        for div in soup.find_all("div", {"data-asin": True}):
            asin = div.get("data-asin")
            if asin and asin.strip() != "":  # Évite les ASINs vides
                asins.append(asin)
        
        logging.info(f"{len(asins)} ASINs trouvés dans {category_url}.")
        return asins
    except Exception as e:
        logging.error(f"Erreur lors du scraping de la catégorie {category_url} : {e}")
        return []

def generate_urls_from_all_categories():
    """Génère des URLs pour toutes les catégories Amazon."""
    categories = get_all_categories()
    all_asins = []
    for category_url in categories:
        logging.info(f"Scraping de la catégorie : {category_url}")
        asins = scrape_category_asins(category_url)
        all_asins.extend(asins)
    
    base_url = "https://www.amazon.fr/dp/"
    return [base_url + asin for asin in all_asins]