import network
import socket
import machine
import time
import binascii
try:
    import hashlib
except:
    import uhashlib as hashlib

# --- PIN TANIMLAMALARI ---
led_yesil = machine.Pin("LED", machine.Pin.OUT)
relays = {
    'r1': machine.Pin(14, machine.Pin.OUT), 'r2': machine.Pin(15, machine.Pin.OUT),
    'r3': machine.Pin(16, machine.Pin.OUT), 'r4': machine.Pin(17, machine.Pin.OUT),
    'r5': machine.Pin(18, machine.Pin.OUT), 'r6': machine.Pin(19, machine.Pin.OUT),
    'r7': machine.Pin(20, machine.Pin.OUT), 'r8': machine.Pin(21, machine.Pin.OUT)
}

for r in relays.values(): r.value(0)
led_yesil.value(0)

OPPOSITES = {
    'r1': 'r2', 'r2': 'r1', 'r3': 'r4', 'r4': 'r3', 'r5': 'r6', 'r6': 'r5'
}

# --- WI-FI ---
ap = network.WLAN(network.AP_IF)
ap.config(essid="Vinc_Kumanda_Sistemi", password="password123", pm=0xa11140)
ap.ifconfig(('192.168.4.1', '255.255.255.0', '192.168.4.1', '8.8.8.8'))
ap.active(True)
led_yesil.value(1)

# --- WEBSOCKET EL SIKIŞMA FONKSİYONU (KRİTİK) ---
def calculate_accept(key):
    GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
    hashed = hashlib.sha1((key + GUID).encode()).digest()
    return binascii.b2a_base64(hashed).decode().strip()

# --- WEB SAYFASI ---
def web_page():
    return """<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no"><style>
    body{font-family:sans-serif;background:#1a1a1a;color:#fff;display:flex;justify-content:center;align-items:center;height:100vh;margin:0;overflow:hidden;touch-action:none}
    .pendant{background:#f1c40f;padding:20px;border-radius:30px;width:240px;text-align:center;border:5px solid #d4ac0d}
    .grid{display:grid;grid-template-columns:1fr 1fr;gap:15px;margin-top:10px}
    .btn{width:80px;height:80px;background:#222;border:4px solid #333;color:#fff;font-size:24px;border-radius:50%;cursor:pointer;display:flex;align-items:center;justify-content:center;user-select:none;outline:none;-webkit-tap-highlight-color:transparent}
    .btn.active{background:#e74c3c!important;border-color:#fff;transform:scale(0.95)}
    .square{border-radius:10px;background:#2c3e50}
    .status{font-size:12px;color:#333;margin-bottom:10px;font-weight:bold}
    </style></head><body><div class="pendant"><div id="st" class="status">BAGLANIYOR...</div>
    <div class="grid"><div id="b1" class="btn">▲</div><div id="b2" class="btn">▼</div><div id="b3" class="btn">▲</div><div id="b4" class="btn">▼</div>
    <div id="b5" class="btn">▲</div><div id="b6" class="btn">▼</div><div id="b7" class="btn square">STOP</div><div id="b8" class="btn square">💡</div></div></div>
    <script>
    let ws, st=document.getElementById('st'), lk=false;
    function cn(){
        ws=new WebSocket('ws://'+window.location.host+'/ws');
        ws.onopen=()=>{st.innerText='BAGLI';st.style.color='green';};
        ws.onclose=()=>{st.innerText='KOPUK-DENENIYOR';st.style.color='red';setTimeout(cn,1000)};
    }
    function sc(p,v){if(ws&&ws.readyState==1)ws.send(p+':'+v)}
    function iM(id,p){
        let e=document.getElementById(id);
        const start=(x)=>{x.preventDefault();if(lk)return;e.classList.add('active');sc(p,1)};
        const end=(x)=>{x.preventDefault();e.classList.remove('active');sc(p,0)};
        e.onmousedown=start;e.onmouseup=end;e.ontouchstart=start;e.ontouchend=end;
    }
    function iT(id,p){
        let e=document.getElementById(id);
        e.onclick=()=>{let a=e.classList.toggle('active');if(id=='b7')lk=a;sc(p,a?1:0)};
    }
    for(let i=1;i<=6;i++)iM('b'+i,'r'+i); iT('b7','r7');iT('b8','r8');cn();
    </script></body></html>"""

# --- WEBSOCKET HANDLER ---
def handle_ws(conn, addr):
    conn.setblocking(False)
    print(f"BAĞLANTI SABİTLENDİ: {addr}")
    try:
        while True:
            try:
                data = conn.recv(1024)
                if not data: break
                if data[0] == 136: break # Kapatma frame'i
                
                # Maskelenmiş veriyi çöz
                m = data[2:6]
                p = data[6:]
                msg = "".join([chr(p[i] ^ m[i % 4]) for i in range(len(p))])
                
                if ':' in msg:
                    pid, v_str = msg.split(':')
                    val = int(v_str[0])
                    if pid in relays:
                        if relays['r7'].value() == 1 and int(pid[1:]) <= 6: continue
                        if val == 1 and pid in OPPOSITES and relays[OPPOSITES[pid]].value() == 1: continue
                        relays[pid].value(val)
                        print(f"Röle {pid}: {val}")
            except OSError:
                time.sleep(0.01)
                continue
    except: pass
    finally:
        for r in relays.values(): r.value(0)
        conn.close()
        print(f"AYRILDI: {addr}")

# --- ANA DÖNGÜ ---
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', 80))
s.listen(1)

print("SİSTEM HAZIR: 192.168.4.1 adresine girin.")
while True:
    try:
        c, a = s.accept()
        raw_req = c.recv(1024).decode()
        if 'Upgrade: websocket' in raw_req:
            # Gerçek bir Sec-WebSocket-Key ayıklama
            key = ""
            for line in raw_req.split('\n'):
                if 'Sec-WebSocket-Key:' in line:
                    key = line.split(':')[1].strip()
            
            accept_key = calculate_accept(key)
            resp = "HTTP/1.1 101 Switching Protocols\r\n"
            resp += "Upgrade: websocket\r\n"
            resp += "Connection: Upgrade\r\n"
            resp += f"Sec-WebSocket-Accept: {accept_key}\r\n\r\n"
            c.send(resp)
            handle_ws(c, a)
        else:
            c.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + web_page())
            c.close()
    except Exception as e:
        print("Hata:", e)

