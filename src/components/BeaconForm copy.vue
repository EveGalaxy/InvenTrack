<!-- <template>
    <div class="beacon-form">
      <h2>บันทึกข้อมูล RSSI ของ Beacon</h2>
      <form @submit.prevent="submitForm">
        <div>
          <label for="x">พิกัด X:</label>
          <input type="number" v-model="form.x" id="x" required />
        </div>
        <div>
          <label for="y">พิกัด Y:</label>
          <input type="number" v-model="form.y" id="y" required />
        </div>
        <div>
          <label for="z">พิกัด Z:</label>
          <input type="number" v-model="form.z" id="z" required />
        </div>
        <div>
          <label for="beacon">Beacon ID:</label>
          <select v-model="form.beaconId" id="beacon" required>
            <option value="" disabled selected>เลือก Beacon</option>
            <option v-for="beacon in beacons" :key="beacon.id" :value="beacon.name">
              {{ beacon.name }}
            </option>
          </select>
        </div>
        <div>
          <label for="rssi">ค่า RSSI:</label>
          <input type="number" v-model="form.rssi" id="rssi" required />
        </div>
        <button type="submit">บันทึก</button>
      </form>
      <p v-if="message" class="message">{{ message }}</p>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        form: {
          x: '',
          y: '',
          z: '',
          beaconId: '',
          rssi: '',
        },
        beacons: [
          { id: '1', name: 'IBKS 105 No 1' },
          { id: '2', name: 'IBKS 105 No 2' },
          { id: '3', name: 'IBKS 105 No 3' },
          { id: '4', name: 'IBKS 105 No 4' },
          { id: '5', name: 'IBKS 105 No 6' },
        ],
        message: '',
      };
    },
    methods: {
      async submitForm() {
        try {
          // ส่งข้อมูลไปยัง Backend
          const response = await fetch('http://localhost:3000/api/save-beacon-data', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(this.form),
          });
          const data = await response.json();
          if (data.success) {
            this.message = 'บันทึกข้อมูลสำเร็จ!';
          } else {
            this.message = 'เกิดข้อผิดพลาดในการบันทึกข้อมูล';
          }
        } catch (error) {
          console.error('Error:', error);
          this.message = 'ไม่สามารถเชื่อมต่อกับเซิร์ฟเวอร์';
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .beacon-form {
    max-width: 400px;
    margin: auto;
  }
  .message {
    margin-top: 10px;
    color: cyan;
  }
  </style>
   -->

  <template>
    <div class="container">
      <div class="beacon-form">
        <h2>บันทึกข้อมูล RSSI ของ Beacon</h2>
        <form @submit.prevent="submitForm">
          <div>
            <label for="x">พิกัด X:</label>
            <input type="number" v-model="form.x" id="x" required />
          </div>
          <div>
            <label for="y">พิกัด Y:</label>
            <input type="number" v-model="form.y" id="y" required />
          </div>
          <div>
            <label for="z">พิกัด Z:</label>
            <input type="number" v-model="form.z" id="z" required />
          </div>
          <div>
            <label for="beacon">Beacon Name:</label>
            <select v-model="form.beaconName" id="beacon" required @change="handleChangeBeacon">
              <option value="" disabled selected>เลือก Beacon</option>
              <option v-for="beacon in beacons" :key="beacon.id" :value="beacon.name">
                {{ beacon.name }}
              </option>
            </select>
          </div>
          <div>
            <label for="address">Beacon Address:</label>
            <input type="text" v-model="form.beaconId" id="address" readonly/>
          </div>
          <div>
            <label for="rssi">ค่า RSSI:</label>
            <input type="number" v-model="form.rssi" id="rssi" readonly />
          </div>
          <button type="submit">บันทึก</button>
        </form>
        <p v-if="message" class="message">{{ message }}</p>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        form: {
          x: '',
          y: '',
          z: '',
          beaconName: '',
          beaconId: '',
          rssi: ''
        },
        beacons: [
          { id: 'D8:6F:B8:83:E6:55', name: 'IBKS 105 No 1' },
          { id: 'F7:C4:0B:AE:40:95', name: 'IBKS 105 No 2' },
          { id: 'C2:AE:AB:86:5F:C2', name: 'IBKS 105 No 3' },
          { id: 'D5:99:FB:6D:1C:DA', name: 'IBKS 105 No 4' },
          { id: 'F0:40:4A:49:3E:2D', name: 'IBKS 105 No 6' },
        ],
        message: '',
      };
    },
    methods: {
      handleChangeBeacon() {
        this.updateBeaconAddress();
        this.fetchRssi();
      },
      updateBeaconAddress() {
        const selectedBeacon = this.beacons.find(
          (beacon) => beacon.name === this.form.beaconName
        );
        if (selectedBeacon) {
          this.form.beaconId = selectedBeacon.id
        } else {
          this.form.beaconId = "ไม่พบข้อมูล Beacon Address"
        }
      },
      async fetchRssi() {
        if (this.form.beaconName) {
          try {
            const response = await fetch('http://localhost:3000/api/get-beacon-rssi', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({beaconId: this.form.beaconId, beaconName: this.form.beaconName}),
            });
            const data = await response.json();
            if (data.success) {
              this.form.rssi = data.rssi;
            } else {
              this.form.rssi = '';
              this.message = data.message || 'ไม่พบข้อมูล Beacon ที่เกี่ยวข้อง';
            }
          } catch (error) {
            console.error('Error:', error);
            this.message = 'ไม่สามารถดึงข้อมูล Beacon ได้';
          }
        }
      },
      async submitForm() {
        try {
          const response = await fetch('http://localhost:3000/api/save-beacon-data', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(this.form),
          });
          const data = await response.json();
          if (data.success) {
            this.message = 'บันทึกข้อมูลสำเร็จ!';
          } else {
            this.message = 'เกิดข้อผิดพลาดในการบันทึกข้อมูล';
          }
        } catch (error) {
          console.error('Error:', error);
          this.message = 'ไม่สามารถเชื่อมต่อกับเซิร์ฟเวอร์';
        }
        this.clearForm();
      },
      clearForm() {
        this.form ={
          x: '',
          y: '',
          z: '',
          beaconName: '',
          beaconId: '',
          rssi: '',
        };
      },
    },
  };
  </script>
  
  <style scoped>
  .container {
    display: flex;
    flex-wrap: wrap;
  }
  .beacon-form {
    max-width: 400px;
    margin: auto;
    padding: 30px;
    font-weight: bold;
    color: black;
    background-color: lightblue;
  }
  .message {
    margin-top: 30px;
    color: green;
  }
  </style>
  