from flask import Flask, jsonify
import xml.etree.ElementTree as ET
import random

app = Flask(__name__)

# پارس کردن فایل XML و استخراج آیه‌ها
def parse_quran(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    ayat = []
    for sura in root.findall('sura'):
        for aya in sura.findall('aya'):
            ayat.append(aya.get('text'))
    return ayat

# لیست آیه‌ها و شماره ختم
ayat = parse_quran('my_flask_app\quran-simple-plain.xml')
random.shuffle(ayat)
used_ayat = []
khatm_number = 1

@app.route('/')
def index():
    global used_ayat, khatm_number
    if len(used_ayat) == len(ayat):
        used_ayat = []
        khatm_number += 1
        random.shuffle(ayat)
    
    next_aya = ayat.pop()
    used_ayat.append(next_aya)
    
    return jsonify({
        'aya': next_aya,
        'khatm_number': khatm_number,
        'remaining': len(ayat) - len(used_ayat)
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001)
