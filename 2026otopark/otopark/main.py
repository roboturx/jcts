import threading
import sqlite3
from datetime import datetime
from flask import Flask, render_template_string, request, redirect, make_response

# Kendi dosyalarımızdan import ediyoruz
from db import init_db, DB_NAME
from ui import UI_TEMPLATE

app = Flask(__name__)
KAPASITE = 25

@app.route('/')
def index():
    is_admin = request.cookies.get('admin_session') == 'active'
    cookie_plaka = request.cookies.get('user_plaka')
    
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        ayar = cur.execute("SELECT * FROM ayarlar WHERE id=1").fetchone()
        odemeler = cur.execute("SELECT * FROM odeme_kanallari").fetchall()
        aktif = cur.execute("SELECT COUNT(*) FROM users WHERE durum='AKTIF'").fetchone()[0]
        
    return render_template_string(UI_TEMPLATE, is_admin=is_admin, cookie_plaka=cookie_plaka, 
                                  ayar=ayar, odemeler=odemeler, kapasite=KAPASITE, aktif=aktif)

@app.route('/kayit', methods=['POST'])
def register():
    plaka = request.form.get('plaka').upper().replace(" ", "")
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute("INSERT OR REPLACE INTO users (plaka, ad_soyad, telefon, email, kayit_tarihi, abonelik_gun) VALUES (?, ?, ?, ?, ?, ?)",
                    (plaka, request.form.get('ad_soyad'), request.form.get('telefon'), 
                     request.form.get('email'), datetime.now().strftime("%Y-%m-%d"), request.form.get('gun')))
        conn.commit()
    
    resp = make_response(redirect('/'))
    resp.set_cookie('user_plaka', plaka, max_age=60*60*24*365)
    return resp

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
        cur.execute("UPDATE ayarlar SET gunluk_fiyat = ?, guncelleme_tarihi = ? WHERE id=1", 
                    (fiyat, datetime.now().isoformat()))
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
    init_db()  # Veritabanını oluştur/kontrol et
    # Otopark projesinde kamera thread'i buraya eklenecek
    app.run(host='0.0.0.0', port=8080)
