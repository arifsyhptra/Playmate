<!-- frontend/src/views/Tennis.vue -->
<template>
  <div class="container">
    <h1>🎾 Tennis</h1>
    <p>Jadwal tetap mingguan. Pilih slot dan join.</p>

    <table>
      <thead>
        <tr>
          <th>Hari</th>
          <th>Jam</th>
          <th>Kapasitas</th>
          <th>Terisi</th>
          <th>Aksi</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="slot in slots" :key="slot.id">
          <td>{{ slot.day }}</td>
          <td>{{ slot.time }}</td>
          <td>{{ slot.capacity }}</td>
          <td>{{ slot.joined }}</td>
          <td>
            <button
              :disabled="slot.joined >= slot.capacity"
              @click="join(slot)"
            >
              Join
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: "Tennis",
  data() {
    return {
      slots: [
        {
          id: 1,
          day: "Sabtu",
          time: "07:00 - 09:00",
          capacity: 4,
          joined: 2
        },
        {
          id: 2,
          day: "Minggu",
          time: "16:00 - 18:00",
          capacity: 4,
          joined: 4
        }
      ]
    };
  },
  methods: {
    join(slot) {
      if (slot.joined < slot.capacity) {
        slot.joined++;
        alert("Berhasil join. Lanjut ke pembayaran.");
      }
    }
  }
};
</script>

<style scoped>
.container {
  padding: 32px;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

th,
td {
  border: 1px solid #ddd;
  padding: 10px;
  text-align: center;
}

th {
  background-color: #f5f5f5;
}

button {
  padding: 6px 12px;
  cursor: pointer;
}

button:disabled {
  background: #ccc;
  cursor: not-allowed;
}
</style>
