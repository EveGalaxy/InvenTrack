import mysql.connector
import numpy as np
import asyncio
from bleak import BleakScanner  # ใช้ Bleak สำหรับ Windows/Linux/Mac

# ตั้งค่าการเชื่อมต่อ MySQL
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '11223344',
    'database': 'demo_radiomap'
}

# 🛜 MAC Address ของ Beacon ที่ต้องการสแกน
BEACON_MAC = "D8:6F:B8:83:E6:55"  # เปลี่ยนเป็น MAC Address จริง

# 🛜 ฟังก์ชันสแกน Beacon และดึงค่า RSSI
async def scan_beacon():
    devices = await BleakScanner.discover()
    for dev in devices:
        if dev.address == BEACON_MAC:
            print(f"🔹 Beacon พบแล้ว! RSSI = {dev.rssi} dBm")
            return dev.rssi  # คืนค่า RSSI ของ Beacon

    print("❌ ไม่พบ Beacon")
    return None  # ถ้าไม่เจอให้คืนค่า None

# 🎯 คำนวณ Euclidean Distance จากค่าที่สแกนได้
def calculate_euclidean(current_rssi):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # ดึงข้อมูล RSSI จาก MySQL
    sql = "SELECT slot, collect, rssi_nb1, rssi_nb2, rssi_nb3, rssi_nb4 FROM radiomap_slot;"
    cursor.execute(sql)
    results = cursor.fetchall()

    ed_list = []

    for row in results:
        slot, collect, nb1, nb2, nb3, nb4 = row
        
        # ข้ามแถวที่มีค่า NULL
        if None in (nb1, nb2, nb3, nb4):
            continue

        # คำนวณ Euclidean Distance
        db_rssi = np.array([nb1, nb2, nb3, nb4])
        ed = np.linalg.norm(db_rssi - current_rssi)

        # เก็บค่า ED
        ed_list.append((slot, collect, ed))

    conn.close()

    # เรียงลำดับจากค่า ED ต่ำสุด (ใกล้เคียงที่สุด)
    ed_list.sort(key=lambda x: x[2])

    print("\n🔹 **ผลลัพธ์ Euclidean Distance** 🔹")
    for slot, collect, ed in ed_list[:10]:  # แสดง 10 อันดับแรก
        print(f"Slot {slot}, Collect {collect}, ED = {ed:.4f}")

# ✅ ฟังก์ชันหลัก
async def main():
    rssi_value = await scan_beacon()  # รับค่า RSSI จาก Beacon จริง

    if rssi_value is not None:
        current_rssi = np.array([rssi_value, rssi_value, rssi_value, rssi_value])  # ใช้ค่าเดียวกันทั้ง 4 NB (หากมี 1 Beacon)
        calculate_euclidean(current_rssi)
    else:
        print("❌ ไม่สามารถคำนวณได้ เนื่องจากไม่พบ Beacon")

# 🚀 เรียกใช้โปรแกรม
asyncio.run(main())
