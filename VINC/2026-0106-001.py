import network      # Wi-Fi ağını yönetmek için
import socket       # TCP ve WebSocket bağlantıları için
import machine      # Pin kontrolü ve donanımsal reset için
import time         # Gecikmeler ve zaman farkı ölçümü için
import binascii     # Verileri Base64 formatına çevirmek için
import gc           # Bellek (RAM) temizliği için

# WebSocket güvenliği (Handshake) için SHA1 algoritması gerekir
try:
    import hashlib
except:
    import uhashlib as hashlib

print("--- SISTEM BASLATILIYOR ---")

# --- PIN TANIMLAMALARI ---
led_durum = machine.Pin("LED", machine.Pin.OUT) # Pico üzerindeki çalışma LED'i

# Röle Pinleri (Pin numaralarını kendi devrene göre kontrol et)
röleler = {
    'r1': machine.Pin(14, machine.Pin.OUT), # Yukarı 1
    'r2': machine.Pin(15, machine.Pin.OUT), # Aşağı 1
    'r3': machine.Pin(16, machine.Pin.OUT), # Yukarı 2
    'r4': machine.Pin(17, machine.Pin.OUT), # Aşağı 2
    'r5': machine.Pin(18, machine.Pin.OUT), # İleri
    'r6': machine.Pin(19, machine.Pin.OUT), # Geri
    'r7': machine.Pin(20, machine.Pin.OUT), # STOP (Basılı Kalan Kilit)
    'r8': machine.Pin(21, machine.Pin.OUT)  # Lamba (Basılı Kalan)
}

# Aynı anda çalışmaması gereken zıt yön eşleşmeleri
ZIT_YONLER = {'r1':'r2','r2':'r1','r3':'r4','r4':'r3','r5':'r6','r6':'r5'}

def tumunu_durdur():
    """Lamba hariç hareketli tüm röleleri kapatır"""
    print("Tum hareketler durduruluyor...")
    for i in range(1, 8): röleler['r'+str(i)].value(0)

# Başlangıçta her şeyi kapat ve LED'i yak
tumunu_durdur()
led_durum.value(1)

# --- WI-FI KURULUMU (ACCESS POINT) ---
wifi_ap = network.WLAN(network.AP_IF)
wifi_ap.config(essid="Vinc_Kumanda_Final", password="password123", pm=0xa11140)
wifi_ap.ifconfig(('192.168.4.1', '255.255.255.0', '192.168.4.1', '8.8.8.8'))
wifi_ap.active(True)
print("Wi-Fi Aktif: Vinc_Kumanda_Final")

def anahtar_hesapla(key):
    """WebSocket el sıkışma anahtarını hesaplar"""
    GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
    hash_obj = hashlib.sha1((key + GUID).encode()).digest()
    return binascii.b2a_base64(hash_obj).decode().strip()

def sayfa_kaynagi():
    """Tarayıcıda görünecek olan arayüz kodları"""
    return """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<style>
    body{font-family:sans-serif;background:#1a111a;color:#fff;display:flex;justify-content:center;height:100vh;margin:0;overflow:hidden;touch-action:none}
    .kumanda{background:#27ae60;padding:15px;border-radius:30px;width:250px;text-align:center;border:5px solid #1e8449}
    .bagli{background:#f1c40f!important;border-color:#d4ac0d!important}
    .izgara{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:10px}
    .buton-grup{display:flex;flex-direction:column;align-items:center;gap:5px}
    .tus{width:80px;height:80px;background:#222;border:4px solid #333;color:#fff;font-size:26px;border-radius:50%;display:flex;align-items:center;justify-content:center;user-select:none;outline:none;cursor:pointer}
    .tus.aktif{background:#e74c3c!important;border-color:#fff;transform:scale(0.95)}
    .sure-giris{width:50px;background:#333;color:#fff;border:1px solid #555;border-radius:5px;text-align:center;font-size:14px}
    .ozel-tus{border-radius:15px;background:#2c3e50;font-size:18px}
    .durum-paneli{font-size:11px;color:#000;margin-bottom:10px;background:rgba(255,255,255,0.7);border-radius:10px;padding:3px;font-weight:bold}
    .kilitli{opacity:0.3;pointer-events:none}
</style>
</head>
<body>
    <div id="govde" class="kumanda">
        <div id="bilgi" class="durum-paneli">BAGLANTI BEKLENIYOR</div>
        <div class="izgara">
            <div class="buton-grup"><div id="b1" class="tus y-tus" data-rel="r1">▲</div><input type="number" id="s1" class="sure-giris" placeholder="sn"></div>
            <div class="buton-grup"><div id="b2" class="tus y-tus" data-rel="r2">▼</div><input type="number" id="s2" class="sure-giris" placeholder="sn"></div>
            <div class="buton-grup"><div id="b3" class="tus y-tus" data-rel="r3">▲</div><input type="number" id="s3" class="sure-giris" placeholder="sn"></div>
            <div class="buton-grup"><div id="b4" class="tus y-tus" data-rel="r4">▼</div><input type="number" id="s4" class="sure-giris" placeholder="sn"></div>
            <div class="buton-grup"><div id="b5" class="tus y-tus" data-rel="r5">▲</div><input type="number" id="s5" class="sure-giris" placeholder="sn"></div>
            <div class="buton-grup"><div id="b6" class="tus y-tus" data-rel="r6">▼</div><input type="number" id="s6" class="sure-giris" placeholder="sn"></div>
            <div class="buton-grup"><div id="b7" class="tus ozel-tus">STOP</div></div>
            <div class="buton-grup"><div id="b8" class="tus ozel-tus">💡</div></div>
        </div>
    </div>
<script>
    let ws, timers = {}, connected = false;
    const info = document.getElementById('bilgi'), govde = document.getElementById('govde');

    function connect() {
        ws = new WebSocket('ws://' + window.location.host + '/ws');
        ws.onopen = () => { connected = true; govde.classList.add('bagli'); info.innerText = 'BAGLI'; };
        ws.onclose = () => { connected = false; govde.classList.remove('bagli'); info.innerText = 'KESILDI'; setTimeout(connect, 2000); };
    }

    function send(rid, v) { if(connected && ws.readyState === 1) ws.send(rid + ':' + v); }

    function stopT(id, rid) {
        if(timers[id]) { clearTimeout(timers[id]); delete timers[id]; }
        document.getElementById(id).classList.remove('aktif');
        send(rid, 0);
    }

    function setup(id) {
        const el = document.getElementById(id);
        const rid = el.getAttribute('data-rel');
        const inpt = document.getElementById('s'+id.slice(1));

        el.onpointerdown = (e) => {
            e.preventDefault();
            if(!connected || document.getElementById('b7').classList.contains('aktif')) return;
            const s = inpt ? parseFloat(inpt.value) : 0;
            el.classList.add('aktif'); send(rid, 1);
            if(s > 0) timers[id] = setTimeout(() => stopT(id, rid), s * 1000);
        };

        el.onpointerup = (e) => {
            e.preventDefault();
            const s = inpt ? parseFloat(inpt.value) : 0;
            if(!s || s <= 0) stopT(id, rid);
        };
    }

    // Yön Tuşlarını Kur (r1-r6)
    for(let i=1; i<=6; i++) setup('b'+i);

    // STOP Butonu (r7) - Basılı Kalan Kilit
    document.getElementById('b7').onpointerdown = (e) => {
        const isLocked = e.target.classList.toggle('aktif');
        send('r7', isLocked ? 1 : 0);
        document.querySelectorAll('.y-tus').forEach(btn => {
            if(isLocked) { 
                btn.classList.add('kilitli');
                stopT(btn.id, btn.getAttribute('data-rel'));
            } else {
                btn.classList.remove('kilitli');
            }
        });
    };

    // LAMBA Butonu (r8) - Basılı Kalan
    document.getElementById('b8').onpointerdown = (e) => {
        const isOn = e.target.classList.toggle('aktif');
        send('r8', isOn ? 1 : 0);
    };

    connect();
</script>
</body>
</html>"""

def ws_yonetici(istemci, adres):
    """Gelen WebSocket komutlarını yönetir"""
    son_sinyal = time.ticks_ms()
    istemci.settimeout(0.1)
    print("WS Baglandi:", adres)
    try:
        while True:
            # 5 saniye boyunca veri gelmezse bağlantıyı düşür
            if time.ticks_diff(time.ticks_ms(), son_sinyal) > 5000: break
            try:
                p = istemci.recv(1024)
                if not p or p[0] == 136: break
                
                # Maskelenmiş WebSocket verisini çöz
                m, y = p[2:6], p[6:]
                msg = "".join([chr(y[i] ^ m[i % 4]) for i in range(len(y))])
                
                if ':' in msg:
                    rid, v = msg.split(':')
                    son_sinyal = time.ticks_ms()
                    
                    if rid in röleler:
                        val = int(v[0])
                        # GÜVENLİK: r7 (STOP) aktifse r1-r6 komutlarını görmezden gel
                        if rid in ['r1','r2','r3','r4','r5','r6'] and röleler['r7'].value() == 1:
                            continue
                        
                        # GÜVENLİK: Zıt yön koruması
                        if val == 1 and rid in ZIT_YONLER and röleler[ZIT_YONLER[rid]].value() == 1:
                            print("Engel: Zit yon aktif!")
                            continue
                            
                        röleler[rid].value(val)
                        print(f"Komut: {rid} -> {val}") # REPL Çıktısı
            except OSError: pass
    finally:
        print("WS Kapatildi.")
        tumunu_durdur()
        istemci.close()
        gc.collect()

def sunucu_dongusu():
    """HTTP Sunucu ve WebSocket el sıkışma döngüsü"""
    while True:
        sunucu = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sunucu.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sunucu.bind(('', 80))
            sunucu.listen(1)
            print("Sunucu Dinlemede (192.168.4.1)...")
            while True:
                gc.collect()
                c, addr = sunucu.accept()
                try:
                    istek = c.recv(1024).decode()
                    if 'Upgrade: websocket' in istek:
                        # WebSocket el sıkışması
                        lines = istek.split('\r\n')
                        key = [l.split(':')[1].strip() for l in lines if 'Sec-WebSocket-Key:' in l][0]
                        c.send("HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Accept: " + anahtar_hesapla(key) + "\r\n\r\n")
                        ws_yonetici(c, addr)
                    else:
                        # Normal Web Sayfası gönderimi
                        c.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + sayfa_kaynagi())
                        c.close()
                except Exception as e:
                    if c: c.close()
                    print("Istek Hatasi:", e)
        except Exception as e:
            print("Kritik Hata, Resetleniyor:", e)
            sunucu.close()
            time.sleep(2)
            machine.reset()

# Programı başlat
sunucu_dongusu()

