import sqlite3
from datetime import datetime

DB_NAME = "otopark.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        # Kullanıcılar Tablosu
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            plaka TEXT UNIQUE, ad_soyad TEXT, telefon TEXT, email TEXT,
            durum TEXT DEFAULT 'BEKLEMEDE', kayit_tarihi TEXT, abonelik_gun INTEGER)''')
        
        # Fiyat Ayarları Tablosu
        cursor.execute('''CREATE TABLE IF NOT EXISTS ayarlar (
            id INTEGER PRIMARY KEY, gunluk_fiyat REAL, guncelleme_tarihi TEXT)''')
        
        # Ödeme Kanalları Tablosu
        cursor.execute('''CREATE TABLE IF NOT EXISTS odeme_kanallari (
            id INTEGER PRIMARY KEY, kanal_adi TEXT, detay TEXT)''')
        
        # Başlangıç değerleri
        cursor.execute("INSERT OR IGNORE INTO ayarlar (id, gunluk_fiyat, guncelleme_tarihi) VALUES (1, 150.0, ?)", 
                       (datetime.now().strftime("%Y-%m-%d"),))
        conn.commit()

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row # Verilere sözlük yapısında erişim sağlar
    return conn
