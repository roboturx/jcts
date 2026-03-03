# ==============================================================================
# VINC SISTEMI V078.5 - BALMER ALARM MODE (CONNECTION SENSITIVE UI)
# ==============================================================================
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
essid, pw, ip = "Vinc_Kumanda_Final", "password123", '192.168.4.1'
ap.config(essid=essid, password=pw)
ap.ifconfig((ip, '255.255.255.0', ip, '8.8.8.8'))
ap.active(True)

print(f"BALMER ALARM MODU AKTIF | IP: {ip}")

def get_accept(key):
    d = hashlib.sha1((key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11").encode()).digest()
    return binascii.b2a_base64(d).decode().strip()

# --- 3. WEB ARAYÜZÜ ---
def web_page():
    return """<!DOCTYPE html><html><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no,viewport-fit=cover">
<style>
*{ -webkit-tap-highlight-color:transparent; -webkit-touch-callout:none; -webkit-user-select:none; user-select:none; outline:none; }
body{font-family:'Arial Black',sans-serif;background:#FFCD00;margin:0;overflow:hidden;display:flex;align-items:center;justify-content:center;height:100vh;touch-action:none}
#st-svg{position:fixed;top:0;left:0;width:100vw;height:100vh;z-index:1;opacity:0.6}
.kum{position:relative;z-index:2;text-align:center;width:280px}
.izg{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:15px}
.tus{width:100px;height:100px;background:#1a1a1a;border:5px solid #000;color:#fff;font-size:45px;font-weight:bold;border-radius:50%;display:flex;align-items:center;justify-content:center;box-shadow:0 8px #000;cursor:pointer}
.akt{background:#444!important;transform:translateY(5px);box-shadow:0 3px #000!important}

#inf-container { position: relative; background: #000; padding: 10px 0; border-radius: 12px; margin-bottom: 15px; border: 3px solid #000; transition: 0.3s; }
#inf { 
    font-size: 55px; font-weight: 900; 
    background: linear-gradient(90deg, #ff0000, #ffee00, #00ff00, #ffee00, #ff0000);
    background-size: 300% 100%; -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    animation: flow 3s linear infinite; transition: 0.3s;
}
/* Baglanti Yoksa (Offline Class) */
.offline #inf { 
    background: #ff0000 !important; -webkit-background-clip: text; -webkit-text-fill-color: transparent; 
    animation: blink 0.5s step-end infinite !important; 
}
@keyframes flow { from { background-position: 0% 50%; } to { background-position: 300% 50%; } }
@keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0.3; } }

#fs-row{margin-top:25px}
#fs-btn{background:#1a1a1a;color:#FFCD00;padding:12px 30px;border-radius:30px;cursor:pointer;font-weight:bold;font-size:14px;border:2px solid #000}
#b7{background:#e74c3c!important;box-shadow:0 8px #922b21}
</style></head><body oncontextmenu="return false;">
    <svg id="st-svg" viewBox="0 0 1000 100" preserveAspectRatio="none">
        <defs><linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="#e74c3c"/><stop offset="50%" stop-color="#f1c40f"/><stop offset="100%" stop-color="#2ecc71"/></linearGradient></defs>
        <path id="wv" fill="none" stroke="url(#g)" stroke-width="6" d="M0 50 L1000 50" stroke-linecap="round"/>
    </svg>
    <div class="kum" id="mainKum">
        <div id="inf-container"><div id="inf">BALMER</div></div>
        <div class="izg">
            <div id="b1" class="tus" data-r="r1">▲</div><div id="b2" class="tus" data-r="r2">▼</div>
            <div id="b3" class="tus" data-r="r3">▲</div><div id="b4" class="tus" data-r="r4">▼</div>
            <div id="b5" class="tus" data-r="r5">▲</div><div id="b6" class="tus" data-r="r6">▼</div>
            <div id="b7" class="tus" style="font-size:20px">STOP</div><div id="b8" class="tus">💡</div>
        </div>
        <div id="fs-row"><span id="fs-btn" onclick="toggleFS()">TAM EKRAN MODU</span></div>
    </div>
<script>
let ws, con=false, pT, tL=50, cL=50, f=0, pts=Array(51).fill(50);
const wv=document.getElementById('wv'), mk=document.getElementById('mainKum');
function toggleFS(){
    if(!document.fullscreenElement) document.documentElement.requestFullscreen();
    else document.exitFullscreen();
}
function solve(d){let p=`M 0 ${100-d[0]}`;for(let i=0;i<d.length-1;i++){p+=` L ${i*20} ${100-d[i]}`;}return p;}
function loop(){
    cL+=(tL-cL)*0.05;
    if(++f>=6){ pts.shift(); pts.push(cL); wv.setAttribute("d",solve(pts)); f=0; }
    requestAnimationFrame(loop);
}
loop();
function cn(){
    ws=new WebSocket('ws://'+location.host+'/ws');
    ws.onopen=()=>{con=true; mk.classList.remove('offline');};
    ws.onclose=()=>{con=false; mk.classList.add('offline'); tL=10; setTimeout(cn,2000)};
    ws.onmessage=(e)=>{if(e.data==='PONG')tL=Math.max(10, 100 - Math.ceil((Date.now()-pT)/6));};
    setInterval(()=>{if(con){pT=Date.now();ws.send('PING');} else {mk.classList.add('offline');}},900);
}
function setup(id){
    const el=document.getElementById(id), rid=el.dataset.r;
    if(!rid) return;
    el.addEventListener('pointerdown', (e)=>{ e.preventDefault(); if(!con) return; el.classList.add('akt'); ws.send(rid+':1'); });
    el.addEventListener('pointerup', (e)=>{ e.preventDefault(); el.classList.remove('akt'); ws.send(rid+':0'); });
}
for(let i=1;i<=6;i++)setup('b'+i);
document.getElementById('b7').onpointerdown=(e)=>{ e.preventDefault(); if(!con)return; let b=document.getElementById('b7'); let k=b.classList.toggle('akt'); ws.send('r7:'+(k?1:0)); };
document.getElementById('b8').onclick=(e)=>{ e.preventDefault(); if(!con)return; let k=e.target.classList.toggle('akt'); ws.send('r8:'+(k?1:0)); };
cn();
</script></body></html>"""

# --- 4. WEBSOCKET VE ANA DÖNGÜ ---
def handle_ws(c, addr):
    c.settimeout(0.01); last = time.ticks_ms()
    try:
        while True:
            now = time.ticks_ms()
            if time.ticks_diff(now, last) > 15000: break
            try:
                p = c.recv(128)
                if not p: break
                last = now
                if p[0] == 0x81:
                    m, y = p[2:6], p[6:]; msg = "".join([chr(y[i] ^ m[i%4]) for i in range(len(y))])
                    if msg == 'PING': c.send(b'\x81\x04PONG')
                    elif ':' in msg:
                        r, v = msg.split(':'); val = int(v)
                        if r == 'r7': 
                            if val == 1: stop_all()
                            röleler['r7'].value(val)
                        elif röleler['r7'].value() == 0:
                            if val == 1:
                                if r in ZIT and röleler[ZIT[r]].value(): röleler[ZIT[r]].value(0)
                                röleler[r].value(1)
                            else: röleler[r].value(0)
            except OSError: pass 
            except KeyboardInterrupt: raise 
            time.sleep(0.02)
    finally: stop_all(); c.close(); gc.collect()

def run():
    s = socket.socket(); s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        s.bind(('', 80)); s.listen(1); s.settimeout(0.5) 
        while True:
            gc.collect()
            try:
                try: cl, ad = s.accept()
                except OSError: continue
                cl.settimeout(0.8)
                req = cl.recv(1024).decode()
                if 'Upgrade: websocket' in req:
                    lines = req.split('\r\n')
                    key = [l.split(':')[1].strip() for l in lines if 'Sec-WebSocket-Key:' in l][0]
                    cl.send("HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Accept: "+get_accept(key)+"\r\n\r\n")
                    handle_ws(cl, ad)
                else:
                    cl.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n" + web_page())
                    cl.close()
            except KeyboardInterrupt: raise 
            except: 
                try: cl.close()
                except: pass
    except KeyboardInterrupt: pass
    finally: stop_all(); s.close()

if __name__ == "__main__":
    run()