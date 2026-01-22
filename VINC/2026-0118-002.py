# Gerekli sistem kütüphaneleri içe aktarılıyor
import network, socket, machine, time, binascii, gc
try: import hashlib
except: import uhashlib as hashlib

# VERSİYON: 2026-01-18.015 (011'e Geri Dönüş - Stabil Animasyon & Renk)
print("--- SISTEM: V1 + 011 REFERANS GERI YUKLEME (V015) ---")

# --- VERSİYON LOG DOSYASI ---
"""
[COPYABLE LOG FILE]
Versiyon: 2026-01-18.011 | Animasyon Fix ve CSS öncelik güncellendi (Referans).
Versiyon: 2026-01-18.012 | Hassas RSSI denemesi (Deneysel).
Versiyon: 2026-01-18.013 | Bar üstü sayısal gösterge denemesi.
Versiyon: 2026-01-18.014 | Bağlantı kurtarma ve soket temizliği denemesi.
Versiyon: 2026-01-18.015 | Kullanıcı isteğiyle 011 sürümüne geri dönüldü.
--------------------------------------------------
"""

# Rölelerin bağlı olduğu GPIO pin numaraları tanımlanıyor
röleler = {
    'r1': machine.Pin(14, machine.Pin.OUT), 'r2': machine.Pin(15, machine.Pin.OUT),
    'r3': machine.Pin(16, machine.Pin.OUT), 'r4': machine.Pin(17, machine.Pin.OUT),
    'r5': machine.Pin(18, machine.Pin.OUT), 'r6': machine.Pin(19, machine.Pin.OUT),
    'r7': machine.Pin(20, machine.Pin.OUT), 'r8': machine.Pin(21, machine.Pin.OUT)
}

# Birbirine zıt çalışan röle çiftleri
ZIT = {'r1':'r2','r2':'r1','r3':'r4','r4':'r3','r5':'r6','r6':'r5'}

# Rölelerin otomatik kapanma zamanlarını tutan liste
bitis = {k: 0 for k in röleler.keys()}

# Sistemin tüm çıkışlarını kapatan güvenlik fonksiyonu
def stop_all():
    for k in röleler.keys():
        röleler[k].value(0)
        bitis[k] = 0

# İlk açılışta temizle
stop_all()

# Wi-Fi Access Point ayarları
ap = network.WLAN(network.AP_IF)
ap.active(False); time.sleep(0.5)
ap.config(essid="Vinc_Kumanda_Final", password="password123")
ap.ifconfig(('192.168.4.1', '255.255.255.0', '192.168.4.1', '8.8.8.8'))
ap.active(True)

# WebSocket el sıkışma algoritması
def get_accept(key):
    d = hashlib.sha1((key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11").encode()).digest()
    return binascii.b2a_base64(d).decode().strip()

# Web arayüzü fonksiyonu (011 Sürümü CSS ve Animasyon Mantığı)
def web_page():
    return """<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no"><style>
@keyframes blink { 0% {background-color:#7f8c8d} 50% {background-color:#e74c3c} 100% {background-color:#7f8c8d} }
body{font-family:sans-serif;background:#111;color:#fff;display:flex;align-items:center;justify-content:center;height:100vh;margin:0;overflow:hidden;touch-action:none;-webkit-user-select:none;user-select:none}
.s-wra{display:flex;gap:15px}.kum{background:#f1c40f;padding:15px;border-radius:25px;width:220px;text-align:center;border:4px solid #d4ac0d;transition:background 0.3s}
.bag{background:#f1c40f!important}.izg{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:10px}
.tus{width:70px;height:70px;background:#222;border:3px solid #333;color:#fff;font-size:24px;border-radius:50%;display:flex;align-items:center;justify-content:center;touch-action:none}
.akt{background:#e67e22!important;border-color:#fff}.inp{width:40px;background:#333;color:#fff;border:1px solid #555;border-radius:4px;text-align:center}
.st-t{width:20px;height:70vh;background:#000;border-radius:5px;display:flex;flex-direction:column-reverse;justify-content:space-between;padding:2px}
.bar{width:100%;height:8.5%;background:#1a1a1a}.l-r{background:#e74c3c}.l-y{background:#f1c40f}.l-g{background:#2ecc71}
.bosta-btn{width:100%;height:45px;background:#34495e;border-radius:10px;margin-top:10px;display:flex;align-items:center;justify-content:center;border:2px solid #2c3e50;font-size:13px;color:#fff}
#b7{background:#e74c3c;font-weight:bold;transition: none}
#b7.pasif{animation: blink 2s step-end infinite !important; border-color:#fff !important; background-image: none !important}
.estop-green{background-color:#2ecc71!important; border-color:#27ae60!important}
</style></head><body oncontextmenu="return false;"><div class="s-wra"><div id="gv" class="kum"><div id="inf" style="font-size:10px;color:#000;background:#fff;border-radius:5px;padding:2px;margin-bottom:5px">BAGLANIYOR...</div><div class="izg">
<div class="gr"><div id="b1" class="tus" data-r="r1" data-z="b2">▲</div><input type="number" id="s1" class="inp"></div>
<div class="gr"><div id="b2" class="tus" data-r="r2" data-z="b1">▼</div><input type="number" id="s2" class="inp"></div>
<div class="gr"><div id="b3" class="tus" data-r="r3" data-z="b4">▲</div><input type="number" id="s3" class="inp"></div>
<div class="gr"><div id="b4" class="tus" data-r="r4" data-z="b3">▼</div><input type="number" id="s4" class="inp"></div>
<div class="gr"><div id="b5" class="tus" data-r="r5" data-z="b6">▲</div><input type="number" id="s5" class="inp"></div>
<div class="gr"><div id="b6" class="tus" data-r="r6" data-z="b5">▼</div><input type="number" id="s6" class="inp"></div>
<div id="b7" class="tus" style="border-radius:10px;font-size:14px">E-STOP</div><div id="b8" class="tus" style="border-radius:10px">💡</div></div></div><div style="display:flex;flex-direction:column;align-items:center"><div id="st" class="st-t"></div><div class="bosta-btn">YETKİ</div></div></div>
<script>
let ws,con=false,tmr={};const gv=document.getElementById('gv'),inf=document.getElementById('inf'),st=document.getElementById('st'),b7=document.getElementById('b7');
for(let i=1;i<=10;i++)st.innerHTML+='<div class="bar" id="br'+i+'"></div>';
function sG(s){for(let i=1;i<=10;i++){let b=document.getElementById('br'+i);b.className='bar';if(i<=s)b.classList.add(i<=3?'l-r':i<=7?'l-y':'l-g');}}
function cn(){ws=new WebSocket('ws://'+location.host+'/ws');
ws.onopen=()=>{con=true;gv.classList.add('bag');inf.innerText='SISTEM AKTIF';sG(10);setInterval(()=>{if(con)ws.send('p')},1000)};
ws.onclose=()=>{con=false;gv.classList.remove('bag');inf.innerText='KESILDI';sG(0);setTimeout(cn,1500)};}
function setup(id){
const el=document.getElementById(id),rid=el.dataset.r,zid=el.dataset.z,inp=document.getElementById('s'+id.slice(1));
el.onpointerdown=(e)=>{e.preventDefault();if(!con||b7.classList.contains('pasif'))return;
const s=parseFloat(inp?.value)||0;el.classList.add('akt');ws.send(rid+':1:'+s);
if(s>0)tmr[id]=setTimeout(()=>{el.classList.remove('akt');ws.send(rid+':0:0')},s*1000)};
el.onpointerup=()=>{if(!parseFloat(inp?.value)){el.classList.remove('akt');ws.send(rid+':0:0')}};}
for(let i=1;i<=6;i++)setup('b'+i);
b7.onpointerdown=(e)=>{let k=e.target.classList.toggle('pasif');
if(k){
    gv.classList.add('estop-green');
    document.querySelectorAll('.tus').forEach(b=>{if(b.id!='b7'&&b.id!='b8')b.classList.remove('akt')});for(let t in tmr)clearTimeout(tmr[t])
}else{
    gv.classList.remove('estop-green');
}
ws.send('r7:'+(k?1:0)+':0');};
document.getElementById('b8').onclick=(e)=>{if(!b7.classList.contains('pasif'))ws.send('r8:'+(e.target.classList.toggle('akt')?1:0)+':0')};
cn();</script></body></html>"""

# WebSocket veri yönetim fonksiyonu
def handle_ws(c, addr):
    c.settimeout(0.01); last = time.ticks_ms()
    try:
        while True:
            now = time.ticks_ms()
            if time.ticks_diff(now, last) > 5000: break
            for r, t in bitis.items():
                if t != 0 and time.ticks_diff(t, now) <= 0:
                    röleler[r].value(0); bitis[r] = 0
            try:
                p = c.recv(1024)
                if not p: break
                last = now
                m, y = p[2:6], p[6:]; msg = "".join([chr(y[i] ^ m[i%4]) for i in range(len(y))])
                if ':' in msg:
                    r, v, s = msg.split(':')
                    val, sn = int(v), float(s)
                    if r == 'r7':
                        if val == 1: stop_all()
                        röleler['r7'].value(val); continue
                    if röleler['r7'].value() == 1: continue
                    if val == 1:
                        if r in ZIT:
                            z = ZIT[r]
                            if röleler[z].value(): röleler[z].value(0); bitis[z]=0; time.sleep(0.01)
                        röleler[r].value(1)
                        bitis[r] = time.ticks_add(now, int(sn*1000)) if sn > 0 else 0
                    else:
                        if not bitis[r]: röleler[r].value(0)
            except: pass
            time.sleep(0.01)
    finally:
        c.close(); gc.collect()

# Ana sunucu döngüsü
def run():
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', 80)); s.listen(1)
    print("Sistem hazir. 015 (011 Stabil) Aktif.")
    while True:
        gc.collect()
        try:
            cl, ad = s.accept(); cl.settimeout(1.0)
            req = cl.recv(1024).decode()
            if 'Upgrade: websocket' in req:
                key = [l.split(':')[1].strip() for l in req.split('\r\n') if 'Sec-WebSocket-Key:' in l][0]
                cl.send("HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Accept: "+get_accept(key)+"\r\n\r\n")
                handle_ws(cl, ad)
            else:
                resp = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nCache-Control: max-age=86400\r\nConnection: close\r\n\r\n" + web_page()
                cl.send(resp); cl.close()
        except:
            time.sleep(0.05)

# Anakod bunu yap
run()
