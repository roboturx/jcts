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
        <h2>🛠️ Admin Panel</h2>
        <form action="/admin/fiyat" method="post">
            <input type="number" step="0.01" name="fiyat" value="{{ ayar[1] }}">
            <button class="btn btn-admin">Fiyatı Güncelle</button>
        </form>
        <hr>
        <form action="/admin/odeme" method="post">
            <input type="text" name="kanal" placeholder="Ödeme Kanalı (Örn: IBAN)">
            <input type="text" name="detay" placeholder="Detay (Örn: TR00...)">
            <button class="btn btn-admin">Ekle</button>
        </form>
        <a href="/logout" style="display:block; text-align:center; margin-top:10px;">Çıkış Yap</a>
    </div>
    {% endif %}

    <div class="stat-box">
        <span>Kapasite: {{ aktif }}/{{ kapasite }}</span>
        <span>Birim: <b>{{ ayar[1] }} TL/Gün</b></span>
    </div>

    {% if cookie_plaka %}
    <div class="card">
        <h2>Hoş Geldiniz, {{ cookie_plaka }}</h2>
        <p class="info-text">İşleminiz yönetici onayı bekliyor olabilir.</p>
        <button class="btn btn-primary" onclick="window.location.reload()">Durumu Yenile</button>
    </div>
    {% else %}
    <div class="card">
        <h2>🚗 Yeni Araç Kaydı</h2>
        <form action="/kayit" method="post">
            <input type="text" name="plaka" placeholder="Plaka" required>
            <input type="text" name="ad_soyad" placeholder="Ad Soyad" required>
            <input type="tel" name="telefon" placeholder="Telefon" required>
            <input type="email" name="email" placeholder="E-posta" required>
            <input type="number" name="gun" id="gun_sayisi" min="1" value="1" oninput="hesapla({{ ayar[1] }})">
            <p>Toplam Tutar: <span id="toplam_tutar" class="price-tag">{{ ayar[1] }} TL</span></p>
            <div style="background: #f8fafc; padding: 10px; border-radius: 8px;">
                {% for kanal in odemeler %}
                <p class="info-text">● {{ kanal[1] }}: {{ kanal[2] }}</p>
                {% endfor %}
            </div>
            <button class="btn btn-primary">Kayıt Ol ve Bildir</button>
        </form>
    </div>
    {% endif %}
</body>
</html>
"""
