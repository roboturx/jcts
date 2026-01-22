import network, socket, machine, time, binascii, gc
try: import uhashlib as hashlib
except: import hashlib

gc.collect()

# --- AYARLAR ---
SSID, PW = "Vinc_Pico_Pro", "password123"
ACIL_STOP = False
SON_SINYAL = time.ticks_ms()
AKTIF_OP = None

# --- DONANIM ---
buzzer = machine.PWM(machine.Pin(13), freq=2000, duty_u16=0)
pins = [14,15,16,17,18,19,20,21]
r = {f'r{i+1}': machine.Pin(p, machine.Pin.OUT, value=0) for i, p in enumerate(pins)}
ZIT_YONLER = {'r1':'r2','r2':'r1','r3':'r4','r4':'r3','r5':'r6','r6':'r5'}

# --- AG KURULUMU ---
ap = network.WLAN(network.AP_IF)
ap.config(essid=SSID, password=PW)
ap.active(True)

def ws_handshake(key):
    magic = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
    sha1 = hashlib.sha1((key + magic).encode()).digest()
    return binascii.b2a_base64(sha1).decode().strip()

# --- ARAYÜZ ---
HTML = """HTTP/1.1 200 OK\r\n\r\n<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1,user-scalable=0">
<style>
body{background:#111;color:#fff;text-align:center;font-family:sans-serif;margin:0;touch-action:none;user-select:none;}
.p{background:#f1c40f;color:#000;padding:10px;border:5px solid #d35400;border-radius:20px;display:flex;margin:10px auto;width:310px;}
.l{width:70px;display:flex;flex-direction:column;align-items:center;justify-content:space-between;border-right:3px solid #d35400;min-height:430px;}
.s-v{display:flex;flex-direction:column-reverse;background:#000;height:150px;width:22px;border-radius:5px;}
.s-b{width:100%;height:12px;margin:1px 0;background:#333;}
.m-c{flex:1;padding-left:10px;}
.g{display:grid;grid-template-columns:1fr 1fr;gap:12px;}
.btn{width:75px;height:75px;background:#222;color:#fff;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:35px;border:4px solid #444;}
.aktif{background:#e74c3c!important;transform:scale(0.9);}
.lock{opacity:0.2;pointer-events:none;}
</style></head><body>
<div class="p"><div class="l"><div class="s-v" id="sb"></div>
<button onclick="location.href='/reset'" style="background:#922b21;color:#fff;border:none;padding:10px;border-radius:5px;">RST</button>
<div id="kb" style="width:50px;height:50px;background:#2980b9;border-radius:10px;color:#fff;display:flex;align-items:center;justify-content:center;font-weight:bold;">KRN</div>
</div><div class="m-c"><div id="ka" class="g">
<div class="btn m" id="r1">▲</div><div class="btn m" id="r2">▼</div>
<div class="btn m" id="r3">▲</div><div class="btn m" id="r4">▼</div>
<div class="btn m" id="r5">▲</div><div class="btn m" id="r6">▼</div>
</div><button id="st" style="background:#c0392b;color:#fff;width:100%;height:60px;margin-top:20px;border-radius:10px;font-size:20px;font-weight:bold;">STOP</button>
</div></div><script>
let ws=new WebSocket('ws://'+location.host);
ws.onopen=()=>{setInterval(()=>{if(ws.readyState===1)ws.send('p')},500)};
ws.onmessage=(e)=>{
    let d=JSON.parse(e.data); let b=document.getElementById('sb'); b.innerHTML="";
    for(let i=1;i<=10;i++)b.innerHTML+=`<div class="s-b" style="background:${i<=d.s?'lime':'#333'}"></div>`;
    document.getElementById('ka').className=d.st?"lock g":"g";
};
document.querySelectorAll('.m').forEach(b=>{
    b.onpointerdown=(e)=>{e.preventDefault();ws.send(b.id+":1")};
    b.onpointerup=()=>{ws.send(b.id+":0")};
});
document.getElementById('st').onclick=()=>ws.send("stop");
document.getElementById('kb').onpointerdown=()=>ws.send("r7:1");
document.getElementById('kb').onpointerup=()=>ws.send("r7:0");
</script></body></html>"""

# --- SUNUCU ---
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', 80))
s.listen(1)
s.settimeout(0.1)

print("Pico Hazir: 192.168.4.1")

while True:
    now = time.ticks_ms()
    
    # EMNİYET KONTROLÜ
    if (AKTIF_OP and time.ticks_diff(now, SON_SINYAL) > 2000) or ACIL_STOP:
        for i in range(1, 7): r[f'r{i}'].value(0)
    
    # BUZZER/SİREN
    if (r['r5'].value() or r['r6'].value() or r['r7'].value()) and not ACIL_STOP:
        buzzer.duty_u16(30000)
    else:
        buzzer.duty_u16(0)

    try:
        res = s.accept()
        c, addr = res
        req = c.recv(1024).decode()
        
        if 'Upgrade: websocket' in req:
            key = [l.split(':')[1].strip() for l in req.split('\r\n') if 'Sec-WebSocket-Key:' in l][0]
            c.send("HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Accept: "+ws_handshake(key)+"\r\n\r\n")
            AKTIF_OP = addr[0]
            c.settimeout(0.1)
            while True:
                try:
                    data = c.recv(64)
                    if not data: break
                    payload_len = data[1] & 127
                    mask = data[2:6]
                    payload = data[6:6+payload_len]
                    msg = "".join([chr(payload[i] ^ mask[i % 4]) for i in range(len(payload))])
                    
                    if msg == 'p':
                        SON_SINYAL = time.ticks_ms()
                        c.send(binascii.a2b_base64("gA==")+'{"s":10,"st":'+str(ACIL_STOP).lower()+'}')
                    elif msg == 'stop':
                        ACIL_STOP = not ACIL_STOP
                        for i in range(1,9): r[f'r{i}'].value(0)
                    elif ':' in msg:
                        cmd, val = msg.split(':'); v = int(val)
                        if cmd == "r7": r['r7'].value(v)
                        elif not ACIL_STOP:
                            if v == 1:
                                z = ZIT_YONLER.get(cmd)
                                if z and r[z].value(): r[z].value(0); time.sleep(0.3)
                                r[cmd].value(1)
                            else: r[cmd].value(0)
                        SON_SINYAL = time.ticks_ms()
                except:
                    if time.ticks_diff(time.ticks_ms(), SON_SINYAL) > 1500: break
                    continue
        elif '/reset' in req:
            machine.reset()
        else:
            c.send(HTML)
        c.close()
    except:
        if 'c' in locals(): c.close()
        gc.collect()
