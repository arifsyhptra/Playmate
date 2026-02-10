<template>
  <div style="padding:30px;">
    <h2>Forecast Service Kendaraan</h2>

    <table border="1" cellpadding="6" cellspacing="0">
      <thead>
        <tr>
          <th>Customer</th>
          <th>Model</th>
          <th>Chassis</th>
          <th>KM Sekarang</th>
          <th>KM Service Berikutnya</th>
          <th>Estimasi Hari</th>
          <th>Status</th>
          <th>Aksi</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="row in data" :key="row.wo_id">
          <td>{{ row.cus_name }}</td>
          <td>{{ row.mod_id }}</td>
          <td>{{ row.chassis }}</td>
          <td>{{ row.km_sekarang }}</td>
          <td>{{ row.km_service_berikutnya }}</td>
          <td>{{ row.estimasi_hari }} hari</td>
          <td>{{ row.status }}</td>
          <td>
            <button @click="copyPesan(row)">Copy</button>
            <button @click="sendWA(row)">WhatsApp</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"

const data = ref([])

onMounted(async () => {
  const res = await fetch("http://127.0.0.1:8000/admin/forecast")
  data.value = await res.json()
})

const buildMessage = (row) => {
  return `
Yth. Bapak/Ibu ${row.cus_name},

Kami informasikan bahwa kendaraan Anda:
Model : ${row.mod_id}
Chassis : ${row.chassis}

Berdasarkan estimasi pemakaian kendaraan, service berikutnya disarankan dilakukan dalam ${row.estimasi_hari} hari ke depan atau saat kilometer mencapai ± ${row.km_service_berikutnya} km.

Silakan melakukan penjadwalan service agar performa kendaraan tetap optimal.
Terima kasih atas kepercayaan Anda kepada bengkel kami.
`.trim()
}

const copyPesan = (row) => {
  navigator.clipboard.writeText(buildMessage(row))
  alert("Pesan berhasil disalin")
}

const sendWA = (row) => {
  const phone = "6282279593771"
  const text = encodeURIComponent(buildMessage(row))
  window.open(`https://wa.me/${phone}?text=${text}`, "_blank")
}
</script>
