from flask import Flask, render_template, jsonify, request, redirect, url_for, session
import xml.etree.ElementTree as ET
import random
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quran_readings.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'
db = SQLAlchemy(app)

class Reading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    aya_text = db.Column(db.String, nullable=False)
    sura = db.Column(db.String, nullable=False)
    aya_num = db.Column(db.String, nullable=False)
    ip_address = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

def parse_quran(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    ayat = []
    for sura in root.findall('sura'):
        sura_name = sura.get('name')
        for aya in sura.findall('aya'):
            ayat.append({
                'text': aya.get('text'),
                'sura': sura_name,
                'aya_num': aya.get('index')
            })
    return ayat

ayat = parse_quran('quran-simple-plain.xml')
random.shuffle(ayat)
used_ayat = []
khatm_number = 1

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/next_aya')
def next_aya():
    global used_ayat, khatm_number, ayat
    if len(used_ayat) == len(ayat):
        used_ayat = []
        khatm_number += 1
        random.shuffle(ayat)
    
    next_aya = ayat[len(used_ayat)]
    used_ayat.append(next_aya)

    ip_address = request.remote_addr
    new_reading = Reading(
        aya_text=next_aya['text'],
        sura=next_aya['sura'],
        aya_num=next_aya['aya_num'],
        ip_address=ip_address
    )
    db.session.add(new_reading)
    db.session.commit()
    
    return jsonify({
        'aya': next_aya['text'],
        'sura': next_aya['sura'],
        'aya_num': next_aya['aya_num'],
        'khatm_number': khatm_number
    })

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        if password == '110114aliali':  # جایگزین 'your_password' با رمز عبور خودت
            session['logged_in'] = True
            return redirect(url_for('readings'))
        else:
            return render_template('login.html', error='رمز عبور نادرست است')
    return render_template('login.html')

@app.route('/readings')
def readings():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    all_readings = Reading.query.order_by(Reading.timestamp.desc()).all()
    return render_template('readings.html', readings=all_readings)

@app.route('/delete_reading/<int:reading_id>', methods=['POST'])
def delete_reading(reading_id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    reading = Reading.query.get(reading_id)
    if reading:
        db.session.delete(reading)
        db.session.commit()
    return redirect(url_for('readings'))

@app.route('/reset_khatm', methods=['POST'])
def reset_khatm():
    global used_ayat, khatm_number
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    used_ayat = []
    khatm_number += 1
    random.shuffle(ayat)
    db.session.query(Reading).delete()
    db.session.commit()
    return redirect(url_for('readings'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
