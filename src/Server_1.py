from flask import Flask, request, jsonify
from flask_cors import CORS
import asyncio
from bleak import BleakScanner
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

# การตั้งค่าการเชื่อมต่อ MySQL
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '11223344',
    'database': 'demo_radiomap'
}

# เส้นทางสำหรับบันทึกข้อมูล
@app.route('/api/save-beacon-data', methods=['POST'])
def save_beacon_data():
    try:
        # รับข้อมูลจาก Frontend
        data = request.get_json()
        x = data.get('x')
        y = data.get('y')
        z = data.get('z')
        beacon_id = data.get('beaconId')
        beacon_name = data.get('beaconName')
        rssi = data.get('rssi')

        # เชื่อมต่อฐานข้อมูล
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # บันทึกข้อมูลลงฐานข้อมูล
        query = "INSERT INTO radiomap (x, y, z, beacon_id, beacon_name, rssi) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (x, y, z, beacon_id, beacon_name, rssi))
        connection.commit()

        # ส่งผลลัพธ์กลับไป
        return jsonify({'success': True, 'message': 'Data saved successfully!'}), 200

    except Error as e:
        print(f"Database error: {e}")
        return jsonify({'success': False, 'error': 'Database error'}), 500

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()

async def scan_beacons():
    devices = await BleakScanner.discover()
    return [
        {
            'name': d.name or 'Unknown',
            'address': d.address,
            'rssi': d.rssi
        }
        for d in devices
        if d.address and d.rssi is not None
    ]

# เส้นทางสำหรับดึงค่า RSSI โดยการสแกน
@app.route('/api/get-beacon-rssi', methods=['POST'])
def get_beacon_rssi():
    try:
        
        # รับข้อมูล Beacon ID และ Name จากผู้ใช้
        data = request.get_json()
        beacon_id = data.get('beaconId')
        beacon_name = data.get('beaconName')

        # if not beacon_id or not beacon_name:
        #     return jsonify({'success': False, 'error': 'Beacon ID and Name are required'}), 400
        
        # สแกนหา Beacon รอบๆ
        scanned_beacons = asyncio.run(scan_beacons())

        # ค้นหา Beacon ที่ตรงกับ Beacon ID และ Name
        matching_beacons = [
            b for b in scanned_beacons if beacon_name.lower() in (b['name'] or '').lower()
        ]

        if matching_beacons:
            # หากพบ Beacon ให้ส่งค่า RSSI กลับไป
            return jsonify({'success': True, 'rssi': matching_beacons[0]['rssi']}), 200
        else:
            return jsonify({'success': False, 'message': 'No matching beacon found nearby'}), 404

    except Exception as e:
        print(f"Error scanning beacons: {e}")
        return jsonify({'success': False, 'error': 'Error scanning beacons'}), 500
    

@app.route('/api/data', methods=['GET'])
def get_data():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT x, y, z, beacon_id, beacon_name, rssi, timestamp FROM radiomap")
    rows = cursor.fetchall()
    conn.close()

    data = [
        {"x": row[0], "y": row[1], "z": row[2],"beacon_id": row[3], "beacon_name": row[4], "rssi": row[5], "timestamp": row[6]}
        for row in rows
    ]
    return jsonify(data)


# เริ่มเซิร์ฟเวอร์ Flask
if __name__ == '__main__':
    app.run(debug=True, port=3000)
