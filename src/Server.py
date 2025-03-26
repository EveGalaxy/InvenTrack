from flask import Flask, jsonify
from flask_cors import CORS
import pymysql

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='11223344',
        database='demo_radiomap'
    )

@app.route('/api/data', methods=['GET'])
def get_data():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT x, y, z, beacon_id, beacon_name, rssi, timestamp FROM radiomap")
    rows = cursor.fetchall()
    conn.close()

    data = [
        {"x": row[0], "y": row[1], "z": row[2],"beacon_id": row[3], "beacon_name": row[4], "rssi": row[5], "timestamp": row[6]}
        for row in rows
    ]
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
