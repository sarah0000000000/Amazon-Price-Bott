import asyncio
import random
import logging
from scraper import AmazonScraper
from url_generator import generate_urls_from_all_categories
from database import Database
from alert import AlertSystem

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filename="bot.log",
)

async def main():
    """Fonction principale du bot."""
    alert_system = AlertSystem()
    await alert_system.send_alert("🤖 **Démarrage du bot Amazon Price Bot...**")

    while True:  # Boucle infinie pour exécuter le bot 24/7
        try:
            logging.info("Démarrage du bot...")
            
            # Initialisation des composants
            scraper = AmazonScraper()
            db = Database()

            # Génération des URLs pour toutes les catégories
            logging.info("Génération des URLs...")
            urls = generate_urls_from_all_categories()
            logging.info(f"{len(urls)} URLs générées.")

            # Scraping des données par lots (batch processing)
            batch_size = 50  # Nombre d'URLs à traiter par lot
            for i in range(0, len(urls), batch_size):
                batch_urls = urls[i:i + batch_size]
                logging.info(f"Traitement du lot {i//batch_size + 1} (URLs {i} à {i + batch_size})...")

                try:
                    # Scraping des données
                    results = await scraper.scrape_all(batch_urls)
                    logging.info(f"Résultats du scraping : {len(results)} produits trouvés.")

                    # Traitement des résultats
                    for product in results:
                        if product:
                            logging.info(f"Produit : {product['name']}, Prix : {product['price']}, URL : {product['url']}")
                            if is_price_valid(product["price"]):
                                asin = product["url"].split("/dp/")[1].split("/")[0]
                                existing_product = db.get_product(asin)

                                if existing_product:
                                    db.update_price(asin, product["price"])
                                    # Détection d'erreurs
                                    error = detect_price_errors({
                                        "price": product["price"],
                                        "initial_price": existing_product[4]  # initial_price dans la base de données
                                    })
                                    if error:
                                        logging.warning(f"⚠️ Erreur détectée pour {product['name']} : {error}")
                                        message = (
                                            f"⚠️ **Erreur détectée pour {product['name']}** : {error}\n"
                                            f"🔗 [URL du produit]({product['url']})\n"
                                            f"💶 Prix initial : {existing_product[4]} €\n"
                                            f"💶 Prix actuel : {product['price']} €"
                                        )
                                        await alert_system.send_alert(message)
                                else:
                                    db.insert_product(asin, product["name"], product["url"], product["price"])
                            else:
                                logging.warning(f"⚠️ Prix invalide pour {product['name']} : {product['price']}")
                except Exception as e:
                    logging.error(f"Erreur lors du traitement du lot {i//batch_size + 1} : {e}")
                    await alert_system.send_alert(f"⚠️ Erreur lors du traitement du lot {i//batch_size + 1} : {e}")

                # Délai aléatoire entre les lots
                delay = random.uniform(10, 30)  # Délai aléatoire entre 10 et 30 secondes
                await asyncio.sleep(delay)

            db.close()
            logging.info("Cycle terminé. Attente avant le prochain cycle...")
            await asyncio.sleep(300)  # Attendre 5 minutes avant de recommencer

        except Exception as e:
            logging.error(f"Erreur dans la boucle principale : {e}")
            await alert_system.send_alert(f"⚠️ Erreur dans la boucle principale : {e}")
            await asyncio.sleep(60)  # Attendre 1 minute avant de réessayer

def is_price_valid(price):
    """Vérifie si le prix est plausible."""
    if price is None:
        return False
    return 1 <= price <= 10000  # Exemple : prix entre 1€ et 10 000€

def detect_price_errors(product):
    """Détecte les erreurs de prix."""
    current_price = product["price"]
    initial_price = product["initial_price"]

    if current_price is None or initial_price is None:
        return "Prix manquant"

    # Erreur si le prix est à 0
    if current_price == 0:
        return "Prix à 0 détecté"

    # Erreur si le prix est trop bas (moins de 1 €)
    if current_price < 1:
        return f"Prix anormalement bas détecté : {current_price} €"

    # Erreur si le prix a baissé de plus de 80 %
    price_drop_ratio = (initial_price - current_price) / initial_price
    if price_drop_ratio > 0.8:
        return f"Réduction extrême détectée ({price_drop_ratio * 100:.2f}%)"

    # Erreur si le prix est trop haut (inflation soudaine)
    if current_price > initial_price * 1.5:
        return f"Inflation soudaine détectée ({current_price / initial_price * 100:.2f}%)"

    return None

if __name__ == "__main__":
    asyncio.run(main())