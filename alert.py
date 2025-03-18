from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler
import os
from dotenv import load_dotenv
import logging
import asyncio

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

class AlertSystem:
    def __init__(self):
        self.bot = Bot(token=TELEGRAM_TOKEN)

    async def send_alert(self, message):
        """Envoie une alerte Telegram."""
        try:
            await self.bot.send_message(
                chat_id=TELEGRAM_CHAT_ID,
                text=message,
                parse_mode="Markdown",  # Activation du Markdown
            )
            logging.info("Message Telegram envoyé avec succès.")
        except Exception as e:
            logging.error(f"Erreur lors de l'envoi de l'alerte Telegram : {e}")

# Commandes du bot Telegram
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "🤖 Bienvenue sur Amazon Price Bot !\n\n"
        "Commandes disponibles :\n"
        "/start - Affiche ce message\n"
        "/help - Affiche l'aide\n"
        "/add <URL> - Ajoute un produit à surveiller\n"
        "/list - Liste les produits surveillés\n"
        "/remove <ASIN> - Supprime un produit\n"
        "/stats - Affiche les statistiques\n"
        "/settings - Configure les notifications"
    )

def add_product(update: Update, context: CallbackContext):
    try:
        url = context.args[0]  # Récupère l'URL passée en argument
        # Ajoutez ici la logique pour ajouter le produit à la base de données
        update.message.reply_text(f"✅ Produit ajouté : {url}")
    except IndexError:
        update.message.reply_text("❌ Utilisation : /add <URL>")

def list_products(update: Update, context: CallbackContext):
    # Récupérez la liste des produits depuis la base de données
    products = ["Produit 1", "Produit 2", "Produit 3"]  # Exemple
    if products:
        update.message.reply_text("📋 Produits surveillés :\n" + "\n".join(products))
    else:
        update.message.reply_text("ℹ️ Aucun produit surveillé pour le moment.")

def remove_product(update: Update, context: CallbackContext):
    try:
        asin = context.args[0]  # Récupère l'ASIN passée en argument
        # Ajoutez ici la logique pour supprimer le produit de la base de données
        update.message.reply_text(f"✅ Produit supprimé : {asin}")
    except IndexError:
        update.message.reply_text("❌ Utilisation : /remove <ASIN>")

def stats(update: Update, context: CallbackContext):
    # Récupérez les statistiques depuis la base de données
    total_products = 10  # Exemple
    price_drops = 3  # Exemple
    update.message.reply_text(
        f"📊 Statistiques :\n"
        f"• Produits surveillés : {total_products}\n"
        f"• Baisses de prix détectées : {price_drops}"
    )

def settings(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Baisse de prix", callback_data="alert_price_drop")],
        [InlineKeyboardButton("Erreur de prix", callback_data="alert_price_error")],
        [InlineKeyboardButton("Produit en stock", callback_data="alert_stock")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("🔔 Choisissez les notifications :", reply_markup=reply_markup)

def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    query.edit_message_text(f"✅ Option sélectionnée : {query.data}")

# Configuration du bot
def main():
    updater = Updater(TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher

    # Ajoutez les gestionnaires de commandes
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("add", add_product))
    dispatcher.add_handler(CommandHandler("list", list_products))
    dispatcher.add_handler(CommandHandler("remove", remove_product))
    dispatcher.add_handler(CommandHandler("stats", stats))
    dispatcher.add_handler(CommandHandler("settings", settings))
    dispatcher.add_handler(CallbackQueryHandler(button_handler))

    # Démarrez le bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()