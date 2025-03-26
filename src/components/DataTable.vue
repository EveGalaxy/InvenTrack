<template>
  <div class="container">
    <h1>Beacon Data for RadioMap</h1>
    <table>
      <thead>
        <tr>
          <th>X</th>
          <th>Y</th>
          <th>Z</th>
          <th>Address</th>
          <th>Name</th>
          <th>Rssi</th>
          <th>TimeStamp</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(row, index) in data" :key="index">
          <td>{{ row.x }}</td>
          <td>{{ row.y }}</td>
          <td>{{ row.z }}</td>
          <td>{{ row.beacon_id }}</td>
          <td>{{ row.beacon_name }}</td>
          <td>{{ row.rssi }}</td>
          <td>{{ row.timestamp }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      data: []
    };
  },
  mounted() {
    axios.get('http://localhost:3000/api/data')
      .then(response => {
        this.data = response.data;
      })
      .catch(error => {
        console.error("There was an error fetching the data!", error);
      });
  }
};
</script>

<style>
.container {
  margin: 10px;
  padding: 30px;
  display: flex;
  flex-wrap: wrap;
  background-color: rgb(128, 143, 139);
}
h1 {
  color: black;
}
table {
  width: auto;
  border-collapse: collapse;
}
th, td {
  color: black;
  border: 1px solid black;
  padding: 8px;
  text-align: left;
}
</style>