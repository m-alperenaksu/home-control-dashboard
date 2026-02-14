# server.py
# Arduino'dan veri okur, MySQL'e kaydeder, tarayıcıya sunar

import serial
import json
import mysql.connector
from http.server import HTTPServer, BaseHTTPRequestHandler

SERIAL_PORT = "COM3"  # kendi portunu yaz
BAUD_RATE   = 9600

DB_CONFIG = {
    "host":     "localhost",
    "user":     "root",
    "password": "password",  # kendi şifreni yaz
    "database": "home_monitor"
}

def init_db():
    conn = mysql.connector.connect(**DB_CONFIG)
    cur  = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS sensor_data (
            id        INT AUTO_INCREMENT PRIMARY KEY,
            temp      FLOAT,
            hum       FLOAT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_to_db(temp, hum):
    conn = mysql.connector.connect(**DB_CONFIG)
    cur  = conn.cursor()
    cur.execute("INSERT INTO sensor_data (temp, hum) VALUES (%s, %s)", (temp, hum))
    conn.commit()
    conn.close()

def get_latest():
    conn = mysql.connector.connect(**DB_CONFIG)
    cur  = conn.cursor()
    cur.execute("SELECT temp, hum FROM sensor_data ORDER BY id DESC LIMIT 1")
    row = cur.fetchone()
    conn.close()
    if row:
        return {"temp": row[0], "hum": row[1]}
    return {"temp": None, "hum": None}

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Arduino'dan oku ve MySQL'e kaydet
        try:
            ser  = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2)
            line = ser.readline().decode("utf-8").strip()
            ser.close()
            if line:
                data = json.loads(line)
                save_to_db(data["temp"], data["hum"])
        except:
            pass

        # MySQL'den son veriyi al
        latest = get_latest()

        body = json.dumps(latest).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        pass

init_db()
print("Server başladı: http://localhost:5000")
HTTPServer(("localhost", 5000), Handler).serve_forever()
