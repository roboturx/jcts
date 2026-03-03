import network, socket, machine, time, binascii, gc
try: import hashlib
except: import uhashlib as hashlib

gc.collect()

# --- 1. DONANIM ---
pins = [14, 15, 16, 17, 18, 19, 20, 21]
röleler = {f'r{i+1}': machine.Pin(p, machine.Pin.OUT) for i, p in enumerate(pins)}
ZIT = {'r1':'r2','r2':'r1','r3':'r4','r4':'r3','r5':'r6','r6':'r5'}

def stop_all():
    for r in röleler.values(): r.value(0)
stop_all()

# --- 2. WI-FI AP ---
ap = network.WLAN(network.AP_IF)
ap.active(False); time.sleep(0.5)
ap.config(essid="!_VINC_COM_PRO", password="password123")
ap.ifconfig(('192.168.4.1', '255.255.255.0', '192.168.4.1', '8.8.8.8'))
ap.active(True)

def get_accept(key):
    d = hashlib.sha1((key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11").encode()).digest()
    return binascii.b2a_base64(d).decode().strip()

# --- 3. WEB ARAYÜZÜ (EN SADE HALİ) ---
def web_page():
    return """<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<style>*{ -webkit-tap-highlight-color:transparent; user-select:none; }
body{font-family:sans-serif;background:#FFCD00;display:flex;align-items:center;justify-content:center;height:100vh;margin:0;overflow:hidden;}
.izg{display:grid;grid-template-columns:1fr 1fr;gap:20px;}
.tus{width:100px;height:100px;background:#1a1a1a;color:#fff;font-size:40px;border-radius:50%;display:flex;align-items:center;justify-content:center;box-shadow:0 8px #000;cursor:pointer}
.akt{background:#444!important;transform:translateY(5px);box-shadow:0 3px #000!important}
#b7{background:#900!important}</style></head><body>
<div class="izg">
<div id="b1" class="tus" data-r="r1">▲</div><div id="b2" class="tus" data-r="r2">▼</div>
<div id="b3" class="tus" data-r="r3">▲</div><div id="b4" class="tus" data-r="r4">▼</div>
<div id="b5" class="tus" data-r="r5">▲</div><div id="b6" class="tus" data-r="r6">▼</div>
<div id="b7" class="tus" style="font-size:20px">STOP</div><div id="b8" class="tus">💡</div>
</div>
<script>
let ws; function cn(){
ws=new WebSocket('ws://'+location.host+'/ws');
ws.onclose=()=>{setTimeout(cn,1000)};
}
function setup(id){
const el=document.getElementById(id), rid=el.dataset.r; if(!rid)return;
el.onpointerdown=(e)=>{e.preventDefault();el.classList.add('akt');ws.send(rid+':1')};
el.onpointerup=(e)=>{e.preventDefault();el.classList.remove('akt');ws.send(rid+':0')};
}
for(let i=1;i<=6;i++)setup('b'+i);
document.getElementById('b7').onpointerdown=(e)=>{ws.send('r7:1')};
document.getElementById('b8').onclick=(e)=>{let k=e.target.classList.toggle('akt');ws.send('r8:'+(k?1:0))};
cn();
</script></body></html>"""

# --- 4. WEBSOCKET ---
def handle_ws(c, addr):
    c.settimeout(0.01)
    last = time.ticks_ms()
    try:
        while True:
            if time.ticks_diff(time.ticks_ms(), last) > 15000: break
            try:
                p = c.recv(128)
                if not p: break
                last = time.ticks_ms()
                if p[0] == 0x81:
                    m, y = p[2:6], p[6:]
                    msg = "".join([chr(y[i] ^ m[i%4]) for i in range(len(y))])
                    if ':' in msg:
                        r, v = msg.split(':')
                        val = int(v)
                        if r == 'r7':
                            stop_all()
                            röleler['r7'].value(val)
                        elif röleler['r7'].value() == 0:
                            if val == 1:
                                if r in ZIT and röleler[ZIT[r]].value(): röleler[ZIT[r]].value(0)
                                röleler[r].value(1)
                            else: röleler[r].value(0)
            except: pass
            time.sleep(0.05)
    finally: stop_all(); c.close()

# --- 5. ANA DÖNGÜ ---
def run():
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', 80)); s.listen(1); s.settimeout(0.5)
    while True:
        gc.collect()
        try:
            try: cl, ad = s.accept()
            except OSError: continue
            req = cl.recv(1024).decode()
            if 'Upgrade: websocket' in req:
                key = [l.split(':')[1].strip() for l in req.split('\r\n') if 'Sec-WebSocket-Key:' in l][0]
                cl.send("HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Accept: "+get_accept(key)+"\r\n\r\n")
                handle_ws(cl, ad)
            else:
                cl.send("HTTP/1.1 200 OK\r\n\r\n" + web_page())
                cl.close()
        except KeyboardInterrupt: break
        except: pass
    s.close()

run()