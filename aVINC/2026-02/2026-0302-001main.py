import network, socket, machine, time, binascii, gc
try: import hashlib
except: import uhashlib as hashlib

# VERSİYON: 2026-03-02.010 (V036 - RENK SIRALAMASI GÜNCELLENDİ)
print("--- SISTEM: V036 RENK SIRALAMASI GÜNCELLENDİ ---")

# --- 1. DONANIM ---
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

# --- 2. NETWORK ---
ap = network.WLAN(network.AP_IF)
ap.active(False); time.sleep(0.5)
ap.config(essid="Vinc_Kumanda_Final", password="password123")
ap.ifconfig(('192.168.4.1', '255.255.255.0', '192.168.4.1', '8.8.8.8'))
ap.active(True)

def get_accept(key):
    d = hashlib.sha1((key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11").encode()).digest()
    return binascii.b2a_base64(d).decode().strip()

# --- 3. WEB ARAYÜZÜ ---
def web_page():
    return """<!DOCTYPE html><html><head><meta charset="UTF-8">
    <meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
    <style>
        @keyframes blink { 0% {background-color:#7f8c8d} 50% {background-color:#e74c3c} 100% {background-color:#7f8c8d} }
        body{font-family:sans-serif;background:#111;color:#fff;display:flex;align-items:center;justify-content:center;height:100vh;margin:0;overflow:hidden;touch-action:none;-webkit-user-select:none;user-select:none}
        .s-wra{display:flex;gap:15px;align-items:stretch}
        .kum{background:#f1c40f;padding:15px;border-radius:25px;width:220px;text-align:center;border:4px solid #d4ac0d;display:flex;flex-direction:column;justify-content:space-between}
        .izg{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:10px}
        .tus{width:70px;height:70px;background:#222;border:3px solid #333;color:#fff;font-size:24px;border-radius:50%;display:flex;align-items:center;justify-content:center}
        .akt{background:#e67e22!important;border-color:#fff}
        .inp{width:40px;background:#333;color:#fff;border:1px solid #555;border-radius:4px;text-align:center}
        .st-t{width:26px;background:#000;border-radius:5px;display:flex;flex-direction:column-reverse;justify-content:space-between;padding:4px;border:1px solid #333}
        .bar{width:100%;height:8.5%;background:#1a1a1a;transition: opacity 0.1s}
        #b7{background:#e74c3c;font-weight:bold}
        #b7.pasif{animation: blink 2s step-end infinite !important; border-color:#fff !important}
        .estop-green{background-color:#2ecc71!important; border-color:#27ae60!important}
    </style></head>
    <body>
        <div class="s-wra">
            <div id="gv" class="kum">
                <div id="inf" style="font-size:10px;color:#000;background:#fff;border-radius:5px;padding:2px;margin-bottom:5px">BAGLI</div>
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
            let ws,con=false,pT;const inf=document.getElementById('inf'),b7=document.getElementById('b7'),st=document.getElementById('st');
            // GÜNCELLENMİŞ RENK SIRALAMASI
            const colors=['#b71c1c','#e74c3c','#fbc02d','#f1c40f','#1b5e20','#1b5e20','#2ecc71','#2ecc71','#2ecc71','#2ecc71'];
            for(let i=1;i<=10;i++)st.innerHTML+='<div class="bar" id="br'+i+'" style="background:'+colors[i-1]+'; opacity:0.1"></div>';
            function setBars(lvl){for(let i=1;i<=10;i++)document.getElementById('br'+i).style.opacity=(i<=lvl)?"1":"0.1";}
            function cn(){
                ws=new WebSocket('ws://'+location.host+'/ws');
                ws.onopen=()=>{con=true;inf.innerText='SISTEM AKTIF';ping();};
                ws.onclose=()=>{con=false;inf.innerText='KESILDI';setBars(0);setTimeout(cn,1500)};
                ws.onmessage=(e)=>{
                    if(e.data==='PONG'){
                        let lat=Date.now()-pT,lvl=0;
                        if(lat<20)lvl=10;else if(lat<40)lvl=9;else if(lat<60)lvl=8;else if(lat<80)lvl=7;else if(lat<100)lvl=6;else if(lat<120)lvl=5;else if(lat<140)lvl=4;else if(lat<150)lvl=3;else if(lat<180)lvl=2;else lvl=1;
                        setBars(lvl);
                    }
                };
            }
            function ping(){if(con){pT=Date.now();ws.send('PING');setTimeout(ping,800);}}
            function setup(id){
                const el=document.getElementById(id),rid=el.dataset.r,inp=document.getElementById('s'+id.slice(1));
                el.onpointerdown=(e)=>{e.preventDefault();if(!con||b7.classList.contains('pasif'))return;el.classList.add('akt');ws.send(rid+':1:'+(parseFloat(inp?.value)||0));};
                el.onpointerup=()=>{if(!parseFloat(inp?.value)){el.classList.remove('akt');ws.send(rid+':0:0')}};
            }
            for(let i=1;i<=6;i++)setup('b'+i);
            b7.onpointerdown=()=>{let k=b7.classList.toggle('pasif');document.getElementById('gv').classList.toggle('estop-green',k);ws.send('r7:'+(k?1:0)+':0');};
            document.getElementById('b8').onclick=(e)=>{if(!b7.classList.contains('pasif'))ws.send('r8:'+(e.target.classList.toggle('akt')?1:0)+':0')};
            cn();
        </script></body></html>"""

# --- 4. WEBSOCKET İŞLEYİCİ ---
def handle_ws(c, addr):
    c.settimeout(0.01); last = time.ticks_ms()
    try:
        while True:
            now = time.ticks_ms()
            if time.ticks_diff(now, last) > 3000: break 
            for r, t in bitis.items():
                if t != 0 and time.ticks_diff(t, now) <= 0:
                    röleler[r].value(0); bitis[r] = 0
            try:
                p = c.recv(1024)
                if not p: break
                last = now
                m, y = p[2:6], p[6:]; msg = "".join([chr(y[i] ^ m[i%4]) for i in range(len(y))])
                if msg == 'PING':
                    c.send(b'\x81\x04PONG')
                    continue
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
            except: pass
            time.sleep(0.05)
    finally:
        stop_all(); c.close(); gc.collect()

# --- 5. ANA DÖNGÜ ---
def run():
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('', 80)); s.listen(1)
    try:
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
                    cl.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection: close\r\n\r\n" + web_page())
                    cl.close()
            except Exception: pass
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("DURDURULDU"); stop_all()
    finally:
        s.close()

run()