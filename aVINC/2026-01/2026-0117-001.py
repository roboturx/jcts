import network, socket, machine, time, binascii, gc

# --- AYARLAR ---
WIFI_SSID = "Vinc_Pico_Pro"
WIFI_PW = "password123"
AKTIF_OPERATOR = None
SON_SINYAL = time.ticks_ms()
ACIL_STOP = False

# --- DONANIM ---
buzzer = machine.PWM(machine.Pin(13))
r_pins = [14,15,16,17,18,19,20,21]
röleler = {f'r{i+1}': machine.Pin(p, machine.Pin.OUT, value=0) for i, p in enumerate(r_pins)}

# --- NETWORK ---
wifi = network.WLAN(network.AP_IF)
wifi.config(essid=WIFI_SSID, password=WIFI_PW)
wifi.active(True)

def anahtar_hesapla(key):
    import uhashlib as hashlib
    res = hashlib.sha1((key + "258EAFA5-E914-47DA-95CA-C5AB0DC85B11").encode()).digest()
    return binascii.b2a_base64(res).decode().strip()

# Sunucuyu Başlat
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', 80))
s.listen(1)
s.settimeout(0.1) # Kilitlenmeyi önlemek için zaman aşımı

print("Sistem Hazır: 192.168.4.1")

while True:
    simdi = time.ticks_ms()
    
    # EMNİYET KONTROLÜ (Thread yerine ana döngüde)
    if (AKTIF_OPERATOR and time.ticks_diff(simdi, SON_SINYAL) > 2000) or ACIL_STOP:
        for i in range(1, 7): röleler[f'r{i}'].value(0)
        buzzer.duty_u16(0)

    try:
        try:
            c, addr = s.accept()
        except:
            continue # Bağlantı yoksa döngüye devam et

        if AKTIF_OPERATOR is None: AKTIF_OPERATOR = addr[0]
        req = c.recv(512).decode()
        
        if 'Upgrade: websocket' in req:
            # WebSocket işlemleri buraya gelecek (V15'teki ile aynı)
            # ... (WebSocket kodlarını buraya ekleyebilirsiniz)
            pass
        elif "/reset" in req:
            machine.reset()
        else:
            # Kumanda HTML sayfasını gönder (V15'teki HTML'in aynısı)
            # c.send(sayfa_kumanda(addr[0]))
            pass
        c.close()
    except Exception as e:
        gc.collect()
