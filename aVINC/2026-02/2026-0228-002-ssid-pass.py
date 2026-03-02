import network, socket, machine, time, binascii, gc, _thread
try: import hashlib
except: import uhashlib as hashlib

# --- 1. YAPILANDIRMA ---
SIFRE = "bv2329101"           
STA_SSID = ""#BALMER"           
STA_PASS = "b2329101"         
AP_SSID = "BALMER VİNÇ"       
AP_PASS = "bv2329101"         

print("--- SISTEM: V032 (Thonny Uyumlu & Guvenli Durdurma) ---")

devam_et = True # Global durdurma bayrağı

röleler = {
    'r1': machine.Pin(14, machine.Pin.OUT), 'r2': machine.Pin(15, machine.Pin.OUT),
    'r3': machine.Pin(16, machine.Pin.OUT), 'r4': machine.Pin(17, machine.Pin.OUT),
    'r5': machine.Pin(18, machine.Pin.OUT), 'r6': machine.Pin(19, machine.Pin.OUT),
    'r7': machine.Pin(20, machine.Pin.OUT), 'r8': machine.Pin(21, machine.Pin.OUT)
}
ZIT = {'r1':'r2','r2':'r1','r3':'r4','r4':'r3','r5':'r6','r6':'r5'}
bitis = {k: 0 for k in röleler.keys()}

def stop_all():
    for k in röleler.keys():
        röleler[k].value(0)
        bitis[k] = 0
stop_all()

# --- 2. NETWORK KURULUMU ---
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=AP_SSID, password=AP_PASS)
ap.ifconfig(('192.168.4.1', '255.255.255.0', '192.168.4.1', '8.8.8.8'))

sta = network.WLAN(network.STA_IF)
sta.active(True)

try:
    network.hostname("balmer") 
except:
    pass

if STA_SSID:
    print(f"Harici ağa ({STA_SSID}) bağlanılıyor...", end="")
    sta.connect(STA_SSID, STA_PASS)
    d = 0
    while not sta.isconnected() and d < 10:
        d += 1; time.sleep(0.5); print(".", end="")
    
    if sta.isconnected():
        ip = sta.ifconfig()[0]
        print(f"\n[BAĞLANDI] Harici IP: {ip}")
        try: ap.config(essid=f"{AP_SSID}-{ip.split('.')[-1]}") 
        except: pass

# --- 3. DNS SERVER (Captive Portal) ---
def dns_server():
    global devam_et
    udps = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udps.settimeout(0.5) # Thonny'nin durdurabilmesi için kritik
    udps.bind(('0.0.0.0', 53))
    while devam_et:
        try:
            data, addr = udps.recvfrom(1024)
            p = data[:2] + b"\x81\x80\x00\x01\x00\x01\x00\x00\x00\x00" + data[12:]
            p += b"\xc0\x0c\x00\x01\x00\x01\x00\x00\x00\x3c\x00\x04\xc0\xa8\x04\x01"
            udps.sendto(p, addr)
        except: pass
    udps.close()
    print("[DNS] Kapatıldı.")

_thread.start_new_thread(dns_server, ())

def get_accept(key):
    d = hashlib.sha1((key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11").encode()).digest()
    return binascii.b2a_base64(d).decode().strip()

# --- 4. WEB ARAYÜZÜ ---
def web_page():
    return """<!DOCTYPE html><html><head><meta charset="UTF-8">
    <meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
    <title>BALMER VİNÇ</title>
    <style>
        @keyframes blink { 0% {background-color:#7f8c8d} 50% {background-color:#e74c3c} 100% {background-color:#7f8c8d} }
        body{font-family:sans-serif;background:#111;color:#fff;display:flex;align-items:center;justify-content:center;height:100vh;margin:0;overflow:hidden;touch-action:none}
        .s-wra{display:flex;gap:15px}
        .kum{background:#f1c40f;padding:15px;border-radius:25px;width:220px;text-align:center;border:4px solid #d4ac0d}
        .izg{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:10px}
        .tus{width:70px;height:70px;background:#222;border:3px solid #333;color:#fff;font-size:24px;border-radius:50%;display:flex;align-items:center;justify-content:center}
        .akt{background:#e67e22!important;border-color:#fff}
        .inp{width:40px;background:#333;color:#fff;border:1px solid #555;border-radius:4px;text-align:center}
        .st-t{width:26px;height:60vh;background:#000;border-radius:5px;display:flex;flex-direction:column-reverse;justify-content:space-between;padding:2px;border:1px solid #333}
        .bar{width:100%;height:8.5%;background:#1a1a1a}.l-g{background:#2ecc71}
        #b7{background:#e74c3c;font-weight:bold}
        #b7.pasif{animation: blink 2s step-end infinite !important; border-color:#fff !important}
        .estop-green{background-color:#2ecc71!important; border-color:#27ae60!important}
        #lck{position:fixed;top:0;left:0;width:100%;height:100%;background:#111;display:flex;flex-direction:column;align-items:center;justify-content:center;z-index:999}
        input#psw{padding:15px;font-size:20px;width:150px;text-align:center;margin-bottom:10px;border-radius:10px;border:none}
    </style></head>
    <body>
        <div id="lck"><h3>BALMER VİNÇ</h3><input type="password" id="psw" placeholder="Şifre"><button onclick="check()" style="padding:10px 20px;border-radius:10px;background:#f1c40f;border:none;font-weight:bold">GIRIŞ</button></div>
        <div class="s-wra" id="main" style="display:none">
            <div id="gv" class="kum">
                <div id="inf" style="font-size:10px;color:#000;background:#fff;border-radius:5px;padding:2px;margin-bottom:5px">BAĞLANIYOR...</div>
                <div class="izg">
                    <div class="gr"><div id="b1" class="tus" data-r="r1">▲</div><input type="number" id="s1" class="inp"></div>
                    <div class="gr"><div id="b2" class="tus" data-r="r2">▼</div><input type="number" id="s2" class="inp"></div>
                    <div class="gr"><div id="b3" class="tus" data-r="r3">▲</div><input type="number" id="s3" class="inp"></div>
                    <div class="gr"><div id="b4" class="tus" data-r="r4">▼</div><input type="number" id="s4" class="inp"></div>
                    <div class="gr"><div id="b5" class="tus" data-r="r5">▲</div><input type="number" id="s5" class="inp"></div>
                    <div class="gr"><div id="b6" class="tus" data-r="r6">▼</div><input type="number" id="s6" class="inp"></div>
                    <div id="b7" class="tus" style="border-radius:10px;font-size:14px">E-STOP</div>
                    <div id="b8" class="tus" style="border-radius:10px">💡</div>
                </div>
            </div>
            <div id="st" class="st-t"></div> </div>
        <script>
            let ws,con=false;const S='"""+SIFRE+"""';
            function check(){if(document.getElementById('psw').value===S){document.getElementById('lck').style.display='none';document.getElementById('main').style.display='flex';cn();}else{alert('Hatalı!');}}
            for(let i=1;i<=10;i++)document.getElementById('st').innerHTML+='<div class="bar l-g" id="br'+i+'"></div>';
            function cn(){
                ws=new WebSocket('ws://'+window.location.host+'/ws');
                ws.onopen=()=>{con=true;document.getElementById('inf').innerText='SISTEM AKTIF';};
                ws.onclose=()=>{con=false;setTimeout(cn,2000)};
            }
            function setup(id){
                const el=document.getElementById(id),rid=el.dataset.r,inp=document.getElementById('s'+id.slice(1));
                el.onpointerdown=(e)=>{
                    e.preventDefault();if(!con||document.getElementById('b7').classList.contains('pasif'))return;
                    const s=parseFloat(inp?.value)||0;el.classList.add('akt');ws.send(rid+':1:'+s);
                };
                el.onpointerup=()=>{if(!parseFloat(inp?.value)){el.classList.remove('akt');ws.send(rid+':0:0')}};
            }
            for(let i=1;i<=6;i++)setup('b'+i);
            document.getElementById('b7').onpointerdown=()=>{let k=document.getElementById('b7').classList.toggle('pasif');document.getElementById('gv').classList.toggle('estop-green',k);ws.send('r7:'+(k?1:0)+':0');};
            document.getElementById('b8').onclick=(e)=>{if(!document.getElementById('b7').classList.contains('pasif'))ws.send('r8:'+(e.target.classList.toggle('akt')?1:0)+':0')};
        </script>
    </body></html>"""

# --- 5. SERVER ---
def handle_ws(c, addr):
    global devam_et
    c.settimeout(0.05)
    last = time.ticks_ms()
    try:
        while devam_et:
            now = time.ticks_ms()
            if time.ticks_diff(now, last) > 20000: break # 20sn sessizlikte kopar
            
            for r, t in bitis.items():
                if t != 0 and time.ticks_diff(t, now) <= 0:
                    röleler[r].value(0); bitis[r] = 0
            try:
                p = c.recv(1024)
                if not p: break
                last = now
                if p[0] == 0x88: break # Close frame
                m, y = p[2:6], p[6:]; msg = "".join([chr(y[i] ^ m[i%4]) for i in range(len(y))])
                if ':' in msg:
                    r, v, s = msg.split(':'); val, sn = int(v), float(s)
                    if r == 'r7':
                        if val == 1: stop_all()
                        röleler['r7'].value(val); continue
                    if röleler['r7'].value() == 1: continue
                    if val == 1:
                        if r in ZIT and röleler[ZIT[r]].value():
                            röleler[ZIT[r]].value(0); bitis[ZIT[r]]=0
                        röleler[r].value(1)
                        bitis[r] = time.ticks_add(now, int(sn*1000)) if sn > 0 else 0
                    else:
                        if not bitis[r]: röleler[r].value(0)
            except OSError: pass
            time.sleep(0.01)
    finally:
        c.close()

def run():
    global devam_et
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', 80)); s.listen(2)
    s.settimeout(1.0) # Her saniye döngüyü kırıp devam_et'i kontrol eder
    
    print("Sistem Çalışıyor. Durdurmak için Ctrl+C...")
    
    try:
        while devam_et:
            gc.collect()
            try:
                cl, ad = s.accept()
            except OSError:
                continue # Timeout oldu, başa dönüp devam_et'i kontrol et
                
            try:
                cl.settimeout(1.0)
                req = cl.recv(1024).decode()
                if 'Upgrade: websocket' in req:
                    key = [l.split(':')[1].strip() for l in req.split('\r\n') if 'Sec-WebSocket-Key:' in l][0]
                    cl.send("HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Accept: "+get_accept(key)+"\r\n\r\n")
                    handle_ws(cl, ad)
                else:
                    cl.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + web_page())
                    cl.close()
            except:
                cl.close()
    except KeyboardInterrupt:
        print("\n[DURDURULUYOR] Thonny sinyali alındı.")
    finally:
        devam_et = False
        stop_all()
        s.close()
        print("[KAPATILDI] Güvenli mod aktif.")

if __name__ == "__main__":
    run()
