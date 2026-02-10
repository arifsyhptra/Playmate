<template>
  <div>
    <h2>Detail Mobil</h2>

    <p><b>Chassis:</b> {{ chassis }}</p>

    <table border="1">
      <thead>
        <tr>
          <th>WO</th>
          <th>Model</th>
          <th>KM</th>
          <th>Tanggal</th>
          <th>Mechanic</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="row in wo" :key="row.wo_id">
          <td>{{ row.wo_id }}</td>
          <td>{{ row.mod_id }}</td>
          <td>{{ row.km }}</td>
          <td>{{ row.date_in }}</td>
          <td>{{ row.mechanic }}</td>
        </tr>
      </tbody>
    </table>

    <button @click="goBack">⬅ Kembali</button>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { useRoute, useRouter } from "vue-router"

const route = useRoute()
const router = useRouter()

const wo = ref([])
const chassis = route.params.chassis

const goBack = () => {
  router.push("/bengkel")
}

onMounted(async () => {
  const cus = localStorage.getItem("cus_name")
  if (!cus) {
    router.push("/login")
    return
  }

  const res = await fetch(
    `http://127.0.0.1:8000/wo/customer/${cus}/chassis/${chassis}`
  )
  wo.value = await res.json()
})
</script>
