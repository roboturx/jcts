import threading
import sqlite3
from datetime import datetime
from flask import Flask, render_template_string, request, redirect, make_response

app = Flask(__name__)
DB_NAME = "otopark.db"
KAPASITE = 25

# --- 1. VERİTABANI VE TABLO YÖNETİMİ ---
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
        
        # Başlangıç değerleri (Eğer tablo boşsa)
        cursor.execute("INSERT OR IGNORE INTO ayarlar (id, gunluk_fiyat, guncelleme_tarihi) VALUES (1, 150.0, '2026-01-26')")
        conn.commit()

# --- 2. TASARIM (MOBİL UYUMLU & ROL TABANLI) ---
UI_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Otopark Sistemi</title>
    <style>
        body { font-family: -apple-system, sans-serif; background: #f4f7f6; margin: 0; padding: 15px; }
        .card { background: white; padding: 20px; border-radius: 12px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-bottom: 15px; }
        h2 { font-size: 1.1rem; color: #1e293b; margin-top: 0; }
        .stat-box { display: flex; justify-content: space-between; background: #1e293b; color: white; padding: 15px; border-radius: 10px; margin-bottom: 15px; font-size: 0.9rem; }
        input, select { width: 100%; padding: 12px; margin: 8px 0; border: 1px solid #ddd; border-radius: 8px; box-sizing: border-box; }
        .btn { width: 100%; padding: 12px; border: none; border-radius: 8px; font-weight: bold; cursor: pointer; }
        .btn-primary { background: #2563eb; color: white; }
        .btn-admin { background: #10b981; color: white; margin-top: 5px; }
        .price-tag { color: #059669; font-weight: bold; font-size: 1.2rem; }
        .badge { font-size: 0.7rem; padding: 4px 8px; border-radius: 5px; font-weight: bold; }
        .info-text { font-size: 0.85rem; color: #64748b; }
    </style>
    <script>
        function hesapla(fiyat) {
            let gun = document.getElementById('gun_sayisi').value;
            document.getElementById('toplam_tutar').innerText = (gun * fiyat).toFixed(2) + " TL";
        }
    </script>
</head>
<body>

    {% if is_admin %}
    <div class="card" style="border-left: 5px solid #10b981;">
        <h2>🛠️ Admin Panel (Super User)</h2>
        <form action="/admin/fiyat" method="post">
            <label>Günlük Fiyat (TL):</label>
            <input type="number" step="0.01" name="fiyat" value="{{ ayar[1] }}">
            <button class="btn btn-admin">Fiyatı Güncelle</button>
        </form>
        <hr>
        <form action="/admin/odeme" method="post">
            <input type="text" name="kanal" placeholder="Ödeme Kanalı (Örn: IBAN)">
            <input type="text" name="detay" placeholder="Detay (Örn: TR00...)">
            <button class="btn btn-admin">Ödeme Kanalı Ekle</button>
        </form>
        <a href="/logout" style="display:block; text-align:center; margin-top:10px; font-size:0.8rem;">Çıkış Yap</a>
    </div>
    {% endif %}

    <div class="stat-box">
        <span>Kapasite: {{ aktif }}/{{ kapasite }}</span>
        <span>Anlık Fiyat: <b>{{ ayar[1] }} TL</b></span>
    </div>

    {% if cookie_plaka %}
    <div class="card">
        <h2>Hoş Geldiniz, {{ cookie_plaka }}</h2>
        <p class="info-text">Sistemde kayıtlı bir başvurunuz bulunmaktadır.</p>
        <button class="btn btn-primary" onclick="window.location.reload()">Durumu Sorgula</button>
    </div>
    {% else %}
    <div class="card">
        <h2>🚗 Yeni Araç Kaydı</h2>
        <form action="/kayit" method="post">
            <input type="text" name="plaka" placeholder="Plaka" required>
            <input type="text" name="ad_soyad" placeholder="Ad Soyad" required>
            <input type="tel" name="telefon" placeholder="Telefon" required>
            <input type="email" name="email" placeholder="E-posta" required>
            
            <label>Abonelik Süresi (Gün):</label>
            <input type="number" name="gun" id="gun_sayisi" min="1" value="1" oninput="hesapla({{ ayar[1] }})">
            
            <p>Toplam Tutar: <span id="toplam_tutar" class="price-tag">{{ ayar[1] }} TL</span></p>
            
            <div style="background: #f8fafc; padding: 10px; border-radius: 8px; margin-bottom: 10px;">
                <p class="info-text"><b>Ödeme Kanalları:</b></p>
                {% for kanal in odemeler %}
                <p class="info-text">● {{ kanal[1] }}: {{ kanal[2] }}</p>
                {% endfor %}
            </div>
            
            <button class="btn btn-primary">Kayıt Ol ve Ödeme Bildir</button>
        </form>
    </div>
    {% endif %}

    <div class="card">
        <p class="info-text" style="text-align: center;">Yönetici misiniz? <a href="/admin_login">Giriş Yap</a></p>
    </div>

</body>
</html>
"""

# --- 3. ROUTE YÖNETİMİ ---

@app.route('/')
def index():
    is_admin = request.cookies.get('admin_session') == 'active'
    cookie_plaka = request.cookies.get('user_plaka')
    
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        ayar = cur.execute("SELECT * FROM ayarlar WHERE id=1").fetchone()
        odemeler = cur.execute("SELECT * FROM odeme_kanallari").fetchall()
        aktif = cur.execute("SELECT COUNT(*) FROM users WHERE durum='AKTIF'").fetchone()[0]
        users = cur.execute("SELECT * FROM users ORDER BY id DESC").fetchall()
        
    return render_template_string(UI_TEMPLATE, is_admin=is_admin, cookie_plaka=cookie_plaka, 
                                  ayar=ayar, odemeler=odemeler, kapasite=KAPASITE, aktif=aktif, users=users)

@app.route('/kayit', methods=['POST'])
def register():
    plaka = request.form.get('plaka').upper().replace(" ", "")
    ad = request.form.get('ad_soyad')
    gun = request.form.get('gun')
    
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute("INSERT OR REPLACE INTO users (plaka, ad_soyad, telefon, email, kayit_tarihi, abonelik_gun) VALUES (?, ?, ?, ?, ?, ?)",
                    (plaka, ad, request.form.get('telefon'), request.form.get('email'), datetime.now().strftime("%Y-%m-%d"), gun))
        conn.commit()
    
    resp = make_response(redirect('/'))
    resp.set_cookie('user_plaka', plaka, max_age=60*60*24*365) # 1 Yıllık Çerez
    return resp

# --- 4. ADMIN İŞLEMLERİ ---

@app.route('/admin_login')
def admin_login():
    resp = make_response(redirect('/'))
    resp.set_cookie('admin_session', 'active')
    return resp

@app.route('/logout')
def logout():
    resp = make_response(redirect('/'))
    resp.delete_cookie('admin_session')
    resp.delete_cookie('user_plaka')
    return resp

@app.route('/admin/fiyat', methods=['POST'])
def update_price():
    fiyat = request.form.get('fiyat')
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute("UPDATE ayarlar SET gunluk_fiyat = ?, guncelleme_tarihi = ? WHERE id=1", (fiyat, datetime.now().isoformat()))
        conn.commit()
    return redirect('/')

@app.route('/admin/odeme', methods=['POST'])
def add_payment():
    kanal = request.form.get('kanal')
    detay = request.form.get('detay')
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO odeme_kanallari (kanal_adi, detay) VALUES (?, ?)", (kanal, detay))
        conn.commit()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=8080, debug=True)
