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

print("--- SISTEM BASLATILIYOR (KARARLI SURUM) ---")

# --- PIN TANIMLAMALARI ---
led_durum = machine.Pin("LED", machine.Pin.OUT)

röleler = {
    'r1': machine.Pin(14, machine.Pin.OUT),
    'r2': machine.Pin(15, machine.Pin.OUT),
    'r3': machine.Pin(16, machine.Pin.OUT),
    'r4': machine.Pin(17, machine.Pin.OUT),
    'r5': machine.Pin(18, machine.Pin.OUT),
    'r6': machine.Pin(19, machine.Pin.OUT),
    'r7': machine.Pin(20, machine.Pin.OUT),
    'r8': machine.Pin(21, machine.Pin.OUT)
}

ZIT_YONLER = {'r1':'r2','r2':'r1','r3':'r4','r4':'r3','r5':'r6','r6':'r5'}

def tumunu_durdur():
    for i in range(1, 8): röleler['r'+str(i)].value(0)

tumunu_durdur()
led_durum.value(1)

# --- WI-FI KURULUMU (GÜÇLENDİRİLMİŞ) ---
wifi_ap = network.WLAN(network.AP_IF)
# pm=0xa11140 güç tasarrufunu kapatır, bağlantı kopmasını engeller
wifi_ap.config(essid="Vinc_Kumanda_Final", password="12345678", pm=0xa11140)
wifi_ap.ifconfig(('192.168.4.1', '255.255.255.0', '192.168.4.1', '8.8.8.8'))
wifi_ap.active(True)
print(wifi_ap.status())

def anahtar_hesapla(key):
    GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
    hash_obj = hashlib.sha1((key + GUID).encode()).digest()
    return binascii.b2a_base64(hash_obj).decode().strip()

def sayfa_kaynagi():
    return """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<style>
    body{font-family:sans-serif;background:#111;color:#fff;display:flex;align-items:center;justify-content:center;height:100vh;margin:0;overflow:hidden;touch-action:none}
    .ekran-sarici{display:flex;align-items:center;justify-content:center;gap:25px;width:100vw;height:100vh}
    .kumanda{background:#27ae60;padding:15px;border-radius:30px;width:240px;text-align:center;border:5px solid #1e8449;flex-shrink:0;box-shadow:0 10px 30px rgba(0,0,0,0.5)}
    .bagli{background:#f1c40f!important;border-color:#d4ac0d!important}
    .izgara{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:10px}
    .buton-grup{display:flex;flex-direction:column;align-items:center;gap:5px}
    .tus{width:75px;height:75px;background:#222;border:4px solid #333;color:#fff;font-size:26px;border-radius:50%;display:flex;align-items:center;justify-content:center;outline:none;cursor:pointer;user-select:none;-webkit-tap-highlight-color:transparent}
    .tus.aktif{background:#e74c3c!important;border-color:#fff;transform:scale(0.92)}
    .sure-giris{width:45px;background:#333;color:#fff;border:1px solid #555;border-radius:5px;text-align:center;font-size:12px;padding:2px}
    .ozel-tus{border-radius:15px;background:#2c3e50;font-size:16px}
    .durum-paneli{font-size:11px;color:#000;margin-bottom:10px;background:rgba(255,255,255,0.7);border-radius:10px;padding:3px;font-weight:bold;text-transform:uppercase}
    .kilitli{opacity:0.3;pointer-events:none}
    
    /* BAĞIMSIZ SİNYAL KULESİ */
    .sinyal-tower{width:30px;height:85vh;background:#000;border:2px solid #444;border-radius:8px;padding:4px;display:flex;flex-direction:column-reverse;justify-content:space-between;flex-shrink:0}
    .bar{width:100%;height:8.5%;background:#1a1a1a;border-radius:2px;transition:0.2s}
    .lvl-g{background:#2ecc71;box-shadow:0 0 8px #2ecc71}
    .lvl-y{background:#f1c40f;box-shadow:0 0 8px #f1c40f}
    .lvl-r{background:#e74c3c;box-shadow:0 0 8px #e74c3c}
</style>
</head>
<body>
    <div class="ekran-sarici">
        <div id="govde" class="kumanda">
            <div id="bilgi" class="durum-paneli">BEKLIYOR...</div>
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
        <div class="sinyal-tower" id="sinyalMetre"></div>
    </div>
<script>
    let ws, timers = {}, connected = false;
    const info = document.getElementById('bilgi'), govde = document.getElementById('govde'), sinyalMetre = document.getElementById('sinyalMetre');
    
    for(let i=1; i<=10; i++){let b=document.createElement('div'); b.className='bar'; b.id='bar'+i; sinyalMetre.appendChild(b);}
    
    function sinyalGuncelle(s){
        for(let i=1; i<=10; i++){
            let b=document.getElementById('bar'+i); b.className='bar';
            if(i<=s){
                if(i<=3) b.classList.add('lvl-r');
                else if(i<=7) b.classList.add('lvl-y');
                else b.classList.add('lvl-g');
            }
        }
    }

    function connect(){
        ws = new WebSocket('ws://'+window.location.host+'/ws');
        ws.onopen = () => { connected=true; govde.classList.add('bagli'); info.innerText='SISTEM AKTIF'; sinyalGuncelle(10); };
        ws.onmessage = (e) => { if(e.data==='p') sinyalGuncelle(10); };
        ws.onclose = () => { connected=false; govde.classList.remove('bagli'); info.innerText='BAGLANTI KESILDI'; sinyalGuncelle(0); setTimeout(connect,200); };
    }

    function send(r,v){ if(connected && ws.readyState===1) ws.send(r+':'+v); }
    
    function stopT(id,rid){
        if(timers[id]){clearTimeout(timers[id]); delete timers[id];}
        document.getElementById(id).classList.remove('aktif'); send(rid,0);
    }

    function setup(id){
        const el=document.getElementById(id), rid=el.getAttribute('data-rel'), inpt=document.getElementById('s'+id.slice(1));
        const handleStart = (e) => {
            e.preventDefault(); if(!connected || document.getElementById('b7').classList.contains('aktif')) return;
            const s=inpt?parseFloat(inpt.value):0; el.classList.add('aktif'); send(rid,1);
            if(s>0) timers[id]=setTimeout(()=>stopT(id,rid), s*1000);
        };
        const handleEnd = (e) => { e.preventDefault(); if(!(inpt?parseFloat(inpt.value):0)) stopT(id,rid); };
        el.addEventListener('pointerdown', handleStart);
        el.addEventListener('pointerup', handleEnd);
        el.addEventListener('pointerleave', handleEnd);
    }

    for(let i=1; i<=6; i++) setup('b'+i);
    
    document.getElementById('b7').onpointerdown=(e)=>{
        const lock=e.target.classList.toggle('aktif'); send('r7',lock?1:0);
        document.querySelectorAll('.y-tus').forEach(b=>{
            if(lock){b.classList.add('kilitli'); stopT(b.id,b.getAttribute('data-rel'));}
            else b.classList.remove('kilitli');
        });
    };
    
    document.getElementById('b8').onpointerdown=(e)=>{send('r8',e.target.classList.toggle('aktif')?1:0);};
    
    connect();
</script>
</body>
</html>"""

def ws_yonetici(istemci, adres):
    son_sinyal = time.ticks_ms()
    istemci.settimeout(0.1)
    try:
        while True:
            # Sinyal pakedini gönder
            try: istemci.send(b'\x81\x01p')
            except: break
            
            # 15 saniye veri gelmezse güvenli kapatma yap
            if time.ticks_diff(time.ticks_ms(), son_sinyal) > 15000: 
                print("Zaman asimi: Baglanti kesiliyor")
                break
                
            try:
                p = istemci.recv(1024)
                if not p or p[0] == 136: break
                
                # WebSocket Mask çözme
                m, y = p[2:6], p[6:]
                msg = "".join([chr(y[i] ^ m[i % 4]) for i in range(len(y))])
                
                if ':' in msg:
                    rid, v = msg.split(':')
                    son_sinyal = time.ticks_ms() # Her komutta süreyi sıfırla
                    
                    if rid in röleler:
                        val = int(v[0])
                        # Güvenlik Kontrolleri
                        if rid in ['r1','r2','r3','r4','r5','r6'] and röleler['r7'].value() == 1: continue
                        if val == 1 and rid in ZIT_YONLER and röleler[ZIT_YONLER[rid]].value() == 1: continue
                        
                        röleler[rid].value(val)
            except: pass
    finally:
        tumunu_durdur()
        istemci.close()
        gc.collect()

def sunucu_dongusu():
    while True:
        sunucu = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sunucu.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sunucu.bind(('', 80)); sunucu.listen(1)
            print("Sunucu Hazir: 192.168.4.1")
            while True:
                gc.collect()
                c, addr = sunucu.accept()
                try:
                    istek = c.recv(1024).decode()
                    if 'Upgrade: websocket' in istek:
                        lines = istek.split('\r\n')
                        key = [l.split(':')[1].strip() for l in lines if 'Sec-WebSocket-Key:' in l][0]
                        c.send("HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Accept: " + anahtar_hesapla(key) + "\r\n\r\n")
                        ws_yonetici(c, addr)
                    else:
                        c.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + sayfa_kaynagi())
                        c.close()
                except:
                    if c: c.close()
        except:
            if 'sunucu' in locals(): sunucu.close()
            time.sleep(0.1)
            machine.reset()

sunucu_dongusu()
