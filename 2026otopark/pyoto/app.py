from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response, Response
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import sqlite3
import os
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from apscheduler.schedulers.background import BackgroundScheduler
import threading
try:
    import RPi.GPIO as GPIO
    GPIO_AVAILABLE = True
except ImportError:
    GPIO_AVAILABLE = False
# import cv2
try:
    from picamera2 import Picamera2
    PICAM_AVAILABLE = True
except ImportError:
    PICAM_AVAILABLE = False
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this to a secure key
# app.config['SESSION_TYPE'] = 'filesystem'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

DB_PATH = 'otopark.db'

# GPIO setup for servo
SERVO_PIN = 18
if GPIO_AVAILABLE:
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SERVO_PIN, GPIO.OUT)
    pwm = GPIO.PWM(SERVO_PIN, 50)
    pwm.start(0)
else:
    pwm = None

# Scheduler for hourly checks
scheduler = BackgroundScheduler()
# scheduler.start()

class User(UserMixin):
    def __init__(self, id, plaka, name, surname, passw):
        self.id = id
        self.plaka = plaka
        self.name = name
        self.surname = surname
        self.passw = passw

@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("SELECT kod, plaka, name, surname, passw FROM user WHERE kod = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return User(user[0], user[1], user[2], user[3], user[4])
    return None

def get_db_connection():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def hourly_status_update():
    conn = get_db_connection()
    cursor = conn.cursor()
    now = datetime.now()
    cursor.execute("""
        UPDATE rights SET durum = 'BİTTİ'
        WHERE durum = 'AKTİF' AND finish_date < ? OR (finish_date = ? AND start_clock < ?)
    """, (now.date(), now.date(), now.time()))
    conn.commit()
    conn.close()

# scheduler.add_job(hourly_status_update, 'interval', hours=1)

# Camera setup
def camera_thread():
    if PICAM_AVAILABLE:
        picam2 = Picamera2()
        picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
        picam2.start()
        while True:
            frame = picam2.capture_array()
            # Process frame for license plate
            # Placeholder: detect plate
            # If plate detected and authorized, open gate
            time.sleep(1)
    else:
        # Fallback for non-RPi
        # cap = cv2.VideoCapture(0)
        while True:
            # ret, frame = cap.read()
            # if ret:
                # Process frame
            pass
            time.sleep(1)

# Start camera thread
# threading.Thread(target=camera_thread, daemon=True).start()

# USB Camera for streaming
def gen_frames():
    # cap = cv2.VideoCapture(1)
    while True:
        # success, frame = cap.read()
        # if not success:
        #     break
        # else:
        #     ret, buffer = cv2.imencode('.jpg', frame)
        #     frame = buffer.tobytes()
        #     yield (b'--frame\r\n'
        #            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + b'fake' + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    # Check for cookie
    plaka_cookie = request.cookies.get('plaka')
    if plaka_cookie:
        # Check if user exists and has active rights
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user WHERE plaka = ?", (plaka_cookie,))
        user = cursor.fetchone()
        if user:
            cursor.execute("SELECT * FROM rights WHERE plaka = ? AND durum = 'AKTİF' ORDER BY finish_date DESC LIMIT 1", (plaka_cookie,))
            active_right = cursor.fetchone()
            cursor.execute("SELECT * FROM rights WHERE plaka = ? ORDER BY start_date DESC LIMIT 3", (plaka_cookie,))
            recent_rights = cursor.fetchall()
            conn.close()
            kalan_gun = None
            if active_right:
                kalan_gun = (datetime.strptime(active_right['finish_date'], '%Y-%m-%d').date() - datetime.now().date()).days
            return render_template('index.html', user=user, active_right=active_right, recent_rights=recent_rights, kalan_gun=kalan_gun)
        conn.close()
    return render_template('index.html')

@app.route('/kayitli_abone', methods=['GET', 'POST'])
def kayitli_abone():
    if request.method == 'POST':
        plaka = request.form['plaka']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user WHERE plaka = ? AND passw = ?", (plaka, password))
        user = cursor.fetchone()
        if user:
            cursor.execute("SELECT * FROM rights WHERE plaka = ?", (plaka,))
            rights = cursor.fetchall()
            conn.close()
            # Set cookie
            resp = make_response(render_template('kayitli_abone.html', user=user, rights=rights))
            resp.set_cookie('plaka', plaka)
            return resp
        else:
            flash('Plaka veya şifre yanlış')
            conn.close()
    return render_template('kayitli_abone_form.html')

@app.route('/yeni_abone', methods=['GET', 'POST'])
def yeni_abone():
    if request.method == 'POST':
        # Handle form submission
        plaka = request.form['plaka']
        name = request.form['name']
        surname = request.form['surname']
        tel = request.form['tel']
        eposta = request.form['eposta']
        arac_marka = request.form['arac_marka']
        passw = request.form['passw']
        gun_sayisi = int(request.form['gun_sayisi'])
        gunluk_fiyat = 10  # Example price
        odeme = gun_sayisi * gunluk_fiyat
        start_date = datetime.now().date()
        finish_date = start_date + timedelta(days=gun_sayisi)
        start_clock = datetime.now().time()

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if plaka already exists
        cursor.execute("SELECT kod FROM user WHERE plaka = ?", (plaka,))
        existing_user = cursor.fetchone()
        if existing_user:
            conn.close()
            flash('Bu plaka zaten kayıtlı.')
            return redirect(url_for('yeni_abone'))

        cursor.execute("""
            INSERT INTO user (plaka, name, surname, tel, eposta, araç_marka, passw, durum)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'BEKLEMEDE')
        """, (plaka, name, surname, tel, eposta, arac_marka, passw))
        cursor.execute("""
            INSERT INTO rights (plaka, start_date, finish_date, durum, odeme, günlükfiat)
            VALUES (?, ?, ?, 'BEKLEMEDE', ?, ?)
        """, (plaka, start_date, finish_date, odeme, gunluk_fiyat))
        conn.commit()
        conn.close()

        # Send email to superuser
        send_email('Superuser Email', 'Yeni abone kaydı', f'Yeni abone: {plaka}')

        flash('Kayıt başarılı, ödeme yapınız')
        return redirect(url_for('odeme'))
    return render_template('yeni_abone.html')

@app.route('/odeme')
def odeme():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM rights WHERE durum = 'BEKLEMEDE'")
    payments = cursor.fetchall()
    conn.close()
    return render_template('odeme.html', payments=payments)

@app.route('/otopark_kullanimi')
def otopark_kullanimi():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usage")
    usages = cursor.fetchall()
    conn.close()
    return render_template('otopark_kullanimi.html', usages=usages)

@app.route('/ac_kapi')
@login_required
def ac_kapi():
    # Check if user has active rights
    plaka = current_user.plaka
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM rights WHERE plaka = ? AND durum = 'AKTİF' AND finish_date >= ? AND start_clock <= ?", (plaka, datetime.now().date(), datetime.now().time()))
    active = cursor.fetchone()
    conn.close()
    if active:
        # Open gate
        if pwm:
            pwm.ChangeDutyCycle(7.5)  # Example for servo
            time.sleep(1)
            pwm.ChangeDutyCycle(0)
        return 'Kapı açıldı'
    else:
        return 'Aktif kayıt bulunamadı'

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT passw FROM password WHERE kod = 1")
        admin_pass = cursor.fetchone()[0]
        conn.close()
        if password == admin_pass:
            session['admin'] = True
            return redirect(url_for('superuser'))
        else:
            flash('Yanlış parola')
    return render_template('admin_login.html')

@app.route('/superuser')
def superuser():
    if not session.get('admin'):
        return redirect(url_for('admin'))
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user")
    users = cursor.fetchall()
    cursor.execute("SELECT * FROM rights")
    rights = cursor.fetchall()
    conn.close()
    return render_template('superuser.html', users=users, rights=rights)

@app.route('/add_user', methods=['POST'])
def add_user():
    if not session.get('admin'):
        return redirect(url_for('admin'))
    plaka = request.form['plaka']
    name = request.form['name']
    surname = request.form['surname']
    tel = request.form['tel']
    eposta = request.form['eposta']
    arac_marka = request.form['arac_marka']
    passw = request.form['passw']
    durum = request.form['durum']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user (plaka, name, surname, tel, eposta, araç_marka, passw, durum) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                   (plaka, name, surname, tel, eposta, arac_marka, passw, durum))
    conn.commit()
    conn.close()
    flash('Kullanıcı eklendi')
    return redirect(url_for('superuser'))

@app.route('/add_right', methods=['POST'])
def add_right():
    if not session.get('admin'):
        return redirect(url_for('admin'))
    plaka = request.form['plaka']
    start_date = request.form['start_date']
    finish_date = request.form['finish_date']
    durum = request.form['durum']
    odeme = request.form['odeme']
    günlükfiat = request.form['günlükfiat']
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO rights (plaka, start_date, finish_date, durum, odeme, günlükfiat) VALUES (?, ?, ?, ?, ?, ?)",
                   (plaka, start_date, finish_date, durum, odeme, günlükfiat))
    conn.commit()
    conn.close()
    flash('Hak eklendi')
    return redirect(url_for('superuser'))

@app.route('/search')
def search():
    if not session.get('admin'):
        return redirect(url_for('admin'))
    query = request.args.get('query')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user WHERE plaka LIKE ?", ('%' + query + '%',))
    users = cursor.fetchall()
    cursor.execute("SELECT * FROM rights WHERE plaka LIKE ?", ('%' + query + '%',))
    rights = cursor.fetchall()
    conn.close()
    return render_template('superuser.html', users=users, rights=rights, search=True)

@app.route('/view_rights')
def view_rights():
    if not session.get('admin'):
        return redirect(url_for('admin'))
    plaka = request.args.get('plaka')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM rights WHERE plaka = ?", (plaka,))
    rights = cursor.fetchall()
    conn.close()
    return render_template('view_rights.html', rights=rights, plaka=plaka)

@app.route('/edit_user/<int:kod>', methods=['GET', 'POST'])
def edit_user(kod):
    if not session.get('admin'):
        return redirect(url_for('admin'))
    conn = get_db_connection()
    cursor = conn.cursor()
    if request.method == 'POST':
        plaka = request.form['plaka']
        name = request.form['name']
        surname = request.form['surname']
        tel = request.form['tel']
        eposta = request.form['eposta']
        arac_marka = request.form['arac_marka']
        passw = request.form['passw']
        durum = request.form['durum']
        cursor.execute("UPDATE user SET plaka=?, name=?, surname=?, tel=?, eposta=?, araç_marka=?, passw=?, durum=? WHERE kod=?",
                       (plaka, name, surname, tel, eposta, arac_marka, passw, durum, kod))
        conn.commit()
        conn.close()
        flash('Kullanıcı güncellendi')
        return redirect(url_for('superuser'))
    cursor.execute("SELECT * FROM user WHERE kod = ?", (kod,))
    user = cursor.fetchone()
    conn.close()
    return render_template('edit_user.html', user=user)

@app.route('/delete_user/<int:kod>')
def delete_user(kod):
    if not session.get('admin'):
        return redirect(url_for('admin'))
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM user WHERE kod = ?", (kod,))
    conn.commit()
    conn.close()
    flash('Kullanıcı silindi')
    return redirect(url_for('superuser'))

@app.route('/edit_right/<int:kod>', methods=['GET', 'POST'])
def edit_right(kod):
    if not session.get('admin'):
        return redirect(url_for('admin'))
    conn = get_db_connection()
    cursor = conn.cursor()
    if request.method == 'POST':
        plaka = request.form['plaka']
        start_date = request.form['start_date']
        finish_date = request.form['finish_date']
        durum = request.form['durum']
        odeme = request.form['odeme']
        günlükfiat = request.form['günlükfiat']
        cursor.execute("UPDATE rights SET plaka=?, start_date=?, finish_date=?, durum=?, odeme=?, günlükfiat=? WHERE kod=?",
                       (plaka, start_date, finish_date, durum, odeme, günlükfiat, kod))
        conn.commit()
        conn.close()
        flash('Hak güncellendi')
        return redirect(url_for('superuser'))
    cursor.execute("SELECT * FROM rights WHERE kod = ?", (kod,))
    right = cursor.fetchone()
    conn.close()
    return render_template('edit_right.html', right=right)

@app.route('/delete_right/<int:kod>')
def delete_right(kod):
    if not session.get('admin'):
        return redirect(url_for('admin'))
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM rights WHERE kod = ?", (kod,))
    conn.commit()
    conn.close()
    flash('Hak silindi')
    return redirect(url_for('superuser'))

def send_email(to, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = 'roboturx@gmail.com'
    msg['To'] = to

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('roboturx@gmail.com', '2123397')  # Use an app password, not your regular password
    server.sendmail('roboturx@gmail.com', to, msg)
    server.quit()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)