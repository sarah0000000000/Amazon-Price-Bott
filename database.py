import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name="prices.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        """Crée la table des produits si elle n'existe pas."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                asin TEXT UNIQUE,
                name TEXT,
                url TEXT,
                initial_price REAL,
                current_price REAL,
                last_checked TEXT
            )
        """)
        self.conn.commit()

    def insert_product(self, asin, name, url, initial_price):
        """Ajoute un nouveau produit à la base de données."""
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute("""
            INSERT INTO products (asin, name, url, initial_price, current_price, last_checked)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (asin, name, url, initial_price, initial_price, date))
        self.conn.commit()

    def update_price(self, asin, current_price):
        """Met à jour le prix d'un produit."""
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute("""
            UPDATE products
            SET current_price = ?, last_checked = ?
            WHERE asin = ?
        """, (current_price, date, asin))
        self.conn.commit()

    def get_product(self, asin):
        """Récupère un produit par son ASIN."""
        self.cursor.execute("SELECT * FROM products WHERE asin = ?", (asin,))
        return self.cursor.fetchone()

    def close(self):
        """Ferme la connexion à la base de données."""
        self.conn.close()